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
		html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters/" + re.sub(' ', '-', monster.lower()))
		#monster_details_on_page = view_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		monster_details_on_page = parse_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		monster_details_on_page["name"] = monster
	return monster_details_on_page

def parse_monster_details(html_soup): 
	final_monster_details = {}
	monster_data_html = html_soup.find_all("div", {"class": "col-xs-12 col-md-6"})
	monster_data = list(monster_data_html)
	data_keys = ["size", "type", "alignment", "armor class", "hit points", "speed", "proficiency bonus", "saving throws", "skills", "senses", "language", "challenge"]

	saved_monster_data_html = []

	#Get monster classifiers: Type, Alignment, and Size
	for i in [0, 1, 3]: 
		saved_monster_data_html.append(re.sub('<[^>]+>', '', str(monster_data_html[0].find_all("em")[i])))
	monster_stats = monster_data_html[0].find_all("div", {"class": "char-details-field"})

	#Code to get monster statistics(AC, HP, Speed, etc.)
	for i in monster_stats: 
		saved_monster_data_html.append(re.sub('<[^>]+>', '', str(i.find_all("span")[0])))
	for i in range(len(data_keys)):
		final_monster_details[data_keys[i]] = saved_monster_data_html[i]

	#Code for collecting monster abilities scores
	monster_abilities = ["str", "dex", "con", "int", "wis", "cha"]
	abilities = monster_data_html[0].find_all("table")[0].find_all("div")
	for i in range(len(abilities)): 
		final_monster_details[monster_abilities[i]] = re.sub('<[^>]+>', '', str(abilities[i]))	

	#final_monster_details["details"] = re.sub('<[^>]+>', '', str(list(monster_data[0])[4]))
	final_monster_details["details"] = {}

	monster_details = list(monster_data[0])[4].find_all("p")[1:]
	for i in monster_details: 
		detail_name = re.sub('<[^>]+>', '', str(i.find_all("strong")))
		detail_text = re.sub('<[^>]+>', '', str(i.find_all("span")))
		final_monster_details["details"][detail_name] = [detail_text]
	
	monster_actions = {}
	monster_lgnd_act = {}

	if len(monster_data_html[2].find_all("h4")) == 1: 
		data = monster_data_html[2].find_all("div")
		for i in data[0].find_all("p"): 
			monster_actions[re.sub('<[^>]+>', '', str(i.find_all("strong")))] = re.sub('<[^>]+>', '', str(i.find_all("span")))
	else: 
		data = monster_data_html[2].find_all("div")
		for i in data[0].find_all("p"): 
			monster_actions[re.sub('<[^>]+>', '', str(i.find_all("strong")))] = re.sub('<[^>]+>', '', str(i.find_all("span")))
		for i in data[2].find_all("p"): 
			monster_lgnd_act[re.sub('<[^>]+>', '', str(i.find_all("strong")))] = re.sub('<[^>]+>', '', str(i.find_all("span")))
		print '\n'

	final_monster_details["actions"] = monster_actions
	final_monster_details["lgnd_actions"] = monster_lgnd_act

	return final_monster_details

def view_monster_details(html_soup): 
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

	print ''

	print monster_actions
	print ''
	print monster_lgnd_act

	return monster_actions

if __name__ == "__main__":
	html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters")
	monster_manual = get_monster_list(bs4.BeautifulSoup(html, 'html.parser'))
	monster_manual = parse_monster_data(monster_manual[0:1])
	monster_directory = make_monsters_dataFrame(monster_manual)
	
	#print(monster_directory)
	all_monster_details = get_all_monster_details(monster_directory["name"])
	print(all_monster_details)


