from typing import List
import requests
from bs4 import BeautifulSoup
import jsonpickle
import re
import os

response = requests.get("http://menumenu.sk/blues/onas?_rf=hpr")
html_to_soup = BeautifulSoup(response.text, 'html.parser')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

class DayWrapper:
    def __init__(self):
        self.weekday = ""
        self.date = ""
        self.soup_of_the_day = ""

all_days = html_to_soup.find_all("div", class_="dmitem clr")
final_all_days: List[DayWrapper] = []

for day in all_days:
    current_day = DayWrapper()
    # Get info about the day
    current_day.weekday = day.find(class_="podnik-nazov").text.capitalize()
    current_day.date = day.find(class_="podnik-cenyod").text.replace("\xa0", " ")
    current_day.soup_of_the_day = day.find(class_="mm-polievky").find(class_="mm-foodwrapper").text.replace("\r","").replace("\n","")
    day_meals = day.find_all(class_="mmfood")
    for id, food in enumerate(day_meals, start=1):  
        day_meal_sanitized = food.text.replace('\xa0',' ')[:-9] 

        # Separate out allergens
        allergens = re.search(r"\(\d*(,*\d*)*\)", day_meal_sanitized)
        allergens_sanitized = ""
        if allergens is not None:
            day_meal_sanitized = day_meal_sanitized.removesuffix(allergens.group(0))
            allergens_sanitized = allergens.group(0)
        meal_price = food.find(class_="mm-cn")

        # Processing requires a flat JSON structure, no objects
        setattr(current_day, f"j{id}num", f'{id}.')
        setattr(current_day, f"j{id}", day_meal_sanitized.strip() )
        setattr(current_day, f"j{id}allergens", allergens_sanitized.strip() )
        setattr(current_day, f"j{id}veg", 'A' if id == 3 else "")
        setattr(current_day, f"j{id}price", meal_price.text.replace('\xa0',' ')[3:] )
        
    print(current_day.__dict__)
    final_all_days.append(current_day)

dir_path = os.getcwd()
new_file_path = os.path.join(dir_path, 'tyzden.json')

with open(new_file_path,"w", encoding='utf-8') as tyzden:
    tyzden.write(jsonpickle.encode(final_all_days, unpicklable=False, indent=4))
