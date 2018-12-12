from bs4 import BeautifulSoup
import requests
import re
import random
import os




class Recommender():
    def __init__(self, today=True):
        self.today = today
        self.events = []
        self.collect_events() 


    def collect_events(self):
        url = "https://theskint.com"
        r = requests.get(url)
        soup  = BeautifulSoup(r.content, 'html.parser')
        paragraphs = soup.find_all('p')
        comingup = False

        for p in paragraphs:
            if "coming up" in p.get_text():
                comingup = True

            if comingup != self.today:
                pa = str(p.contents[0])
                if "span" in pa:
                    match = r'[ >]([0-9]*\/[0-9]* [0-9]*(am|pm)|[0-9]*(am|pm)-[0-9]*(am|pm)|[0-9]*-[0-9]*(am|pm)|[0-9]*:[0-9]*(am|pm)|[0-9]*\/[0-9]* [0-9]*:[0-9]*(am|pm)|[0-9]*(am|pm)|[0-9]*\/[0-9]*-[0-9]*|[0-9]*\/[0-9]*)[ :]'
                    remove_date = r'([0-9]*\/[0-9]|[0-9]*\/[0-9]*)*(.+?)(am|pm|monthly\)|weekly\)|show|[0-9]):'
                    regex = re.compile(match)
                    prices_regex = re.compile(r'\$[0-9]*') 
                    prices = prices_regex.findall(p.get_text()) 
                    dateandtime = regex.findall(pa)
                    event = dict()
                    if dateandtime:
                        if len(prices) > 0: 
                            event["price"] = "-".join(prices)
                        elif "free" in p.get_text():
                            event["price"] = "free"
                        event["datetime"] = dateandtime[0][0]
                        description = str(re.sub(remove_date, '', p.get_text())).replace('>', '')
                        event["description"] = description
                        event['url'] = p.find('a').get('href') 
                        self.events.append(event) 


    def get_all_events(self):
        return self.events


    def just_choose_this(self):
        choice = random.choice(self.events)
        return choice 


    def get_recommendation(self):
        choice = self.just_choose_this() 
        message = ""
        if 'price' in choice:
            message += "price: {}\n".format(choice['price'])
        datetimemessage = "time"
        if "/" in choice['datetime'] and 'pm' not in choice['datetime'] and 'am' not in choice['datetime']:
            datetimemessage = 'until'
        if "/" in choice['datetime'] and ('pm' in choice['datetime'] or 'am' in choice['datetime']):
            datetimemessage = 'date and time'
        message += "{}: {}\n".format(datetimemessage,choice['datetime'])
        message += "link: {}\n".format(choice['url'])
        message += "description: {}\n".format(choice['description'])
        return message
