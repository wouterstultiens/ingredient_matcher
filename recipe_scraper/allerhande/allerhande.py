from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv

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

    driver.quit()
    return all_recipe_links

def scrape_recipe_details(recipe_links):
    driver = init_driver()
    all_recipes = []

    for recipe in recipe_links:
        driver.get(recipe['link'])
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Simplified scraping logic
        recipe_info = {
            'name': recipe['name'],
            'link': recipe['link'],
            'time_prepare': get_time_element(soup, 0),
            'time_wait': get_time_element(soup, 1),
            'rating': get_rating(soup),
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
    if detailed_recipes:
        keys = detailed_recipes[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(detailed_recipes)

def main():
    # Main execution
    base_url = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
    num_pages = 0

    recipe_links = scrape_recipe_links(base_url, num_pages)
    detailed_recipes = scrape_recipe_details(recipe_links)

    save_to_csv(detailed_recipes)

    for recipe in detailed_recipes:
        print(recipe)

if __name__ == "__main__":
    main()