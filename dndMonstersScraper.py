import bs4
import urllib
import pandas as pd
import re

def get_monster_list(html_soup): 
	monsters_html = []
	all_monsters_on_page = html_soup.find_all("div", {"class": "lv-title p-t-10"})
	for monster in all_monsters_on_page:
		monsters_html.append(monster)
	return monsters_html

def parse_monster_data(monsters): 
	monster_data = []
	for monster in monsters: 
		data = {
			"name" : re.sub('<[^>]+>', '', str(monster.find_all("strong", {"itemprop": "name"})[0])), 
			"size" : re.sub('<[^>]+>', '', str(monster.find_all("em")[0])), 
			"type" : re.sub('<[^>]+>', '', str(monster.find_all("em")[1])), 
			"alignment" : re.sub('<[^>]+>', '', str(monster.find_all("em")[2])), 
			"challenge" : re.sub('<[^>]+>|CR |\[|\]', '', str(monster.find_all("strong",  {"class" : "m-l-10"})))
		}

		monster_data.append(data)
	return monster_data

def make_monsters_dataFrame(monsters):
	data = pd.DataFrame(monsters, columns = ['name', 'type', 'size', 'alignment', 'challenge'])
	return data

def get_all_monster_details(monsters): 
	for monster in monsters: 
		html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters/" + monster.lower())
		#view_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		monster_details_on_page = parse_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		monster_details_on_page["name"] = monster
		return monster_details_on_page

def parse_monster_details(html_soup): 
	final_monster_details = {}
	monster_data = html_soup.find_all("div", {"class": "col-xs-12 col-md-6"})
	data_keys = ["size", "type", "alignment", "armor class", "hit points", "speed", "proficiency bonus", "saving throws", "skills", "senses", "language", "challenge"]

	saved_monster_data = []

	for i in [0, 1, 3]: 
		saved_monster_data.append(re.sub('<[^>]+>', '', str(monster_data[0].find_all("em")[i])))
	monster_stats = monster_data[0].find_all("div", {"class": "char-details-field"})

	for i in monster_stats: 
		saved_monster_data.append(re.sub('<[^>]+>', '', str(i.find_all("span")[0])))
	for i in range(len(data_keys)):
		final_monster_details[data_keys[i]] = saved_monster_data[i]

	monster_abilities = ["str", "dex", "con", "int", "wis", "cha"]
	abilities = monster_data[0].find_all("table")[0].find_all("div")
	for i in range(len(abilities)): 
		final_monster_details[monster_abilities[i]] = re.sub('<[^>]+>', '', str(abilities[i]))

	return final_monster_details

def view_monster_details(html_soup): 
	monster_data = html_soup.find_all("div", {"class": "col-xs-12 col-md-6"})
	print(monster_data)
	abilities = []
	print("\n +++++++++++++++++++++++++++++++++++++++++++++ \n")

	monster_stats = monster_data[0].find_all("table")[0].find_all("div")
	for i in monster_stats: 
		abilities.append(re.sub('<[^>]+>', '', str(i)))
	print(abilities)
	return {}


if __name__ == "__main__":
	html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters")
	monster_manual = get_monster_list(bs4.BeautifulSoup(html, 'html.parser'))
	monster_manual = parse_monster_data(monster_manual[0:1])
	monster_directory = make_monsters_dataFrame(monster_manual)
	
	#print(monster_directory)
	all_monster_details = get_all_monster_details(monster_directory["name"])
	print(all_monster_details)




