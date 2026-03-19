import lxml.etree
import zeep
import json
import os
import lxml
import datetime
from .utils import functions as helper_functions

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

translate_dict = {"ID": "Id", "NARSIVGOREVID": "Archive task ID", "NKAYITGUNU": "Action date", "SHATKODU": "line_code",
                  "SGUZERGAHKODU": "route_code", "SKAPINUMARA": "door_number", "DTBASLAMAZAMANI": "start_date", "DTBITISZAMANI": "end_date",
                  "SGOREVDURUM": "Mission status", "NGOREVID": "Mission ID", "DTPLANLANANBASLANGICZAMANI": "planned_start_date", 
                  "DTDUZENLENENBASLANGICZAMANI": "edited_start_date"}

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

def main(date_val):
    # helper_functions.validate_date_input(date)

    # API Call expects date of format yyyy-mm-dd
    date_val = helper_functions.convert_date_to_yyyymmdd(date_val)

    response = soap_call(date_val)

    response_parsed = parse_xml(response)
    
    return response_parsed