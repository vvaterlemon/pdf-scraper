import os, requests, sys, argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Documentation
p = argparse.ArgumentParser(description="python script to scrape for all pdf of in a webpage and all its interal links")
p.add_argument("url", type=str, help="root url that the script will start searching from")
p.add_argument("keyphrase", type=str, help="search term that the filename of the pdf should contain")

args = p.parse_args()

# root url 
url = sys.argv[1]
# word looked for 
keyphrase = sys.argv[2]
visited_links = []

# make directory
directory = 'scrapings'
if not os.path.exists(directory):os.mkdir(directory)

def get_all_pdfs(cur_url):
	# download all pdfs in url
	## html of the webpage
	html=BeautifulSoup(requests.get(cur_url).text, "html.parser")  
	## list of pdfs 
	pdfs = html.select(f"a[href$='.pdf'][href*='{keyphrase}']")
	##
	for link in pdfs:
		pdf_url = link['href']
		print(f"Downloading: {pdf_url}")
		# pdf files named using actual file name (not pdf url)
		filename = os.path.join(directory, pdf_url.split('/')[-1])
		with open(filename, 'wb') as f:
			f.write(requests.get(urljoin(cur_url, pdf_url)).content)

	# iterate for all hyperlinks in webpage
	## record current url to avoid downloading repeatedly the same pdf
	visited_links.append(cur_url)	
	## hyperlinks in current webpage within root url
	links = html.select(f"a[href*='{url}']")
	## hyperlinks not visited
	new_links = [link['href'] for link in links if link['href'] not in visited_links]
	print("{} pages visited".format(len(visited_links)))
	## iterate
	if len(new_links) == 0: 
		print("End")
		return 0
	else:
		for new_link in new_links: 
			get_all_pdfs(new_link)
			return 0

get_all_pdfs(url)
