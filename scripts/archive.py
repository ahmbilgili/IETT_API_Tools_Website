import lxml.etree
import zeep
import json
import os
import lxml
import datetime
from .utils import functions as helper_functions
from sshtunnel import SSHTunnelForwarder
import mysql.connector
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

translate_dict = {"ID": "Id", "NARSIVGOREVID": "Archive task ID", "NKAYITGUNU": "Action date", "SHATKODU": "Line code",
                  "SGUZERGAHKODU": "Route code", "SKAPINUMARA": "Door number", "DTBASLAMAZAMANI": "Mission start date", "DTBITISZAMANI": "Mission end date",
                  "SGOREVDURUM": "Mission status", "NGOREVID": "Mission ID", "DTPLANLANANBASLANGICZAMANI": "Planned mission start date", 
                  "DTDUZENLENENBASLANGICZAMANI": "Edited mission start date"}

def soap_call(date):
    client = zeep.Client(wsdl=wsdl)

    response = client.service.GetIettArsivGorev_XML(date)
    
    if len(response) == 0:
        raise Exception("No data found")

    return response
    
def parse_xml(body):
    output_buffer = []
    for table in body:
        if isinstance(table, lxml.etree._Element) == False:
            raise TypeError(f"Invalid type {type(table)} passed to parse_xml function")
        output_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))

    return output_buffer

def get_specific_bus_line_data(table_list, bus_line_code):
    bus_line_data = []
    if bus_line_code == "":
        return table_list
    else:
        for table in table_list:
            if bus_line_code == table["Line code"]:
                bus_line_data.append(table)
    return bus_line_data

def get_archive_records_from_DB(bus_line, date_val):
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
                cursor.execute("SELECT line_code, route_code, door_number, start_date, end_date, planned_start_date, edited_start_date FROM archive WHERE line_code = %s AND planned_start_date LIKE %s", [bus_line, f"%{date_val}%"])
                print("eee")
                return cursor.fetchall()
        except mysql.connector.errors.Error as err:
            raise Exception(err)

def main(date, bus_line):
    helper_functions.validate_date_input(date)
    helper_functions.validate_line_code(bus_line)

    # API Call expects date of format yyyy-mm-dd
    '''
    date = helper_functions.convert_date_to_yyyymmdd(date)
    '''
    
    '''
    response = soap_call(date)

    response_parsed = parse_xml(response)
    '''

    bus_line = helper_functions.special_char_upper_func(bus_line)

    '''
    specific_bus_line_data = get_specific_bus_line_data(response_parsed, bus_line)
    '''

    specific_bus_line_data = get_archive_records_from_DB(bus_line, date)

    if len(specific_bus_line_data) == 0:
        raise Exception("No logs found!")

    return specific_bus_line_data
    
if __name__ == "__main__":
    main()