from concurrent.futures import ThreadPoolExecutor
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import os

# Initialize constants
MAX_THREADS = 5  # Max number of concurrent threads
REQUEST_INTERVAL = 4  # Seconds between requests in each thread

def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_recipe_links(base_url, num_pages):
    driver = init_driver()
    all_recipe_links = []

    for i in range(num_pages + 1):
        driver.get(f"{base_url}&page={i}" if i > 0 else base_url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div in soup.find_all('div', class_='column xxlarge-4 large-6 small-12'):
            link_tag = div.find('a', href=True)
            if link_tag and "recept/R-" in link_tag.get('href', ''):
                name = link_tag.get('aria-label', '').replace('Recept: ', '')
                link = "https://www.ah.nl" + link_tag['href']
                img_tag = div.find('img', class_='card-image-set_imageSet__Su7xI')
                image_src = img_tag['data-srcset'].split(', ')[-1].split(' ')[0] if img_tag else ''
                all_recipe_links.append({'name': name, 'link': link, 'image': image_src})
                print(f"{name}: link retrieved")

    driver.quit()
    return all_recipe_links

def scrape_recipe_details(recipe_links, scraped_recipes):
    driver = init_driver()
    all_recipes = []

    for recipe in recipe_links:
        if recipe['link'] in scraped_recipes:
            continue # Skip already scraped recipes

        # Rate limiting
        time.sleep(REQUEST_INTERVAL)

        driver.get(recipe['link'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Simplified scraping logic
        recipe_info = {
            'name': recipe['name'],
            'link': recipe['link'],
            'time_prepare': get_time_element(soup, 0),
            'time_wait': get_time_element(soup, 1),
            'rating': get_rating(soup),
            'rating_count': int(soup.select_one('.recipe-header-rating_count__ugfac').text) if soup.select_one('.recipe-header-rating_count__ugfac') else 0,
            'tags': [tag.text for tag in soup.select('.recipe-header-tags_tags__DFsas li .recipe-tag_text__aKcWG')],
            'servings': get_text(soup, '.recipe-ingredients_count__zS2P-'),
            'ingredients': [(amount.text.strip(), name.text.strip()) for amount, name in zip(soup.select('.recipe-ingredients_ingredientsList__thXVo .ingredient_unit__-ptEq'), soup.select('.recipe-ingredients_ingredientsList__thXVo .ingredient_name__WXu5R'))],
            'equipment': [item.text.strip() for item in soup.select('.recipe-ingredients_kitchen__Ag6XI p.typography_root__Om3Wh')],
            'steps': [step.text.strip() for step in soup.select('.recipe-steps_step__FYhB8 p.typography_root__Om3Wh')],
            'image': recipe['image'],
        }
        print(recipe_info)
        all_recipes.append(recipe_info)

    driver.quit()
    return all_recipes

def get_time_element(soup, index):
    elements = soup.select('.recipe-header-time_timeLine__nn84w')
    return elements[index].text if len(elements) > index else None

def get_rating(soup):
    star_full_count = len(soup.select('.allerhande-icon.svg.svg--svg_star'))
    star_half_count = len(soup.select('.allerhande-icon.svg.svg--svg_star-half'))
    return star_full_count + star_half_count / 2

def get_text(soup, selector):
    element = soup.select_one(selector)
    return element.text if element else None

def save_to_csv(detailed_recipes, filename='recipes.csv'):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, detailed_recipes[0].keys())
        if not file_exists:
            dict_writer.writeheader()  # Write header if file doesn't exist
        dict_writer.writerows(detailed_recipes)

def read_existing_recipes(filename='recipes.csv'):
    try:
        with open(filename, newline='', encoding='utf-8') as file:
            return {row['link'] for row in csv.DictReader(file)}
    except FileNotFoundError:
        # Create an empty file with headers if it doesn't exist
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'link', 'time_prepare', 'time_wait', 'rating', 'rating_count', 'tags', 'servings', 'ingredients', 'equipment', 'steps', 'image'])
        return set()

def main():
    base_url = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
    num_pages = 5

    scraped_recipes = read_existing_recipes()
    recipe_links = scrape_recipe_links(base_url, num_pages)

    new_recipe_links = [link for link in recipe_links if link['link'] not in scraped_recipes]

    if not new_recipe_links:
        print("Finished: no new recipe links found")
        return

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(scrape_recipe_details, new_recipe_links[i:i + MAX_THREADS], scraped_recipes)
                   for i in range(0, len(new_recipe_links), MAX_THREADS)]

        detailed_recipes = []
        for future in futures:
            detailed_recipes.extend(future.result())

    save_to_csv(detailed_recipes)

if __name__ == "__main__":
    main()