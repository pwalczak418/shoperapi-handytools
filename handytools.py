# shoperapi-handytools v0.02 #

import tkinter as tk
from tkinter import ttk
from requests.auth import HTTPBasicAuth
import time
import requests
import config

global url # Complete URL for store's API

session_shoper = requests.Session()
session_shoper.headers.update({
    'User-Agent': 'shoperapi-handytools/0.02 (+https://github.com/pwalczak418/shoperapi-handytools)',
    "Content-Type": "application/json",
})

def login():
    global url
    url = entry_shpr_url.get()
    url = url if url.startswith("https://") else "https://" + url.replace("http://", "")
    url = url if url.endswith("/") else url + "/"
    url = url + "webapi/rest/"

    shpr_user = entry_shpr_user.get()
    shpr_pass = entry_shpr_pass.get()

    loginurl = url + "auth"
    response = session_shoper.post(loginurl, auth=HTTPBasicAuth(shpr_user, shpr_pass))
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        response_data = response.json()
        bearer_token = response_data['access_token']
        session_shoper.headers.update({
        'Authorization': 'Bearer ' + bearer_token
                        })
        print(f"Login was successful: {url}")
        button_login.destroy()
        label_login = ttk.Label(root, text=f"Logged in, Shoper URL: {url}")
        label_login.pack()
        create_menu()
    else:
        print(f"Login was unsuccessful, HTTP code: {response.status_code}")

def create_menu():
    delete_attributes_button = ttk.Button(root, text="Delete attributes and attribute groups", command=delete_attributes)
    delete_attributes_button.pack(pady=2)

    delete_option_groups_button = ttk.Button(root, text="Delete option groups", command=delete_option_groups)
    delete_option_groups_button.pack(pady=2)

######################################################################
#                              TOOLS                                 #
######################################################################

def delete_attributes(): # Up to 50 for this version
    att_url = url + "attributes"
    gr_att_url = url + "attribute-groups"
    response1 = session_shoper.get(att_url, params={"limit": 50})
    response2 = session_shoper.get(gr_att_url, params={"limit": 50})
    data1 = response1.json()
    data2 = response2.json()

    for item in data1["list"]:
        att_id = item["attribute_id"]
        session_shoper.delete(f"{att_url}/{att_id}")
        time.sleep(config.CRAWL_DELAY)

    for item in data2["list"]:
        gr_att_id = item["attribute_group_id"]
        json = {"categories":[]} # Categories must be deleted from the attribute group before the group can be deleted.
        session_shoper.put(f"{gr_att_url}/{gr_att_id}", json=json)
        time.sleep(config.CRAWL_DELAY)
        session_shoper.delete(f"{gr_att_url}/{gr_att_id}")
        time.sleep(config.CRAWL_DELAY)

def delete_option_groups(): # This will work if there are no connections with products
    option_groups_url = url + "option-groups"
    response = session_shoper.get(option_groups_url, params={"limit": 50})
    data = response.json()

    for item in data["list"]:
        option_group_id = item["group_id"]
        session_shoper.delete(f"{option_groups_url}/{option_group_id}")
        time.sleep(config.CRAWL_DELAY)

######################################################################
#                                UI                                  #
######################################################################

root = tk.Tk()
root.title("Handytools for Shoper API")
root.geometry("600x400")
root.resizable(False, False)
root.configure(bg="#0064b0")

style = ttk.Style()
style.configure("TLabel", background="#9cd4ff")

label_shpr_url = ttk.Label(root, text="Shoper URL:")
label_shpr_url.pack()
entry_shpr_url = ttk.Entry(root, width=30)
entry_shpr_url.insert(0, f"{config.DEFAULT_SHOP_URL}") 
entry_shpr_url.pack()

label_shpr_user = ttk.Label(root, text="API user:")
label_shpr_user.pack()
entry_shpr_user = ttk.Entry(root, width=30)
entry_shpr_user.insert(0, f"{config.DEFAULT_API_USER}") 
entry_shpr_user.pack()

label_shpr_pass = ttk.Label(root, text="Password:")
label_shpr_pass.pack()
entry_shpr_pass = ttk.Entry(root, width=30, show="*")
entry_shpr_pass.insert(0, f"{config.DEFAULT_API_PASSWORD}") 
entry_shpr_pass.pack()

label_shpr_locale = ttk.Label(root, text="Chosen Locale:")
label_shpr_locale.pack()
entry_shpr_locale = ttk.Entry(root, width=30)
entry_shpr_locale.insert(0, f"{config.DEFAULT_LOCALE}") 
entry_shpr_locale.pack()

button_login = ttk.Button(root, text="Login", command=login)
button_login.pack(pady=2)

root.mainloop()