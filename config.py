from dotenv import load_dotenv
import os
IN_PROD = os.getenv("IN_PROD")

if IN_PROD:
    load_dotenv(dotenv_path="/app/prod.env")
    print("were in prod")
else:
    load_dotenv(dotenv_path="../dev.env")
    print("were in dev")

class Config:
    SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")