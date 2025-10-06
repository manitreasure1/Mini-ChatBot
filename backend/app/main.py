from fastapi import FastAPI
from app.routes import auth, chat, user


app = FastAPI(title="Mini chatbot", summary="A mini text conversation chatbot ")





app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/chat")
app.include_router(user.router, prefix="/user")