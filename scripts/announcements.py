# Lists announcements for the given bus line
# If you cannot recover from an exception, no need to catch it.

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
    announcements_response = client.service.GetDuyurular_json()

    if len(announcements_response) == 0:
        raise Exception("No announcements found!")

    return announcements_response

def soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_specific_bus_lines_announcements(line_code, announcement_list):
    output_buffer = []
    for element in announcement_list:
        if line_code in element["HATKODU"]:
            output_buffer.append(helper_functions.parse_and_translate_values_dict(translate_dict, element))
    return output_buffer

def main(line_code):
    global COOLDOWN_SEC
    format_line_code(line_code)
    announcements_response = soap_call()
    announcements_response_list = soap_response_to_list(announcements_response)
    specific_announcements = get_specific_bus_lines_announcements(line_code, announcements_response_list)
    if len(specific_announcements) == 0:
        raise Exception("No announcments found!")
    # helper_functions.print_result(specific_announcements)
    return specific_announcements

if __name__ == "__main__":
    main()