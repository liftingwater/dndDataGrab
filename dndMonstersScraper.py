import bs4
import urllib
import pandas as pd
import re

#Get a list of monsters on the main page: http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters
#Takes a urllib.urlopen object
def get_monster_list(html_soup): 
	monsters_html = []
	#uses the 'find_all' method to get data
	all_monsters_on_page = html_soup.find_all("div", {"class": "lv-title p-t-10"})
	for monster in all_monsters_on_page:
		monsters_html.append(monster)
	return monsters_html

#Get name, size, type, alignment and challenge rating from main page 
def parse_monster_data(monsters): 
	monster_data = []
	for monster in monsters: 
		#print monster
		data = {
			"name" : re.sub('<[^>]+>', '', str(monster.find_all("strong", {"itemprop": "name"})[0])), 
			"size" : re.sub('<[^>]+>', '', str(monster.find_all("em")[0])), 
			"type" : re.sub('<[^>]+>', '', str(monster.find_all("em")[1])), 
			"alignment" : re.sub('<[^>]+>', '', str(monster.find_all("em")[2])), 
			"challenge" : re.sub('<[^>]+>|CR |\[|\]', '', str(monster.find_all("strong",  {"class" : "m-l-10"})))
		}
		monster_data.append(data)
	return monster_data

#Convert the main page data to a data frame
def make_monsters_dataFrame(monsters):
	data = pd.DataFrame(monsters, columns = ['name', 'type', 'size', 'alignment', 'challenge'])
	return data

def make_monster_details_dataFrame(monsters): 
	data = pd.DataFrame(monsters, columns = ["name", "size", "type", "alignment", "armor class", "hit points", "speed", "str", "dex", "con", "int", "wis", "cha", "proficiency bonus", "saving throws", "skills", "damage vulnerabilities", "damage resistances", "damage immunities", "condition immunities", "senses", "languages", "challenge"])
	return data

#Take the monster directory and visit the page for each monster in it
def get_all_monster_details(monsters): 
	total_monster_details_list = []
	for monster in monsters: 
		#print(re.sub(' ', '-', monster.lower()))
		#print monster
		#Visit monster page
		monster = re.sub(',|\(|\)|\-|\/|\'', '', monster)
		print(re.sub(' ', '-', monster.lower()))
		html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters/" + re.sub(' ', '-', monster.lower()))
		#print("Now retrieving data from ")
		#print("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters/" + re.sub(' ', '-', monster.lower()))
		#monster_details_on_page = view_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		#This line of code calls the function to get the monster details for that specific monster
		monster_details_on_page = parse_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		monster_details_on_page["name"] = monster
		total_monster_details_list.append(monster_details_on_page)
	return total_monster_details_list

#Parse the monster details from each monster page 
def parse_monster_details(html_soup): 
	final_monster_details = {}
	monster_data_html = html_soup.find_all("div", {"class": "col-xs-12 col-md-6"})
	monster_data = list(monster_data_html)
	saved_monster_data_html = []
	final_monster_details["size"] = re.sub('<[^>]+>', '', str(monster_data_html[0].find_all("em")[0]))
	final_monster_details["type"] = re.sub('<[^>]+>', '', str(monster_data_html[0].find_all("em")[1]))
	final_monster_details["alignment"] = re.sub('<[^>]+>', '', str(monster_data_html[0].find_all("em")[3]))
	property_names = []
	property_values = []
	monster_stats = monster_data_html[0].find_all("div", {"class": "char-details-field"})
	for i in monster_stats:
		property_names = re.sub('<[^>]+>', '', str(i.find_all("h5")[0]))
		#print(property_names)
		property_values = re.sub('<[^>]+>', '', str(i.find_all("span")[0]))
		#print(property_values)
		final_monster_details[property_names.lower()] = property_values
	        
	#Code for collecting monster abilities scores
	monster_abilities = ["str", "dex", "con", "int", "wis", "cha"]
	abilities = monster_data_html[0].find_all("table")[0].find_all("div")
	for i in range(len(abilities)): 
		final_monster_details[monster_abilities[i]] = re.sub('<[^>]+>', '', str(abilities[i]))
	#print(final_monster_details)
	return final_monster_details

def view_monster_details(html_soup): 
	print "Test mode"
	monster_data_html = html_soup.find_all("div", {"class": "col-xs-12 col-md-6"})
	monster_data = list(monster_data_html)
	monster_actions = {}
	monster_lgnd_act = {}

	if len(monster_data_html[2].find_all("h4")) == 1: 
		data = monster_data_html[2].find_all("div")
		for i in data[0].find_all("p"): 
			monster_actions[re.sub('<[^>]+>', '', str(i.find_all("strong")))] = re.sub('<[^>]+>', '', str(i.find_all("span")))

	else: 
		print "Legendary Creature"
		data = monster_data_html[2].find_all("div")
		for i in data[0].find_all("p"): 
			monster_actions[re.sub('<[^>]+>', '', str(i.find_all("strong")))] = re.sub('<[^>]+>', '', str(i.find_all("span")))
		print monster_actions
		for i in data[2].find_all("p"): 
			monster_lgnd_act[re.sub('<[^>]+>', '', str(i.find_all("strong"))) + '*'] = re.sub('<[^>]+>', '', str(i.find_all("span")))
		print monster_lgnd_act

	print monster_actions
	print monster_lgnd_act

	return monster_actions

if __name__ == "__main__":
	html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters")
	monster_manual = get_monster_list(bs4.BeautifulSoup(html, 'html.parser'))
	#Get a list of monsters on the main page: http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters
	#print monster_manual[88:93]
	#monster manual is a list of html code taken from parts of the website that 
	monster_manual = parse_monster_data(monster_manual)
	#parse the html code for the list of attributes. Monster manual becomes a dictionary of 
	#print monster_manual
	monster_directory = make_monsters_dataFrame(monster_manual)
	#monster_directory is a data frame
	
	#print("Printing Monster Directory")
	#print( monster_directory)
	all_monster_details = get_all_monster_details(monster_directory["name"])
	#for i in all_monster_details: 
		#print i,'\n'
	all_monster_details = make_monster_details_dataFrame(all_monster_details)
	#for key in all_monster_details:
		#print key+': '+str(all_monster_details[key])
