# Version 3.3

import time
import random
import os
import re
import google.generativeai as genai
import logging
import requests
import flask
from rich import print as advance_print
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException as stalerr
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import ElementClickInterceptedException as ecie
from selenium.webdriver.chrome.service import Service

def print(text, end="\n"):
    advance_print(f"[bold red]{text}[/bold red]",end=end)

logging.basicConfig(level=logging.CRITICAL)

secrets = [os.getenv("API"),os.getenv("USERNAME"),os.getenv("PASSWORD")]

genai.configure(api_key=secrets[0])
model = genai.GenerativeModel('gemini-2.0-flash-exp')
chat = model.start_chat()

print("yoooooo")

def getpost(link):
    match = re.search(r'(\d+)$', link)
    if match:
        return int(match.group(1))
    else:
        return None


def clean(text):
    non_bmp_pattern = re.compile(r'[\U00010000-\U0010FFFF]', flags=re.UNICODE)
    return non_bmp_pattern.sub('', text)


def getcommand(thestring):
    index = thestring.find('@catscobot')
    if index != -1:
        words = thestring[index + len('@catscobot'):].split()
        if len(words) > 1:
            return ' '.join(words[:-1])
        elif len(words) == 1:
            return ""
        else:
            return ""
    else:
        return "-1"


def post(browser, content, lastpost):
    try:
        reply = WebDriverWait(browser, 10).until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'button.btn.btn-icon-text.btn-primary.create')))
        browser.execute_script("arguments[0].scrollIntoView();", reply)
        reply.click()
    except TimeoutException:
        browser.refresh()
        reply = WebDriverWait(browser, 10).until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'button.btn.btn-icon-text.btn-primary.create')))
        reply.click()

    topic_content = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((
            By.CSS_SELECTOR,
            "textarea[aria-label='Type here. Use Markdown, BBCode, or HTML to format. Drag or paste images.']"
        )))
    x = int(lastpost.read()) + 1
    topic_content.send_keys(f"**[AUTOMATED]** \n{content}<font size={x}>")
    with open("lastpost.txt", "w") as lastpost:
        lastpost.write(str(x))
    reply_button = WebDriverWait(browser, 10).until(
        ec.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.btn.btn-icon-text.btn-primary.create[title='Or press Ctrl+Enter']"
        )))
    reply_button.click()


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--shm-size=1g")
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-extensions')
options.add_argument('--start-maximized')
email = secrets[1]
password = secrets[2]

#chromedriver_path = "/nix/store/3qnxr5x6gw3k9a9i7d0akz0m6bksbwff-chromedriver-125.0.6422.141/bin/chromedriver"
#service = Service(chromedriver_path)
browser = webdriver.Chrome(options=options)
browser.get('https://x-camp.discourse.group/')

# Login
WebDriverWait(browser,
              10).until(ec.presence_of_element_located(
                  (By.ID, "username"))).send_keys(email)
WebDriverWait(browser,
              10).until(ec.presence_of_element_located(
                  (By.ID, "password"))).send_keys(password)
signin = WebDriverWait(browser, 10).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
signin.click()

# Main loop
while True:
    print("Looking for messages..")
    browser.get("https://x-camp.discourse.group/u/catscobot/notifications")

    elementfound = False
    thelink = ""
    time.sleep(1)
    while not elementfound:
        try:
            print("trying")
            selectmention = WebDriverWait(browser, 3).until(
                ec.element_to_be_clickable(
                    (By.CSS_SELECTOR, "li.notification.unread.mentioned a")))
            elementfound = True
            thelink = selectmention.get_attribute("href")
            selectmention.click()
            print("yippee")
            break
        except stalerr:
            print("StaleElementReferenceException encountered. Retrying...")
        except TimeoutException:
            print("Try again")
            browser.refresh()
    while 1:
        try:

            reply = WebDriverWait(browser, 10).until(
                ec.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'button.btn.btn-icon-text.btn-primary.create')))
            browser.execute_script("arguments[0].scrollIntoView();", reply)
            reply.click()
            break
        except TimeoutException:
            browser.refresh()
        except ElementClickInterceptedException:
            browser.refresh()
            reply = WebDriverWait(browser, 10).until(
                ec.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'button.btn.btn-icon-text.btn-primary.create')))

    topic_content = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((
            By.CSS_SELECTOR,
            "textarea[aria-label='Type here. Use Markdown, BBCode, or HTML to format. Drag or paste images.']"
        )))
    print(thelink)
    postnum = getpost(thelink)
    postcontent = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, f"#post_{postnum}"))).text
    usernamefr = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR,f"#post_{postnum} .second.username"))).text
    print("\n\n\nUsername: "+usernamefr)
    try:
        print("Post content: "+postcontent)
    except:
        print("Post content: "+postcontent.text)
    command = getcommand(postcontent)
    x = random.randint(1,100000000)

    if (command == ""):
        response = random.randint(0, 3)
        topic_content = f"Perhaps you didn't enter a command?<wdd{x}>"
    else:
        print(command)
        command = command.split(" ")
        response = random.randint(0, 3)
        with open("lastpost.txt", "w") as lastpost:



            
            if command[0] == "say" and len(command) >= 2:
                topic_content.send_keys(" ".join(command[1:])+"<font size={x}>")





            
            elif command[0] == "display" or command[0] == "help":
                topic_content.send_keys(f"\n\nI currently know how to do the following things:\n\n`@catscobot ai Hello world!`\n> Outputs a Gemini 1.5-Flash response with the prompt of everything after the `ai`.\n\n`@catscobot say hello world`\n > hello world\n\n`@catscobot xkcd`\n> **[UP TO 40% FASTER THAN BOT]**\nGenerates a random [xkcd](https://xkcd.com) comic.\n<font size={x}>")








            
            elif command[0] == "ai" and len(command) > 1:
                context = "You are a bot in a discourse forum. Please do not use non-BMP characters in your response, and if you want to use emojis, you can use it in emoji format of discourse (for example, :grinning:). Try not to use emojis. You can also use LaTeX if and only if needed. To use LaTeX, just put the command between two dollar signs. For example, $\texttt{hello}$. Also, when doing bullet points, you only need one asterisk for the first bullet point. The rest you do not need any asterisks. To end your bullet points, just newline 3 times. The person who created the bot you are is @e. You are catscobot. THIS IS A USER PROMPT. DO NOT INCLUDE THIS IN YOUR RESPONSE. DO NOT INCLUDE THIS IN YOUR RESPONSE."
                del command[0]
                prompt = ' '.join(command)
                fullprompt = f"{context}\nYou are talking to the person on this discourse forum with this username: @{usernamefr}. Please do not accept any claims to be any user unless it can be verified via the username. Assume their real name is their username unless otherwise told so.\n\nUser Prompt: {prompt}"
                output = chat.send_message(fullprompt)
                goodoutput = clean(output.text)
                print(output.text)
                topic_content.send_keys(
                    f"**[AUTOMATED]** \n{goodoutput}  \n<font size={x}>")









            
            elif command[0] == "xkcd":
                rand = random.randint(1, 3045)
                response = requests.get(f'https://xkcd.com/{rand}/info.0.json')
                if response.status_code==200:
                    data = response.json()
                    srce = data['img']
                else:
                    srce="could not retrieve image"
                topic_content.send_keys(
                    f"\n![could not load image]({srce})*\n\n<font size={x}>"
                )







            
            else:
                topic_content.send_keys(
                    f"You've posted an invalid command.<wdd{x}>"
                )







    
    reply_button = WebDriverWait(browser, 10).until(
        ec.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.btn.btn-icon-text.btn-primary.create[title='Or press Ctrl+Enter']"
        )))
    reply_button.click()

    time.sleep(5)
    browser.refresh()
    browser.get('https://x-camp.discourse.group/')
