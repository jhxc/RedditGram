### 
# github.com/jhxc
#
###
#Required dependencies

from pynput.keyboard import Key, Controller
from bs4 import BeautifulSoup
import requests
import urllib.request
import praw
from PIL import Image
from resizeimage import resizeimage

#allocates memory for using keyboard input as a controller
keyboard = Controller()

UNAME = "INSERTUSERNAMEHERE"
PASSWD = "INSERTPASSWORDHERE"
POSTCMD = "instapy -u %s -p %s -f %s -t %s"
TARGETSUBREDDIT = "INSERTSUBREDDITHERE"


def post(url, description):
    LINK = POSTCMD%(UNAME,PASSWD,url,description)
    keyboard.type(LINK)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter) 
 
def downloader(image_url,name):
    file_name = name
    full_file_name = str(file_name) + '.jpg'
    urllib.request.urlretrieve(image_url,full_file_name)
    
# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='my user agent', client_id ='INSERTID', client_secret='INSERTSECRET') 
submissions = r.subreddit(TARGETSUBREDDIT).hot(limit = 5)
for submission in submissions:
    if '[Discussion]' in submission.title:
        continue
    desc = submission.title.replace('[Image]', '')
    desc = desc.replace('[image]','')
    desc = desc.replace('[IMAGE]','')
    fixedDesc = "\"%s\""%(desc)
    fixedName = "\"%s\""%(desc)
    downloader(submission.url,desc)
    full_name = desc +'.jpg'
    
    with open(full_name, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_contain(image, [512, 512])
            rgb = cover.convert('RGB')
            rgb.save(full_name, image.format)

    post(fixedName+'.jpg',fixedDesc)


