from asyncio import sleep
import os
import praw
import database
from gtts import gTTS
from selenium import webdriver
import time
from optparse import OptionParser

from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import video

language = 'en'

CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    ) 

reddit = praw.Reddit(
    client_id="y2ypd4wXHnkZ9HGxSIZXaA",
    client_secret="cDrW2FTkHjbLr4cN5MlTZ0svddsSIw",
    user_agent="<console:YoutubeBotty:1.0>",
)

subreddit = reddit.subreddit(input("Enter a subreddit: "))

count = 0

for post in subreddit.hot(limit=1):
    if database.check_if_post_exists(post.id):
        print("Post already exists.")
        continue
    else:
        # Check if the directory exists
        if not os.path.exists("/home/thomas/redditYoutubeBot/posts"):
            os.system("mkdir /home/thomas/redditYoutubeBot/posts")
        if not os.path.exists("/home/thomas/reddit_bot/posts/" + post.id):
            os.system("mkdir /home/thomas/redditYoutubeBot/posts/" + post.id)
            os.system("mkdir /home/thomas/redditYoutubeBot/posts/" + post.id + "/main")
            os.system("mkdir /home/thomas/redditYoutubeBot/posts/" + post.id + "/comments")
        else:
            print("Directory already exists.")
            continue
        # print("Making directory for post: " + post.id, end="")
        # sleep(1)
        # print(".", end="")
        # sleep(1)
        # print(".", end="")
        # sleep(1)
        text = post.title
        # tidy up the text to make it easier to process
        text = misc.tidy_up_text(text)
        audio = gTTS(text=text, lang=language)
        audio.save(f"/home/thomas/redditYoutubeBot/posts/{post.id}/main/audio_title_{post.id}.mp3")
        if post.selftext:
            text = post.selftext
            audio = gTTS(text=text, lang=language)
            audio.save(f"/home/thomas/redditYoutubeBot/posts/{post.id}/main/audio_selftext_{post.id}.mp3")
        # Now get screenshot of head of post from the url
        # and save it to a file using chrome.
        driver.get(post.url)
        # Accept the cookies
        # driver.find_element(By.XPATH, '//button[@id="js-accept-button"]').click()
        # Now select part of the page to screenshot.
        driver.find_element(by=By.XPATH, value=f'//div[@id="t3_{post.id}"]').screenshot(f"posts/{post.id}/main/screenshot_{post.id}.png")

        count += 1
        database.add_post(post.id)
        print(f"Added post {count}.")
        print(f"Post ID: {post.id}")
        print(f"Post title: {post.title}")
        print(f"Post URL: {post.url}")
        print("")
        
        comments = []
        # Now add top comments to an array
        rangeRepeat = 3
        if len(post.comments) < 3:
            rangeRepeat = len(post.comments)-1
        for i in range(0, rangeRepeat):
            print(f"Comment ID: {post.comments[i]}")
            print(f"Comment text: {post.comments[i].body}")
            print("")
            text = post.comments[i].body
            audio = gTTS(text=text, lang=language)
            audio.save(f"/home/thomas/redditYoutubeBot/posts/{post.id}/comments/{post.comments[i].id}_audio.mp3")
            driver.find_element(by=By.ID, value=f't1_{post.comments[i]}').screenshot(f"/home/thomas/redditYoutubeBot/posts/{post.id}/comments/{post.comments[i].id}_screenshot.png")

        video.generate_video(post.id)