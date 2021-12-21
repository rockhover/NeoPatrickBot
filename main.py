import fbchat
from fbchat import Client
from fbchat.models import *
from dotenv import load_dotenv
from PIL import Image
import deeppyer
import asyncio
import os
import requests
import shutil

load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
target_name = "Patrick Day"
# patrick's ID is the default
target_id = "100003820518842"

pat = Image.open('stored_images/patwave.png')

# Neo Kino Chat
thrd_id = "2238564959531921"

# test group chat
# thrd_id = "6566850490051694"
thread_type = ThreadType.GROUP

async def fry(path):
    img = Image.open(path)
    img = await deeppyer.deepfry(img, flares=True)
    # pasting patrick onto the picture
    global pat
    ratio = min((img.size[0] / 2) / pat.size[0], (img.size[1] / 2) / pat.size[1])
    new_height = ratio * pat.size[1]
    new_width = ratio * pat.size[0]
    pat = pat.resize((int(new_width), int(new_height)))
    img.paste(pat, (0, int(img.size[1]) - int(new_height)), pat)
    img.save('stored_images/merge.jpg')


class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        print("pingas")
        atts = message_object.attachments
        if thread_id == thrd_id and len(atts) != 0 and isinstance(atts[0], fbchat.ImageAttachment) and author_id != self.uid:
            # img_url = self.fetchImageUrl(atts[0].uid)
            img_url = atts[0].large_preview_url
            print(img_url)
            r = requests.get(img_url, stream=True)
            print(int(r.headers['Content-Length']))
            # Check if the image was retrieved successfully
            if r.status_code == 200: # and int(r.headers['Content-Length']) < 1000000:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                # filename = img_url.split("/")[-1]
                # Open a local file with wb ( write binary ) permission.
                with open("stored_images/penguin.jpg", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                print('[Image Successfully Downloaded]')

                loop = asyncio.get_event_loop()
                loop.run_until_complete(fry("stored_images/penguin.jpg"))

                print('[Image Fried and Shopped]')

                self.sendLocalImage('stored_images/merge.jpg', thread_id=thrd_id, thread_type=thread_type)
                print('[Image Sent]')
            else:
                print('{Image Couldn\'t be retrieved}')


def main():
    client = EchoBot(email, password)
    client.listen()
    client.logout()


def find_id_by_name():
    client = Client(email, password)
    # Fetches a list of all users you're currently chatting with, as `User` objects
    return client.searchForUsers(target_name)[0].uid

if __name__ == '__main__':
    # find_id_by_name()
    main()
