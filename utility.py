from requests import request
from termcolor import colored
from time import localtime

def download_or_read(file_name: str):
    result_list = []
    try:
        if file_name.startswith("http"):
            loaded_data = ""
            response = request("GET",file_name,timeout=5)
            if response.status_code == 200:
                loaded_data = response.text
            else:
                report(f"Unable to load from \"{file_name}\". Code: {response.status_code}","ERROR")
                return result_list
        else:
            with open(file_name, "r") as f:
                loaded_data = f.read()
    except Exception as e:
        report(f"Unable to load config file. Error: {e}","ERROR")
        return result_list
    if "\n" in loaded_data:
        result_list += loaded_data.split("\n")
    result_list = [line.strip("\r") for line in result_list if not line.startswith("#")]
    return result_list

def send_or_write(file_name: str,data: list):
    try:
        if file_name.startswith("http"):
            report("Unable send data recently.","ERROR")
        else:
            with open(file_name,"w") as f:
                for line in data:
                    f.write(line + "\n")
                report(f"{len(data)} lines were written to \"{file_name}\"","MAIN")
    except Exception as e:
        report(f"Unable to write data. Error: {e}","ERROR")


def report(message: str, type: str):
    time_stamp = localtime()
    time_str = " (" +str(time_stamp.tm_hour) + ":" + str(time_stamp.tm_min) + ":" + str(time_stamp.tm_sec) + ") "
    if type == "ERROR":
        print(colored(type + ":", "red") + time_str  + message)
    elif type == "MAIN":
        print(colored(type + ":", "green") + time_str + message)
    elif type == "SYSTEM":
        print(colored(type + ":", "blue") + time_str  + message)
    else:
        print(type + ":" + time_str + message)
