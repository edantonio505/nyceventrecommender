from bs4 import BeautifulSoup
from datetime import datetime
import requests
import random
import re


# week days
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class Recommender():
    def __init__(self, today=True, json=False):
        self.today = today
        self.events = []
        self.json = json
        self.collect_events() 

    def collect_events(self):
        url = "https://theskint.com"
        r = requests.get(url)
        soup  = BeautifulSoup(r.content, 'html.parser')
        paragraphs = soup.find_all('p')
        current_day = ""
        todays_activites = []    

        for p in paragraphs:
            event = dict()
            # Get current day of the week
            if p.get_text().capitalize() in weekdays:
                current_day = p.get_text().capitalize()
                today = weekdays[datetime.today().weekday()]
                if current_day == today:
                    current_day = "Today"
            
            pa = str(p.contents[0])
            if "span" in pa:
                match = r'[ >]([0-9]*\/[0-9]* [0-9]*(am|pm)|[0-9]*(am|pm)-[0-9]*(am|pm)|[0-9]*-[0-9]*(am|pm)|[0-9]*:[0-9]*(am|pm)|[0-9]*\/[0-9]* [0-9]*:[0-9]*(am|pm)|[0-9]*(am|pm)|[0-9]*\/[0-9]*-[0-9]*|[0-9]*\/[0-9]*)[ :]'
                remove_date = r'([0-9]*\/[0-9]|[0-9]*\/[0-9]*)*(.+?)(am|pm|monthly\)|weekly\)|show|[0-9]):'
                regex = re.compile(match)
                prices_regex = re.compile(r'\$[0-9]*') 
                prices = prices_regex.findall(p.get_text()) 
                dateandtime = regex.findall(pa)
        
                if dateandtime: 
                    # parse event data
                    if len(prices) > 0: 
                        event["price"] = "-".join(prices)
                    elif "free" in p.get_text():
                        event["price"] = "free"
                    event["datetime"] = dateandtime[0][0] if "/" not in dateandtime[0][0] else "- " + str(dateandtime[0][0])
                    event["description"] = p.get_text().replace('>', '')
                    event['url'] = p.find('a').get('href') 
                    event['day'] = current_day
                    if event["day"] == "Today":
                        todays_activites.append(event)
                    self.events.append(event)
        if self.today:
            self.events = todays_activites




    def get_all_events(self):
        return self.events


    def just_choose_this(self):
        choice = random.choice(self.events)
        return choice 


    def get_recommendation(self):
        choice = self.just_choose_this() 
        if self.json:
            return choice
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
