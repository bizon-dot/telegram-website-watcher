import telegram
import requests
import logging
import json
from threading import Thread

logging.basicConfig(filename='site-automotive.log', filemode='a', format='%(asctime)s - %(message)s')

def send_message(bot, chat_id, text):
    """Sends a message to the specified Telegram chat."""
    bot.send_message(chat_id=chat_id, text=text)

def check_website(bot, url):
    """Sends a request to the specified URL and logs the status code."""
    statuses = {
        200: "Website Available",
        301: "Permanent Redirect",
        302: "Temporary Redirect",
        404: "Not Found",
        500: "Internal Server Error",
        503: "Service Unavailable"
    }
    try:
        web_response = requests.get(url)
        logging.warning(url + " " + str(web_response.status_code) + " " + statuses[web_response.status_code])
        if web_response.status_code != 200:
            message = url + " " + str(web_response.status_code) + " " + statuses[web_response.status_code]
            thread = Thread(target=send_message, args=(bot, "CHATID", message))
            thread.start()
        print(url, statuses[web_response.status_code])
    except:
        logging.exception(url + " " + "Website Not Available")
        message = url + " " + "Website Not Available"
        thread = Thread(target=send_message, args=(bot, "CHATID", message))
        thread.start()

def main():
    # Create a Telegram bot and a session object
    bot = telegram.Bot(token="TOKEN)
    session = requests.Session()

    # Read the automotive sites from the JSON file
    with open("automotive-sites.json") as f:
        automotive_sites = json.load(f)

    # Check the status of each website
    for url in automotive_sites["automotive_websites"]:
        check_website(bot, url)

if __name__ == "__main__":
    main()
