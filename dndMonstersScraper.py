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
		monster_details_on_page = parse_monster_details(bs4.BeautifulSoup(html, 'html.parser'))
		monster_details_on_page["name"] = monster
		return monster_details_on_page

def parse_monster_details(html_soup): 
	final_monster_details = {}
	monster_data = html_soup.find_all("div", {"class": "col-xs-12 col-md-6"})
	print(len(monster_data))
	return final_monster_details


if __name__ == "__main__":
	html = urllib.urlopen("http://www.orcpub.com/dungeons-and-dragons/5th-edition/monsters")
	monster_manual = get_monster_list(bs4.BeautifulSoup(html, 'html.parser'))
	monster_manual = parse_monster_data(monster_manual[0:1])
	monster_directory = make_monsters_dataFrame(monster_manual)
	
	#print(monster_directory)
	all_monster_details = get_all_monster_details(monster_directory["name"])
	print(all_monster_details)




