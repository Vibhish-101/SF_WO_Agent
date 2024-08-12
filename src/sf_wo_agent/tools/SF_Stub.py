import os
import logging
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
from simple_salesforce import Salesforce
import uvicorn
# Load environment variables from the .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Model for the customer request
class CustomerRequest(BaseModel):
    customer_order: str

# Salesforce credentials
def get_salesforce_credentials():
    return {
        "url": os.getenv("SALESFORCE_URL"),
        "username": os.getenv("SALESFORCE_USERNAME"),
        "password": os.getenv("SALESFORCE_PASSWORD"),
        "client_id": os.getenv("SALESFORCE_CLIENT_ID"),
        "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET"),
        "instance_url": os.getenv("SALESFORCE_INSTANCE_URL")
    }

# Validate Salesforce credentials
def validate_salesforce_credentials(credentials):
    for key, value in credentials.items():
        if not value:
            raise ValueError(f"Missing Salesforce environment variable: {key}")

# Salesforce authentication details
def authenticate_salesforce():
    credentials = get_salesforce_credentials()
    validate_salesforce_credentials(credentials)

    params = {
        "grant_type": "password",
        "username": credentials["username"],
        "password": credentials["password"],
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"]
    }

    try:
        # Request an access token
        response = requests.post(credentials["url"], data=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to authenticate with Salesforce: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to authenticate with Salesforce: {str(e)}")

    # Extract the access token from the response
    access_token = response.json().get("access_token")
    instance_url = credentials["instance_url"]

    if not access_token:
        logging.error("Failed to retrieve access token from Salesforce")
        raise HTTPException(status_code=500, detail="Failed to retrieve access token from Salesforce")

    logging.info("Successfully authenticated with Salesforce")
    return Salesforce(instance_url=instance_url, session_id=access_token)

# Fetch orchestration items for the customer
def fetch_orch_items(sf, customer_order):
    query = f"""
    SELECT
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.AccountName__c,
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.AccountStatus__c,
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.OrderNumber,
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.vlocity_cmt__OrderStatus__c,
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationItemType__c,
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__c,
    Name,
    Id,
    vlocity_cmt__OrchestrationItemId__r.Name,
    vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__State__c,
    vlocity_cmt__OrchestrationItemId__r.CreatedDate
    FROM
        vlocity_cmt__OrchestrationDependency__c
    where
        vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.Product_Name__c='Fiber Internet'
    and
        vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.Type!='Change'
    and
        vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.Service_State_Short__c not in ('NC','MO','TX','WI','AL','VA','OH','AR','PA','MS','GA','KS','TN','SC','IN','NJ','LA','IL')
    and 
        vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.OrderNumber = '{customer_order}'
    LIMIT 100
    """
    results = sf.query(query)
    return results['records']

# Normalize the records to extract only necessary fields
def normalize_records(records):
    normalized_data = []
    for record in records:
        normalized_record = {
            "Id": record.get("Id"),
            "AccountName": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__OrchestrationPlanId__r", {}).get("vlocity_cmt__AccountId__r", {}).get("AccountName__c"),
            "AccountStatus": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__OrchestrationPlanId__r", {}).get("vlocity_cmt__AccountId__r", {}).get("AccountStatus__c"),
            "OrderNumber": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__OrchestrationPlanId__r", {}).get("vlocity_cmt__OrderId__r", {}).get("OrderNumber"),
            "OrderStatus": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__OrchestrationPlanId__r", {}).get("vlocity_cmt__OrderId__r", {}).get("vlocity_cmt__OrderStatus__c"),
            "OrchestrationItemType": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__OrchestrationItemType__c"),
            "OrchestrationPlanId": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__OrchestrationPlanId__c"),
            "Dependency": record.get("Name"),
            "OrchestrationItemName": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("Name"),
            "OrchestrationItemState": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("vlocity_cmt__State__c"),
            "CreatedDate": record.get("vlocity_cmt__OrchestrationItemId__r", {}).get("CreatedDate")
            
        }
        normalized_data.append(normalized_record)
    return normalized_data


@app.websocket("/ws/orchestration-items/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            order = CustomerRequest(customer_order=data)

            try:
                # Authenticate and fetch Orchestration Items
                sf = authenticate_salesforce()
                orchestration_items = fetch_orch_items(sf, order.customer_order)
                normalized_items = normalize_records(orchestration_items)                
                # Send the Orchestration Items back to the Client
                await websocket.send_json({"orchestration_items": normalized_items})
            except Exception as e:
                logging.error(f"Error fetching orchestration items: {str(e)}")
                await websocket.send_json({"error": f"Failed to fetch orchestration items: {str(e)}"})

            # Sleep for delay
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        logging.info("Client disconnected")
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
        

# if __name__ == '__SF_Stub__':
#     uvicorn.run(app, host = "0.0.0.0", port = 8000)