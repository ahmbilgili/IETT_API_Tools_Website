# Outputs the top 50 bus lines with highest number of travels for the given date
# If the user asks for a specific bus line, (considering it's in top 50), only information regarding that bus line is displayed instead.

import zeep
import json
from datetime import date, timedelta
from .utils import functions as helper_functions

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

translate_dict = {"Gun": "Day", "Hat": "Line", "Yolculuk": "Number of trips"}

# Converts ms to date by adding ms_input to epoch date (1970-01-01) 
def ms_to_date_converter(ms_input):
    return date.fromisoformat('1970-01-02') + timedelta(milliseconds=ms_input) # epoch + 1 + ms, API call returns values of previous day

def soap_call(date_val):
    client = zeep.Client(wsdl=wsdl)
    response = client.service.GetIettYolculukHat_json(date_val)
    if len(response) == 2:
        raise Exception("No data for given date found!")
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

def main(date_val):
    try:
        helper_functions.validate_date_input(date_val)        
        
        soap_response = soap_call(date_val)

        soap_response_list = convert_soap_response_to_list(soap_response)

        bus_data = get_data_of_buses(soap_response_list)
        
        if len(bus_data) == 0:
            raise Exception("Number of trips not found for the specified bus line")
        
        return bus_data
    except Exception as exc:
        return exc

if __name__ == "__main__":
    main()