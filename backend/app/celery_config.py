# from celery import Celery
# from typing import Optional
# from flask import Flask


# class FlaskCelery:
#     def __init__(self, app:Optional[Flask]=None, **kwargs) -> None:
#         self.celery = None
#         self.options = kwargs

#         if app:
#             self.init_app(app, **kwargs)

#     def init_app(self, app: Flask):
#         self.celery = Celery(
#             app,
#             kwargs=self.options
#         )