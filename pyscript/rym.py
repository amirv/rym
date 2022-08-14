#!/usr/bin/python

import requests
import pickle
import logging
import contextlib
from http.client import HTTPConnection
from pathlib import Path
import json

home = str(Path.home())

COOKIES_FILE = f"{Path.home()}/.rym.cookies"
SECRETS_FILE = f"{Path.home()}/.rym.secrets"

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.7,he;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://rym-pro.com/',
        'Content-Type': 'application/json',
        'x-app-id': '3a869241-d476-40f6-a923-d789d63db11d',
        'Origin': 'https://rym-pro.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'TE': 'trailers',
        }

def do_auth(s):
    with open(SECRETS_FILE, "r") as f:
        cred = json.load(f)

    r = s.post('https://api.city-mind.com/consumer/login', headers=headers, json=data)
    print(f"Login response: {r.text}")

    token = r.json()["token"]

    with open(COOKIES_FILE, 'wb') as f:
        pickle.dump((s.cookies, token), f)

    return token

def get_readings(s, token):
    headers["x-access-token"] = token

    url = "https://api-ctm.city-mind.com"
    path = "consumption/last-read"

    r = s.get(f"{url}/{path}", headers=headers)
    
    print(r.text)

    return r.json()[0]['read']


with requests.Session() as s:
    try:
        with open(COOKIES_FILE, 'rb') as f:
            cj, token = pickle.load(f)
            s.cookies.update(cj)
    except FileNotFoundError:
        token = do_auth(s)

    try:
        readings = get_readings(s, token)
    except Exception:
        print("Failed getting readings - trying a new token")
        token = do_auth(s)
        readings = get_readings(s, token)


    print(f"Reading: {readings}")
