import requests
from bs4 import BeautifulSoup
import jsonpickle
import re

html = requests.get("http://menumenu.sk/blues/onas?_rf=hpr")
soup = BeautifulSoup(html.text, 'html.parser')
jsonpickle.set_encoder_options('json', ensure_ascii=False)


class Den:
    weekday = ""
    sviatok = False
    datum = ""
    polievka = ""


all_days = soup.find_all("div", class_="dmitem clr")
final_all_days = []

for day in all_days:
    current_den = Den()
    # metadata ohladne dna
    current_den.weekday = day.find(class_="podnik-nazov").text.capitalize()
    current_den.datum = day.find(class_="podnik-cenyod").text.replace("\xa0", " ")
    current_den.polievka = day.find(class_="mm-polievky").find(class_="mm-foodwrapper").text.replace("\r","").replace("\n","")
    # check for Sviatok
    current_den.sviatok = False
    # pokracujeme 
    if current_den.sviatok == False:
        day_hj = day.find_all(class_="mmfood") # hj = hlavne jedlo
        for id, food in enumerate(day_hj, 1 ):  
            cleaned_food = food.text.replace('\xa0',' ')[:-9]
                        
            # Zisti a zapis alergeny
            alergeny = re.search(r"\(\d*(,*\d*)*\)", cleaned_food)
            final_alergeny = ""
            if alergeny is not None:
                cleaned_food = cleaned_food.removesuffix(alergeny.group(0))
                final_alergeny = alergeny.group(0)
            exec(f"current_den.j{id}cislo = '{id}.'")
            if id == 3:
                exec(f"current_den.j{id}veg = 'A'")
            exec(f"current_den.j{id} = cleaned_food")
            exec(f"current_den.j{id}a = final_alergeny + ' '")

            # Zisti a zapis cenu
            cena = food.find(class_="mm-cn")
            exec(f"current_den.j{id}c = cena.text.replace('\xa0',' ')[3:]")
        
    print(current_den.__dict__)
    final_all_days.append(current_den)

with open("C:\\Users\\rkas\\Desktop\\menumenu-parser\\tyzden.json","w", encoding='utf-8') as tyzden:
    tyzden.write(jsonpickle.encode(final_all_days, unpicklable=False, indent=4))
