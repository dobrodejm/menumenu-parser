# menumenu-parser
A python parser developed for myself, parsing the slovak [menumenu.sk](https://menumenu.sk) website. Working on the weekly menu pdfs for one of the restuarants listed there, I made this script whose output is read by the Data Merge functionality of Affinity Publisher to automatically insert the text.
This cut down the weekly processing time from 30-40 minutes down to between 5 and 10.

## To run this code
This repo is setup to work with the Anaconda package manager for python. I used miniconda which should do the trick. To initialize this project's packages, run  
`conda activate menumenu`  
inside this project's root folder. Afterwards, you should be able to just run the main file.
Modify the URL in the script to whichever restaurant you want to fetch menus for.  
run `python main.py` in the project's root to launch the script.

## Potential downside:  
If the site owners at menumenu decide to change the DOM structure, the script breaks. The script was created and tested 28 - November - 2021.  
Still works March 2025 🎉

## Potential upgrades:
Script works just as expected, automating a boring manual process. 🤷‍♀️

## Time spent:
Roughly 10 hours to create the script, about an hour every few months to clean things up etc.

