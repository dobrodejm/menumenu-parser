import requests
from bs4 import BeautifulSoup
import jsonpickle
import re
import os

html = requests.get("http://menumenu.sk/blues/onas?_rf=hpr")
html_to_soup = BeautifulSoup(html.text, 'html.parser')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

class Day_Wrapper:
    weekday = ""
    date = ""
    soup_of_the_day = ""


all_days = html_to_soup.find_all("div", class_="dmitem clr")
final_all_days = []

for day in all_days:
    current_day = Day_Wrapper()
    # Get info about the day
    current_day.weekday = day.find(class_="podnik-nazov").text.capitalize()
    current_day.date = day.find(class_="podnik-cenyod").text.replace("\xa0", " ")
    current_day.soup_of_the_day = day.find(class_="mm-polievky").find(class_="mm-foodwrapper").text.replace("\r","").replace("\n","")
    # Check if it's a holiday
    current_day.holiday = False
    if current_day.holiday == False:
        day_meals = day.find_all(class_="mmfood")
        for id, food in enumerate(day_meals, 1 ):  
            day_meal_sanitized = food.text.replace('\xa0',' ')[:-9]

            # Separate out allergens
            allergens = re.search(r"\(\d*(,*\d*)*\)", day_meal_sanitized)
            allergens_sanitized = ""
            if allergens is not None:
                day_meal_sanitized = day_meal_sanitized.removesuffix(allergens.group(0))
                allergens_sanitized = allergens.group(0)
            exec(f"current_day.m{id}price = '{id}.'")
            # Usually, #3 is a vegetarian option, adds the letter "A" ->
            # replaced by a vegetarian symbol during later processing (not in this script)
            if id == 3:
                exec(f"current_day.m{id}veg = 'A'")
            exec(f"current_day.m{id} = day_meal_sanitized")
            exec(f"current_day.m{id}allergens = allergens_sanitized + ' '")

            # Get the meal price
            meal_price = food.find(class_="mm-cn")
            exec(f"current_day.m{id}price = meal_price.text.replace('\xa0',' ')[3:]")
        
    print(current_day.__dict__)
    final_all_days.append(current_day)

dir_path = os.getcwd()
new_file_path = os.path.join(dir_path, 'tyzden.json')

with open(new_file_path,"w", encoding='utf-8') as tyzden:
    tyzden.write(jsonpickle.encode(final_all_days, unpicklable=False, indent=4))
