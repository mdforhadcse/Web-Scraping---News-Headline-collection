import csv
from time import sleep
from datetime import datetime
from random import random
from selenium.common import exceptions
from selenium import webdriver
# import undetected_chromedriver as uc
from bs4 import BeautifulSoup


def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d%H%S%M")
    # stem = path = '_'.join(search_term.split(' '))
    filename = timestamp + '.csv'
    return filename


def save_data_to_csv(record, filename, new_file=False):
    header = ['headline', 'link', 'description', 'time']
    if new_file:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    else:
        with open(filename, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(record)


def generate_url(page):
    base_template = 'https://banglanews24.com/news-Sort-By-District?district=7&division=2'
    # search_term = search_term.replace(' ', '+')
    stem = base_template  # .format(search_term)
    url_template = stem + '&page={}'
    if page == 1:
        return stem
    else:
        return url_template.format(page)


def extract_card_data(card):
    headline = card.find('a').text.strip()
    link = card.find('a')['href'].strip()
    description = card.find('p').text.strip()
    time = card.find('time').text.strip()
    #
    # description = card.find_element_by_xpath('.//h2/a').text.strip()
    # url = card.find_element_by_xpath('.//h2/a').get_attribute('href')
    # try:
    #     price = card.find_element_by_xpath('.//span[@class="a-price-whole"]').text
    # except exceptions.NoSuchElementException:
    #     return
    # try:
    #     temp = card.find_element_by_xpath('.//span[contains(@aria-label, "out of")]')
    #     rating = temp.get_attribute('aria-label')
    # except exceptions.NoSuchElementException:
    #     rating = ""
    # try:
    #     temp = card.find_element_by_xpath('.//span[contains(@aria-label, "out of")]/following-sibling::span')
    #     review_count = temp.get_attribute('aria-label')
    # except exceptions.NoSuchElementException:
    #     review_count = ""
    return headline, link, description, time


def collect_product_cards_from_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all('div', attrs={'class': 'col-md-8 list'})
    return cards


def sleep_for_random_interval():
    time_in_seconds = random() * 2
    sleep(time_in_seconds)


def run():
    """Run the Amazon webscraper"""
    filename = generate_filename()
    save_data_to_csv(None, filename, new_file=True)  # initialize a new file
    driver = webdriver.Chrome()
    num_records_scraped = 0

    for page in range(1, 21):  # max of 20 pages
        # load the next page
        search_url = generate_url(page)
        print(search_url)
        driver.get(search_url)
        print('TIMEOUT while waiting for page to load')

        # extract product data
        cards = collect_product_cards_from_page(driver)
        for card in cards:
            record = extract_card_data(card)
            if record:
                save_data_to_csv(record, filename)
                num_records_scraped += 1
        sleep_for_random_interval()

    # shut down and report results
    driver.quit()
    print(f"Scraped {num_records_scraped:,d} in banglanews24")


if __name__ == '__main__':
    run()
