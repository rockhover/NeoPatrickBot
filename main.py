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
target_id = ""

thread_id = "6566850490051694"
thread_type = ThreadType.GROUP

async def fry(path):
    img = Image.open(path)
    img = await deeppyer.deepfry(img)
    img.save('stored_images/fry.jpg')


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

                print('[Image Successfully Downloaded]')

                loop = asyncio.get_event_loop()
                loop.run_until_complete(fry("stored_images/penguin.jpg"))

                print('[Image Fried]')

                self.sendLocalImage('stored_images/fry.jpg', thread_id=thread_id, thread_type=thread_type)
                print('[Image Sent]')
            else:
                print('{Image Couldn\'t be retrieved}')


def main():
    client = EchoBot(email, password)
    client.listen()
    client.logout()

if __name__ == '__main__':
    main()
