from dotenv import load_dotenv
import os

if os.getenv("IN_PROD"):
    load_dotenv(dotenv_path="prod.env")
else:
    load_dotenv(dotenv_path="../dev_localtest.env")

class Config:
    SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")