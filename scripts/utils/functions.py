import time
import datetime
import random
import base64
from captcha.image import ImageCaptcha

# to convert some of the turkish lowercase characters to their corresponding upper case pairs
def special_char_upper_func(param):
    special_chars = {"ğ":"Ğ", "ü":"Ü", "i":"İ", "ş":"Ş", "ö":"Ö", "ç":"Ç"}
    for key, value in special_chars.items():
        param = param.replace(key, value)
    return param.upper()

# converts given input to ms
# Example: /DateTime(number)/, extracts number
def ms_parser(line):
    startidx = -1
    endidx = -1

    for i in range(len(line)):
        if (line[i] == '('):
            startidx = i
        elif (line[i] == ')'):
            endidx = i
    date_to_ms = int(line[startidx+1:endidx])
    return date_to_ms

# Converts the dictionary elements in given list to a string format.
def convert_list_tostr(announcement_list):
    out_string = ""
    for element in announcement_list:
        for key, value in element.items():
            out_string += f"{key}: {value}\n"
        out_string += "\n"
    return out_string

# For translating key(s) in dictionary and adding (translated_key, value) pair to a new dictionary
def parse_and_translate_values_dict(translate_dict, buffer):
    temp_dict = {}
    for key, value in buffer.items():
        try:
            temp_dict[translate_dict[key]] = value
        except:
            temp_dict[key] = value
    return temp_dict

def parse_and_translate_values_etree(translate_dict, buffer):
    temp_dict = {}
    for element in buffer:
        try:
            temp_dict[translate_dict[element.tag]] = element.text
        except:
            temp_dict[element.tag] = element.text
    return temp_dict

# Prints results. buffer is a list of dictionaries.
def print_result(buffer):
    for element in buffer:
        for key, value in element.items():
            print(f"{key}: {value}")
        print()

# Checks if date_input is of type YYYY-MM-DD
def validate_date_input(date_val):
    date_val_list = date_val.split("-")

    if len(date_val_list) != 3:
        raise ValueError("Incorrect format")    
    elif int(date_val_list[0]) < 2019:
        raise ValueError("Year cannot be less than 2019")
    elif int(date_val_list[1]) < 1 or int(date_val_list[1]) > 12:
        raise ValueError("Invalid month")
    elif int(date_val_list[2]) < 1 or int(date_val_list[2]) > 31:
        raise ValueError("Invalid day")
    return True

def validate_line_code(line_code):
    if line_code == "":
        raise ValueError("Incorrect line code")
    
# Converts date (in str format, YYYY-MM-DD) to YYYYMMDD format
def convert_date_to_yyyymmdd(date_input):
    date_input = date_input.split("-")
    converted_str = str(date_input[0]) + str(date_input[1]) + str(date_input[2])
    # print(converted_str)
    return converted_str

def generate_captcha():
    image = ImageCaptcha()
    code = ""
    for i in range(4):
        character_type = random.randint(0, 1)
        if character_type == 0:
            code += chr(random.randint(97, 122))
        else:
            code += chr(random.randint(48, 57))
    base64_captcha = base64.b64encode(image.generate(code, bg_color=(255, 255, 255)).getvalue()).decode("utf-8")
    return code, base64_captcha

'''
def timer(sec, mutex):
    mutex.acquire()
    start = time.time()
    while (time.time() - start < sec):
        pass
    mutex.release()
'''