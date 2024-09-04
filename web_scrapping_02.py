import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL of the website
base_url = 'https://www.maatribhasha.com/'

# List of Rasas with corresponding URL endpoints
rasas = [
    'shringaar_ras.php', 'haasya_ras.php', 'karun_ras.php', 'raudra_ras.php',
    'veer_ras.php', 'bhayanak_ras.php', 'veebhatsa_ras.php', 'adbhut_ras.php', 'shant_ras.php'
]

# Initialize a list to store poems data
poems_data = []

# Loop through each rasa to scrape poems
for rasa in rasas:
    poem_count = 0
    page_number = 1

    while poem_count < 50:
        # Construct the full URL for the rasa page with pagination
        rasa_url = f"{base_url}{rasa}?selector={page_number}&offset={(page_number - 1) * 30}"

        try:
            # Send a GET request to fetch the page content
            response = requests.get(rasa_url, timeout=3)
        except requests.RequestException as e:
            print(f"Failed to fetch page for {rasa}. Error: {e}")
            break

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the page content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links to individual poems
            poem_links = soup.find_all('a', href=True)

            # Check if there are no more poems on this page
            if not poem_links:
                print(f"No more poems found for {rasa}. Exiting.")
                break

            # Loop through each poem link to fetch the poem details
            for link in poem_links:
                poem_url = base_url + link['href']

                # Ensure the link is a valid poem link
                if 'read_poem.php' in poem_url:
                    try:
                        # Send a GET request to fetch the poem page content
                        poem_response = requests.get(poem_url, timeout=10)
                    except requests.RequestException as e:
                        print(f"Failed to fetch poem page at {poem_url}. Error: {e}")
                        continue

                    if poem_response.status_code == 200:
                        poem_soup = BeautifulSoup(poem_response.content, 'html.parser')

                        # Extract the poem title, poet's name, rasa type, and poem text
                        title_tag = poem_soup.find('h3', class_='style1')
                        poem_title = title_tag.get_text(strip=True) if title_tag else "N/A"

                        panel_heading = poem_soup.find('div', class_='panel-heading')
                        if panel_heading:
                            poet_rasa_info = panel_heading.get_text(strip=True).split('|')
                            poet_name = poet_rasa_info[0].strip() if len(poet_rasa_info) > 0 else "Unknown"
                            rasa_type = poet_rasa_info[1].strip() if len(poet_rasa_info) > 1 else "Unknown"
                        else:
                            poet_name = "Unknown"
                            rasa_type = "Unknown"

                        panel_body = poem_soup.find('div', class_='panel-body')
                        poem_text = panel_body.get_text(strip=True) if panel_body else "No Text"

                        # Store the poem details in the list
                        poems_data.append({
                            'Title': poem_title,
                            'Poet': poet_name,
                            'Rasa': rasa_type,
                            'Poem': poem_text
                        })

                        poem_count += 1

                        # Break out of the loop if we reach 100 poems
                        if poem_count >= 50:
                            break
                    else:
                        print(f"Failed to fetch poem page at {poem_url}. Status code: {poem_response.status_code}")
        else:
            print(f"Failed to fetch page for {rasa}. Status code: {response.status_code}")
            break

        # Increment page number for next loop
        page_number += 1

        # Pause to be respectful to the server
        time.sleep(1)

        # Stop after 10 pages if no valid poems are found
        if page_number > 3:
            print(f"Reached page limit for {rasa}. Exiting.")
            break

        print(f"Processed page {page_number} for {rasa}, total poems collected: {poem_count}")

# Create a DataFrame from the list of poems
df = pd.DataFrame(poems_data)

# Save the DataFrame to an Excel file
df.to_excel('hindi_poetry_dataset_auto.xlsx', index=False)

print("Poetry dataset has been saved to hindi_poetry_dataset.xlsx")
