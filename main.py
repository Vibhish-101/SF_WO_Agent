import os
from langchain_google_vertexai import ChatVertexAI
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'config.json'
# chat=ChatVertexAI(model_name="gemini-1.0-pro-002")
# llm=chat.invoke('tell me a joke')
# print(llm.content)
