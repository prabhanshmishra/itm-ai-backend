"""
ITM AI - API Backend
Groq API + FastAPI
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

---------------- CONFIG ----------------

API_KEY = os.environ.get("GROQ_API_KEY", "*")
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = (
"Tum ek helpful, friendly Hindi-English (Hinglish) "
"bolne wale AI assistant ho."
)

---------------- APP ----------------

app = FastAPI(title="ITM AI")

client = Groq(api_key=API_KEY)

---------------- DATA MODELS ----------------

class ChatRequest(BaseModel):
message: str

class ChatResponse(BaseModel):
reply: str

---------------- API ----------------

@app.get("/")
def home():
return {
"status": "online",
"message": "ITM AI Backend is running 🚀"
}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

if not request.message.strip():  
    raise HTTPException(  
        status_code=400,  
        detail="Message empty nahi ho sakta."  
    )  

try:  
    response = client.chat.completions.create(  
        model=MODEL,  
        messages=[  
            {  
                "role": "system",  
                "content": SYSTEM_PROMPT  
            },  
            {  
                "role": "user",  
                "content": request.message  
            }  
        ],  
        temperature=0.7,  
    )  

    reply = response.choices[0].message.content  

    return ChatResponse(reply=reply)  

except Exception as e:  
    raise HTTPException(  
        status_code=500,  
        detail=f"AI Error: {str(e)}"  
    )

---------------- RUN DIRECTLY ----------------

if name == "main":
import uvicorn

uvicorn.run(  
    app,  
    host="0.0.0.0",  
    port=8000,  
    reload=False  
)
