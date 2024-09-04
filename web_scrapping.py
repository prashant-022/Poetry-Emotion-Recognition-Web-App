import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get all poem links from the page
def get_poem_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    poem_links = []

    # Finding all poem links from the page
    poem_items = soup.find_all('div', class_='contentListItems rt_manageColumn')
    for item in poem_items:
        link_tag = item.find('a', href=True)
        if link_tag:
            poem_links.append('https://www.hindwi.org' + link_tag['href'])

    return poem_links

# Function to scrape a single poem
def scrape_poem(poem_url):
    response = requests.get(poem_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting poem title
    title_tag = soup.find('div', class_='maincontentBody')
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = 'No Title'
    
    # Extracting poem content
    poem_content = ''
    poem_body_tag = soup.find('div', {'id': lambda L: L and L.startswith('guru-aur-chela')})
    if poem_body_tag:
        poem_content = poem_body_tag.get_text(separator='\n', strip=True)
    
    return {'Title': title, 'Content': poem_content}

# Main scraping function for Hasya Rasa
def scrape_hasya_rasa():
    base_url = 'https://www.hindwi.org/tags/hasya/kavita'
    poem_links = get_poem_links(base_url)
    poems = []

    for link in poem_links:
        poem = scrape_poem(link)
        if poem['Content']:  # Ensure there's content before adding
            poems.append(poem)

        if len(poems) >= 30:  # Limit to 50 poems
            break

    # Saving to Excel file
    df = pd.DataFrame(poems)
    df.to_excel('hasya_rasa_poems.xlsx', index=False)
    print('Saved 50 Hasya Rasa poems to hasya_rasa_poems.xlsx')

# Execute the scraping function
scrape_hasya_rasa()
