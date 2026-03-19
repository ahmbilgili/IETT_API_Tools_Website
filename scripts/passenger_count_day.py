# Outputs the top 50 bus lines with highest number of travels for the given date
# If the user asks for a specific bus line, (considering it's in top 50), only information regarding that bus line is displayed instead.

# Calls the mariaDB database to fetch records instead of sending a request to SOAP API
# For fetching results from the server, check passenger_count_day_SOAP_caller.py

import zeep
import json
from datetime import date, timedelta
from .utils import functions as helper_functions
import mysql.connector
import boto3
from dotenv import load_dotenv
import os
from sshtunnel import SSHTunnelForwarder

'''
if DEV_ENV:
    # Loads config file from parent dir
    load_dotenv(dotenv_path="../config.env")
else:
    # Loads config file from current dir (app)
    load_dotenv(dotenv_path="/app/config.env")
'''

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

translate_dict = {"Gun": "Day", "Hat": "Line", "Yolculuk": "Number of trips"}

# Converts ms to date by adding ms_input to epoch date (1970-01-01) 
def ms_to_date_converter(ms_input):
    return date.fromisoformat('1970-01-02') + timedelta(milliseconds=ms_input) # epoch + 1 + ms, API call returns values of previous day

'''
def soap_call(date_val):
    client = zeep.Client(wsdl=wsdl)
    response = client.service.GetIettYolculukHat_json(date_val)
    if len(response) == 2:
        raise Exception("No records found for the given date")
    return response

def convert_soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_data_of_buses(response_list):
    output_buffer = []
    for element in response_list:
         if isinstance(element["Hat"], str): # Don't add bus lines with bus line name "None"
            temp_dict = {}
            for key, value in element.items():
                # will not use parse_and_translate_values here, internal logic is different.
                try:
                    if key == "Gun":
                        date_to_ms = helper_functions.ms_parser(value)
                        curr_date_conversion = ms_to_date_converter(date_to_ms) 
                        value = curr_date_conversion
                    temp_dict[translate_dict[key]] = value
                except:
                    temp_dict[key] = value
            output_buffer.append(temp_dict)
    return output_buffer
'''

def get_passenger_counts_from_DB(date_val):
        try:
            with SSHTunnelForwarder(
                ssh_address_or_host=(os.getenv("SSH_TUNNEL_HOST"), 22),
                ssh_pkey=os.getenv("SSH_PKEY_PATH"),
                ssh_username=os.getenv("SSH_USERNAME"),
                remote_bind_address=(os.getenv("REMOTE_DB_ADDRESS"), int(os.getenv("REMOTE_DB_PORT"))),
                local_bind_address=("localhost", int(os.getenv("REMOTE_DB_PORT")))
            ) as ssh_tunnel:
                ssh_tunnel.start()
                connection = mysql.connector.connect(
                host="localhost",
                port=int(os.getenv("REMOTE_DB_PORT")),
                database='iett_website_db',
                user='viewer',
                password=os.getenv("MARIADB_VIEWER_PASSWORD"),
                ssl_disabled=False,
                ssl_ca= os.getenv("GLOBAL_CERT_PATH")
                )
                cursor = connection.cursor()
                date_val += " 00:00:00"
                cursor.execute("SELECT date, line, departure_count FROM departure_counts WHERE date=%s", [date_val])
                result = cursor.fetchall()
                return result
        except mysql.connector.errors.Error as err:
            raise Exception(err)

def main(date_val):
    helper_functions.validate_date_input(date_val)        

    '''
    soap_response = soap_call(date_val)

    soap_response_list = convert_soap_response_to_list(soap_response)

    bus_data = get_data_of_buses(soap_response_list)
    '''
    
    result = get_passenger_counts_from_DB(date_val)

    if len(result) == 0:
        raise Exception("No data found!")
    
    return result


if __name__ == "__main__":
    main()