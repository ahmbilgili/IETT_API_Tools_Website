# Displays general information about given bus line

import zeep
import json
import lxml.etree
from .utils import functions as helper_functions

translate_dict = {"HAT_KODU": "Line code", "HAT_ADI": "Line name", "TAM_HAT_ADI": "Complete line name", "HAT_DURUMU": "Line status", "BOLGE": "Region", "SEFER_SURESI": "One-way trip time"}
wsdl = "scripts/xml/durak_hat_bilgi.xml"

def take_line_code(line_code_input):
    line_code = helper_functions.special_char_upper_func(line_code_input)
    return line_code

def soap_call(line_code):
    client = zeep.Client(wsdl=wsdl)
    line_service_response = client.service.HatServisi_GYY(line_code) # returns lxml.etree._Element
    return line_service_response

def parse_etree(input_lxml_etree):
    outp_buffer = []
    for table in input_lxml_etree:
        outp_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))
    return outp_buffer

def main(line_code):
    try:
        line_code = take_line_code(line_code)
        line_service_response = soap_call(line_code)
        parsed_response = parse_etree(line_service_response)
        if len(parsed_response) == 0:
            raise Exception("No records found for the given line")
        return parsed_response
    except Exception as exc:
        return exc

if __name__ == "__main__":
    main() 