#/usr/bin/env python3

import requests


def download(url):
    get_response = requests.get(url)
    file_name =url.split("/")[-1]
    with open("/root/Desktop/" + file_name, "wb") as out_file:
        out_file.write(get_response.content)

download("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYTxA3mlBC9TBWHoFUiGpuy-k-f7hYgwUouQ&usqp=CAU")
