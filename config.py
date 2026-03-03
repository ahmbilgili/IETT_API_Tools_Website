from dotenv import load_dotenv
import os
DEV_ENV = False

if DEV_ENV:
    load_dotenv(dotenv_path="../config.env")
    CERT_PATH = "/certs"
else:
    load_dotenv(dotenv_path="./config.env")
    CERT_PATH = "./certs"

class Config:
    SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")