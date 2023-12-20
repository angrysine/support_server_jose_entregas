from fastapi import FastAPI, Request
from telegram.model import ChatBotModel

app = FastAPI()
llm = ChatBotModel()

@app.get("/")
async def root(request: Request):
    body = await request.json()
 

    return {"message": llm.chat(body["message"])}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)