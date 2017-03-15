import bs4
import urllib
import pandas as pd
import re

def test_spell_entry(row): 
	row_cells = row.find_all("td")
	try: 
		spell_name = row_cells[1].find_all("a")[0].text
	except: 
		pass
	
	if (len(row_cells) == 9 and spell_name): 
		return True
	else:
		return False

def get_all_spells(html_soup): 
	spells=[]
	all_rows_in_html_page = html_soup.find_all("tr")
	for row in all_rows_in_html_page: 
		if test_spell_entry(row): 
			row_cells = row.find_all("td")
			spell_entry = {
				"name": row_cells[1].find_all("a")[0].text, 
				"level": row_cells[2].text, 
				"school": row_cells[3].text, 
				"casting time": row_cells[4].text, 
				"ritual": row_cells[5].text, 
				"concentration": row_cells[6].text, 
				"classes": ' '.join((re.sub('[\n]', '', row_cells[7].text).strip(' ')).split()), 
				"source": row_cells[8].text
			}
			spells.append(spell_entry)
	return spells

def get_spell_details(html_soup): 
	all_details_on_page = html_soup.find_all("div", { "class" : "col-md-12" })
	details = {
		"name" : re.sub('<[^>]+>', '', str(list(all_details_on_page[0].find_all("span")[0]))),
		"level" : re.sub('<[^>]+>', '', str(all_details_on_page[0].find_all("p")[1].find_all("strong")[0])),
		"casting" : re.sub('<[^>]+>', '', str(all_details_on_page[0].find_all("p")[1].find_all("strong")[1])),
		"range" : re.sub('<[^>]+>', '', str(all_details_on_page[0].find_all("p")[1].find_all("strong")[2])),
		"componants" : re.sub('<[^>]+>', '', str(all_details_on_page[0].find_all("p")[1].find_all("strong")[3])),
		"duration" : re.sub('<[^>]+>', '', str(all_details_on_page[0].find_all("p")[1].find_all("strong")[4])),
		"description" : '',
		"source" : ''
	} 

	for i in range(2, len(all_details_on_page[0].find_all("p"))): 
		if re.search("Page:", str(all_details_on_page[0].find_all("p")[i])):
			details['source'] = re.sub('<[^>]+>|[\n]', '', str(all_details_on_page[0].find_all("p")[i])).strip(' ')
			break
		else: 
			details['description'] += re.sub('<[^>]+>|[\n]|[\r]', '', str(all_details_on_page[0].find_all("p")[i])).strip(" ")
	return details

def make_spells_df(spells): 
	data = pd.DataFrame(spells)["name", "level", "school", "casting time", "ritual", "concentration", "classes", "source"]
	return data

def get_all_spell_details(spell_list): 
	spell_details = []
	for name in spell_list: 
		print(name)
		name = re.sub(' \(Ritual\)$', '-ritual', name)
		name = re.sub(r'[^\x00-\x7F]+|[/]','', name).strip(' ')
		name = name.replace(' ', '-')

		html_address = "https://www.dnd-spells.com/spell/" + str(name.lower())
		print(html_address)
		html = urllib.urlopen(html_address)
		spell_details.append(get_spell_details(bs4.BeautifulSoup(html, 'html.parser')))
	return spell_details

def build_dataFrames(html_soup):
	pass

if __name__ == "__main__":
	html = urllib.urlopen("https://www.dnd-spells.com/spells")

	spells_list = get_all_spells(bs4.BeautifulSoup(html, 'html.parser'))
	spells_df = pd.DataFrame(spells_list)

	all_spell_details = get_all_spell_details(spells_df['name'])
	spell_details_df = pd.DataFrame(all_spell_details)

	spells_df.to_csv('spells.csv', encoding='utf-8')
	spell_details_df.to_csv('spellDetails.csv', encoding='utf-8')


	

