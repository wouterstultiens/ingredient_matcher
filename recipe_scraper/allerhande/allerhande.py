from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def scrape_recipes(base_url, num_pages):
    all_recipes = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for i in range(0, num_pages + 1):
        url = f"{base_url}&page={i}" if i > 0 else base_url
        print(f"Accessing URL: {url}")

        driver.get(url)
        time.sleep(5)  # Adding delay to mimic human behavior and prevent blocking

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        recipes_found = False
        for div in soup.find_all('div', class_='column xxlarge-4 large-6 small-12'):
            try:
                link_tag = div.find('a', href=True)
                if link_tag:
                    name = link_tag.get('aria-label', '').replace('Recept: ', '')
                    link = "https://www.ah.nl" + link_tag.get('href', '')
                    img_tag = div.find('img', class_='card-image-set_imageSet__Su7xI')
                    image_src = img_tag.get('data-srcset', '').split(', ')[-1].split(' ')[0] if img_tag else ''

                    all_recipes.append({'name': name, 'link': link, 'image': image_src})
                    recipes_found = True
            except Exception as e:
                print(f"Error processing a recipe: {e}")

        if not recipes_found:
            print(f"Warning: No recipes found at {url}")

    driver.quit()
    return all_recipes

# Base URL and number of pages
base_url = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
num_pages = 2  # Adjust as needed
recipes = scrape_recipes(base_url, num_pages)

# Print or process the scraped data
for recipe in recipes:
    print(recipe)
