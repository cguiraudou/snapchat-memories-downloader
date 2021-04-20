#!/usr/bin/python3

import json
import requests
import time
from datetime import datetime
from os import path, makedirs

start_time = time.time()

ok_count, err_count = 0, 0
dest_folder = "snapchat_data"
src_folder = "json/memories_history.json"

makedirs(dest_folder, exist_ok=True)

with open(src_folder, "r") as json_file:
    json_content = json.loads(json_file.read())

    for entry in json_content["Saved Media"]:
        try:
            geturl = requests.post(entry["Download Link"]) # Get file url
            media_url = geturl.text
            getfile = requests.get(media_url)

            file_date = datetime.strptime(entry["Date"], "%Y-%m-%d %H:%M:%S %Z")
            
            file_name = media_url.split("?")[0].split("/")[-1] # Get filename from url
            file_name_with_date = f"{file_date.year}_{file_date.month}_{file_date.day}_{file_name}"

            with open(path.join(dest_folder, file_name_with_date), "wb") as save_file:
                save_file.write(getfile.content)

            ok_count += 1
            
        except Exception as e:
            print("Error : couldn't get " + str(entry))
            print(e)
            err_count += 1

print(f"{err_count} errors, {ok_count} elements downloaded in {time.time() - start_time} seconds.")