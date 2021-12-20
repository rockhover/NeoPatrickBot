
from itertools import islice
from fbchat import Client
from fbchat.models import *

email = ""
password = ""
target_id = ""

thread_id = "6566850490051694"
thread_type = ThreadType.GROUP

def parseLogin():
    with open("personal_data.txt", "r") as f:
        login = f.readlines()
    global email
    email = login[0].strip()
    global password
    password = login[1].strip()

def main():

    client = Client(email, password)

    print("Own id: {}".format(client.uid))

    client.send(Message(text="Bot: Pingas"), thread_id=thread_id, thread_type=thread_type)

    client.logout()

if __name__ == '__main__':
    parseLogin()
    main()
