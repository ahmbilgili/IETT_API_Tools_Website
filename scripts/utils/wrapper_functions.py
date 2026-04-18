import sys
import os
import mysql.connector
from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import Session
from sshtunnel import SSHTunnelForwarder

def insert_to_test_db(table, values):
    engine = create_engine(f"mysql+mysqlconnector://root:{os.getenv("MARIADB_ROOT_PASSWORD")}@{os.getenv("REMOTE_DB_ADDRESS")}:{os.getenv("REMOTE_DB_PORT")}/{os.getenv("DB_NAME")}", echo=True)
    with Session(engine) as session:  
        try:                  
            session.execute(
                insert(table).values(values)
            )
            session.commit()
            return True
        except Exception as exc:
            return exc
        

def insert_to_db(user, password, table, values):
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@127.0.0.1:3306/{os.getenv("DB_NAME")}", echo=True)
    with SSHTunnelForwarder(
    ssh_address_or_host=(os.getenv("SSH_TUNNEL_HOST"), 22),
    ssh_pkey=os.getenv("SSH_PKEY_PATH"),
    ssh_username=os.getenv("SSH_USERNAME"),
    remote_bind_address=(os.getenv("REMOTE_DB_ADDRESS"), int(os.getenv("REMOTE_DB_PORT"))),
    local_bind_address=("localhost", int(os.getenv("REMOTE_DB_PORT")))
    ) as ssh_tunnel:
        ssh_tunnel.start()
        with Session(engine) as session:  
            try:                  
                session.execute(
                    insert(table).values(values)
                )
                session.commit()
                return True
            except Exception as exc:
                return exc