# Lists announcments for the given bus line

import zeep
import json
import os
from .utils import functions as helper_functions
import threading
import sys

wsdl = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"

translate_dict = {"HATKODU": "Line Code", "HAT": "Line", "TIP": "Type", "GUNCELLEME_SAATI": "Update Time", "MESAJ": "Message"}

def format_line_code(line_code_input):
    line_code = helper_functions.special_char_upper_func(line_code_input)
    return line_code

def soap_call():
    client = zeep.Client(wsdl=wsdl)
    announcments_response = client.service.GetDuyurular_json()

    if len(announcments_response) == 0:
        raise Exception("No announcments found!")

    return announcments_response

def soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_specific_bus_lines_announcments(line_code, announcment_list):
    output_buffer = []
    for element in announcment_list:
        if line_code in element["HATKODU"]:
            output_buffer.append(helper_functions.parse_and_translate_values_dict(translate_dict, element))
    return output_buffer

def main(line_code):
    global COOLDOWN_SEC
    try:
        format_line_code(line_code)
        announcments_response = soap_call()
        announcments_response_list = soap_response_to_list(announcments_response)
        specific_announcments = get_specific_bus_lines_announcments(line_code, announcments_response_list)
        # helper_functions.print_result(specific_announcments)
        return specific_announcments
    except Exception as exc:
        return exc

if __name__ == "__main__":
    main()