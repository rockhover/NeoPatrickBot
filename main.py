
from itertools import islice

import fbchat
from fbchat import Client
from fbchat.models import *
import requests
import shutil

email = ""
password = ""
target_id = ""

thread_id = "6566850490051694"
thread_type = ThreadType.GROUP

class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        print("pingas")
        atts = message_object.attachments
        if len(atts) != 0 and isinstance(atts[0], fbchat.ImageAttachment):
            print("fat penguin")
            img_url = self.fetchImageUrl(atts[0].uid)
            r = requests.get(img_url, stream=True)
            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                # filename = img_url.split("/")[-1]
                # Open a local file with wb ( write binary ) permission.
                with open("stored_images/penguin.jpg", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                print('Image successfully Downloaded')
            else:
                print('Image Couldn\'t be retrieved')


def parseLogin():
    with open("personal_data.txt", "r") as f:
        login = f.readlines()
    global email
    email = login[0].strip()
    global password
    password = login[1].strip()

def main():

    client = EchoBot(email, password)
    client.listen()
    client.logout()

if __name__ == '__main__':
    parseLogin()
    main()
