from dotenv import load_dotenv
import os

if os.getenv("IN_PROD"):
    load_dotenv(dotenv_path="prod.env")
    print("loading prod config")
elif os.getenv("IN_TEST_CLOUD"):
    load_dotenv(dotenv_path="../dev_cloudtest.env")
    print("loading cloud test config")
else:
    load_dotenv(dotenv_path="../dev_localtest.env")
    print("loading local test config")

class Config:
    SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")