from db.schemas import SendMessage
from db.models import ChatMessage
from textblob import TextBlob
from notebook.my_bot import ChatBot
from sqlmodel.ext.asyncio.session import AsyncSession

class ChatServive:
    async def send_message(self, message, session: AsyncSession):

        message_validation = SendMessage(**message)
        message = str(message_validation).strip()
        clean_txt = self.text_correction(message)

        response = ChatBot(clean_txt)

        user_id = ""
        if user_id:
            user_history =ChatMessage(
                message=clean_txt,  # type: ignore
                response=response, # type: ignore
                user_id=user_id # type: ignore
            )
            session.add(user_history)
            await session.commit()
            await session.refresh(user_history)
        return response

    def text_correction(self, text):
        txt = TextBlob(text)
        return txt.correct()
