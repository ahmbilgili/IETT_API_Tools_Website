# Displays scheduled departure hours of given bus line on given weekdays and given direction

from zeep import Client, Settings
import json
import sys
from .utils import functions as helper_functions
from . import line_service

translate_dict = {"SHATKODU": "Line code", "HATADI": "Line name", "SGUZERAH": "Route", "SYON": "Direction", 
                  "SGUNTIPI": "Day type", "GUZERGAH_ISARETI": "Route sign", "SSERVISTIPI": "Service type", "DT": "Time information"}

wsdl = "scripts/xml/PlanlananSeferSaati.asmx.xml"

def validate_and_format_line_code_day(line_code, day):
    line_code = helper_functions.special_char_upper_func(line_code)

    if line_code == "": # I am expecting a line_code, so its reasonable to place exception here.
        raise ValueError("Bus code cannot be left empty")
    
    day = day.upper()

    if day not in {"I", "C", "P"}:
        raise ValueError("Incorrect day choice")

    output_dict = {"Line_Code": line_code, "Day": day}
    return output_dict
    
def soap_call(input_line_code):
    client = Client(wsdl=wsdl)
    line_hours_response = client.service.GetPlanlananSeferSaati_json(input_line_code)

    if len(line_hours_response) == 2:
        raise Exception("Timetable not found, it's possible that bus line is incorrect")

    return line_hours_response

def convert_soap_response_to_list(soap_response_string):
    soap_response_list = json.loads(soap_response_string)
    return soap_response_list

def obtain_unique_bus_line_names(soap_response_list):
    bus_lines = []

    for element in soap_response_list:
        if element["HATADI"] not in bus_lines: # a bus line can have multiple bus names (endpoints can be different)
            bus_lines.append(element["HATADI"])
    
    return bus_lines

def print_bus_line_names(bus_lines):
    for element in bus_lines:
        print(element)

def convert_direction_to_G_D(line_info, direction):  
    if direction != "": 
        directions = line_info[0]["Line name"].split("-")
        # Assume line name = sabancı üni / kurtköy
        # 0 -> Sabancı Üni
        # 1 -> Kurtköy metro
        # G (Gidiş) -> Left to right, D (Dönüş)-> Right to left
        # if direction is kurtköy -> G (Gidiş) 
        # if direction is sabancı -> D (Dönüş)
        direction = direction.upper()
        if direction in directions[1]:
            return "G"
        elif direction in directions[0]:
            return "D"
        else:
            raise Exception("Invalid direction!")
    raise Exception("Invalid direction!")

def get_specific_timetables(soap_response_list, user_inputs):
    outp_buffer = []

    for element in soap_response_list:
        if element["SYON"] == user_inputs["Direction"] and element["SGUNTIPI"] == user_inputs["Day"]:
            outp_buffer.append(helper_functions.parse_and_translate_values_dict(translate_dict, element))

    if len(outp_buffer) == 0:
        # print("Unable to find timetable of queried bus line with given specifics")
        exit()
        
    return outp_buffer

def main(line_code, day, direction="", querying_for_line=False):
    try:
        if (querying_for_line):
            user_inputs = validate_and_format_line_code_day(line_code, day)
            line_info = line_service.main(line_code)
            return [line_info[0]["Line name"]]
        else:
            user_inputs = validate_and_format_line_code_day(line_code, day)

            line_info = line_service.main(line_code)

            user_inputs["Direction"] = convert_direction_to_G_D(line_info, direction)
        
            soap_response = soap_call(user_inputs["Line_Code"])

            soap_response_list = convert_soap_response_to_list(soap_response)

            unique_bus_line_names = obtain_unique_bus_line_names(soap_response_list)

            # print_bus_line_names(unique_bus_line_names)
                            
            timetables = get_specific_timetables(soap_response_list, user_inputs)
            
            return timetables
    except Exception as exc:
        return exc

if __name__ == "__main__":
    main()
