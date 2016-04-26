#This script aims to extract all plot summaries from the Grimm brother's fairy
#tales

import urllib2
from bs4 import BeautifulSoup
import re

def make_soup(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    return soup, html

def extract_section(soup, html, section_re):
    """
    This function attempts to retrieve a certain section from an article
    If no match is found, it returns None, None
    """
    sections = soup.find_all('h2')
    #Not very Pythonic ;(
    #TODO replace this with finding section, then finding next UL
    for i in xrange(len(sections)):
        if re.search(section_re, str(sections[i])):
            new_html = html.split(str(sections[i]))[1]
            html = new_html.split(str(sections[i + 1]))[0]
            soup = BeautifulSoup(html)
            return soup, html
    return None, None

def extract_plot_section(link, directory):
    """
    This function extracts the plot section of a wiki page and saves them to a
    directory
    """
    try:
        print "http://en.wikipedia.org" + link
        soup, html = make_soup("http://en.wikipedia.org" + link)
    except:
        return
    soup, html = extract_section(soup, html, r"(Synopsis)|(Plot)")
    if soup:
        file_name = directory + link.split('/')[-1]
        f = open(file_name, 'w')
        f.write(soup.get_text().encode('utf8'))
        f.close()

def extract_Grimm():
    #open the page with the fairytales
    soup, html = make_soup("http://en.wikipedia.org/wiki/Grimms%27_Fairy_Tales")

    #We want to find all links in the list of fairy tales
    soup, html = extract_section(soup, html, r"List_of_fairy_tales")

    #find all list items, then extract links from them
    fairytale_list = soup.find_all('li')
    fairytale_list = [x.find('a') for x in fairytale_list]

    links = []
    for tale in fairytale_list:
        if tale != None:
            link = tale['href']
            links.append(link)
            extract_plot_section(link, "./grimm/")

    print len(links)

    """
    for i in xrange(0,20):
        print links[i]
        print "\n"

    print links[-1]
    """

if __name__ == "__main__":
    extract_Grimm()
