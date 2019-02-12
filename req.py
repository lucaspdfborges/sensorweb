import requests
import math
import time

rLogin = requests.post('http://127.0.0.1:8000/api-token-auth/',{'username': 'pessoa2', 'password': 'zxcvbnm1'})

URL = 'http://127.0.0.1:8000/api/v1/dashdata-view'

token = rLogin.json()['token']

rView = requests.get(URL, headers={'Authorization':'Bearer {}'.format(token)})

for i in range(200):
    time.sleep(1);

    rInsert = requests.post('http://127.0.0.1:8000/dashdata-insert/',{'experimento': 'sensor2', 'dado': 10*math.cos(math.pi*i/10)},headers={'Authorization':'Bearer {}'.format(token)})

    print(rInsert, end="")
    print(rInsert.json())
