
from itertools import islice
from fbchat import Client
from fbchat.models import *

email = ""
password = ""


thread_id = "1234567890"
thread_type = ThreadType.GROUP

def main():

    client = Client(email, password)

    print("Own id: {}".format(client.uid))

    # Print image url for 20 last images from thread.
    images = client.fetchThreadImages(thread_id)
    for image in islice(images, 20):
        print(image.large_preview_url)


    client.logout()

if __name__ == '__main__':
    print("Pingas")
