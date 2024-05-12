import sqlite3
import requests
import json

URL = "https://leak-lookup.com/api/search"
KEY = "f40da5b9297a2431c945d94d92ac7648"
TYPE = "email_address"
PATH = "info.json"
PATH2 = "Breach.sqlite"
PARAMETER = f"{input('საძიებო მეილი : ')}"
QUERY = f'key={KEY}&type={TYPE}&query={PARAMETER}'


def get_info(url, query=QUERY):
    response = requests.post(url, query)
    statuscode = response.status_code
    header = response.headers
    info = response.json()

    print(f'სტატუსის კოდი : {statuscode} ')
    print(f"თარიღი - {header['Date']}\n"
          f"კონტენტისა და სიმბოლოების ტიპი - {header['Content-Type']}")
    print(f"დატა გაჟონილია შემდეგი საიტებიდან :")
    for x in info['message']:
        print(x)

    return


def save_into_file(path, url, query=QUERY):
    data = requests.post(url, query).json()

    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def save_info_database(path2, url, query=QUERY):
    data = requests.post(url, query).json()

    conn = sqlite3.connect(path2)
    curr = conn.cursor()
    curr.execute('''CREATE TABLE if not exists Breaches (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           BreachFrom TEXT)''')

    for x in data['message']:
        curr.execute("INSERT INTO Breaches (BreachFrom) VALUES (?)", (x,))

    conn.commit()
    conn.close()
    return


def main():
    get_info(URL)
    save_into_file(PATH, URL)
    save_info_database(PATH2, URL)


main()
