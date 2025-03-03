
from textblob import TextBlob


from app.config import Config

config =Config() # type: ignore





def text_correction(text):
    txt = TextBlob(text)
    return txt.correct()


