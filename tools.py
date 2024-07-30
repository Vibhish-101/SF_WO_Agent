import json


with open('SF_Stub.json', 'r') as file:
        data = json.load(file)


@tool("Account_Status_Checker")
def Account_Status_Checker(address):
    "You are an expert in fetching account status for any given address."
    acc_status = data[address]["account"]
    return acc_status

@tool("Service_Appt_Checker")
def Service_Appt_Checker(address):
    "You are an expert in fetching service appointment information for any given address."
    service_appt = data[address]["service_appt"]
    return service_appt

@tool("Work_Order_Checker")
def Work_Order_Checker(address):
    "You are an expert in fetching work order information for any given address."
    work_order = data[address]["work_order"]
    return work_order

@tool("Work_Order_Checker")
def Work_Order_Checker(address):
    "You are an expert in fetching work order information for any given address."
    work_order = data[address]["work_order"]
    return work_order

@tool("SmartNID_Status_Checker")
def SmartNID_Status_Checker(address):
    "You are an expert in fetching SmartNID status for any given address."
    smartnid_status = data[address]["smartnid status"]
    return smartnid_status


@tool("Adapt_Status_Checker")
def Adapt_Status_Checker(address):
    "You are an expert in fetching adapt status for any given address."
    try:    
        adapt_status = data[address]["adapt_status"]
        return adapt_status
    except KeyError:
        return "Not found"


@tool("UDIF_Checker")
def UDIF_Checker(address):
    "You are an expert in fetching UDIF information for any given address."
    try:
        result = data[address]["UDIF"]
        return result
    except KeyError:
        return "Not found"


@tool("BSU_Checker")
def BSU_Checker(address):
    "You are an expert in fetching BSU information for any given address."
    try:
        result = data[address]["BSU"]
        return result
    except KeyError:
        return "Not found"


@tool("Result_Checker")
def Result_Checker(address):
    "You are an expert in fetching result information for any given address."
    result = data[address]["result"]
    return result


