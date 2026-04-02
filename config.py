from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="../dev_cloudtest.env")


class Config:
    SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")