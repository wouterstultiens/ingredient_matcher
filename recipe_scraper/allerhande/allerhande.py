from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def scrape_recipe_links(base_url, num_pages):
    all_recipe_links = []
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
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div in soup.find_all('div', class_='column xxlarge-4 large-6 small-12'):
            try:
                link_tag = div.find('a', href=True)
                if link_tag:
                    name = link_tag.get('aria-label', '').replace('Recept: ', '')
                    link = "https://www.ah.nl" + link_tag.get('href', '')
                    img_tag = div.find('img', class_='card-image-set_imageSet__Su7xI')
                    image_src = img_tag.get('data-srcset', '').split(', ')[-1].split(' ')[0] if img_tag else ''

                    if "recept/R-" in link:
                        all_recipe_links.append({'name': name, 'link': link, 'image': image_src})
                        print(f"Recipe: {name} retrieved")
                    else:
                        print(f"LINK NOT VALID: Recipe: {name}, URL: {url}")

            except Exception as e:
                print(f"Error processing a recipe link: {e}")

    driver.quit()
    return all_recipe_links

def scrape_recipe_details(recipe_links):
    all_recipes = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for recipe in recipe_links:
        print(recipe)
        driver.get(recipe['link'])
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Scraping time elements
        time_elements = soup.select('.recipe-header-time_timeLine__nn84w')
        time_prepare = time_elements[0].text if len(time_elements) > 0 else None
        time_wait = time_elements[1].text if len(time_elements) > 1 else None

        # Scraping star ratings
        star_full_count = len(soup.select('.allerhande-icon.svg.svg--svg_star'))
        star_half_count = len(soup.select('.allerhande-icon.svg.svg--svg_star-half'))
        stars = star_full_count + star_half_count / 2

        # Scraping the tags
        tags_list = soup.select('.recipe-header-tags_tags__DFsas li')
        tags = [tag.select_one('.recipe-tag_text__aKcWG').text for tag in tags_list if tag.select_one('.recipe-tag_text__aKcWG')]

        # Scraping servings
        servings = soup.select_one('.recipe-ingredients_count__zS2P-').text if soup.select_one('.recipe-ingredients_count__zS2P-') else None

        # Scraping ingredients
        ingredients = []
        ingredients_list = soup.select('.recipe-ingredients_ingredientsList__thXVo .ingredient_name__WXu5R')
        ingredients_amount = soup.select('.recipe-ingredients_ingredientsList__thXVo .ingredient_unit__-ptEq')
        for amount, name in zip(ingredients_amount, ingredients_list):
            ingredients.append((amount.text.strip(), name.text.strip()))

        # Scraping kitchen equipment
        kitchen_equipment = []
        kitchen_div = soup.find('div', class_='recipe-ingredients_kitchen__Ag6XI')
        if kitchen_div:
            kitchen_items = kitchen_div.find_all('p', class_='typography_root__Om3Wh')
            for item in kitchen_items:
                kitchen_equipment.append(item.text.strip())

        # Scraping the steps
        steps = []
        steps_div = soup.find_all('div', class_='recipe-steps_step__FYhB8')
        for step_div in steps_div:
            step_text = step_div.find('p', class_='typography_root__Om3Wh').text.strip()
            steps.append(step_text)

        recipe_info = {
            'name': recipe['name'],
            'link': recipe['link'],
            'time_prepare': time_prepare,
            'time_wait': time_wait,
            'rating': stars,
            'tags': tags,
            'servings': servings,
            'ingredients': ingredients,
            'equipment': kitchen_equipment,
            'steps': steps,
            'image': recipe['image'],
        }

        all_recipes.append(recipe_info)

    driver.quit()
    return all_recipes

# Base URL and number of pages
base_url = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
num_pages = 0

# Scrape recipe links
recipe_links = scrape_recipe_links(base_url, num_pages)

# Scrape details from each recipe link
detailed_recipes = scrape_recipe_details(recipe_links[:10])

# Print or process the scraped data
for recipe in detailed_recipes:
    print(recipe)