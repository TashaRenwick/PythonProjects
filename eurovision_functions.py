from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import pandas as pd

def get_soups(years: list, base_url: str, wait_id: str) -> list:
    # Setting driver options to headless to improve speed
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))

    # Empty list for returning later
    list_of_soups = []

    # Loop through requested year
    for year in years:
        # Construct url and get request
        url = base_url + year

        try:
            driver.get(url)
            # Waiting until voting table is loaded
            element = WebDriverWait(driver, timeout=7).until(EC.presence_of_element_located((By.ID, wait_id)))
            print(f"{url} is ready!")

            # Create soup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Add soup and year to list as tuple
            list_of_soups.append((soup, year))

        except Exception as e:
            print(url, e)
            # could add naughty list ot be reprocessed later

    driver.quit()

    return list_of_soups

def results_df(list_of_soups: list) -> pd.DataFrame:
    # Define empty list for concatenating later
    list_of_dfs = []

    # Loop through soups
    for tuple in list_of_soups:
        # Pulling out soup from tuple
        soup = tuple[0]
        year = tuple[1]

        # Find results table
        table = soup.find('div',
                          attrs={'id': 'voting_table'})
        try:
            # Find content
            table_content = table.find_all('a')
        except Exception as e:
            print(e, tuple[1])


        # List to contain all of the content, will have 4 datum per country
        big_list = []

        # Extract content strings from Soup's NavigableString and append to big_list
        for line in table_content:
            # If link is correct, add to big_list
            link = line['href']
            if year in link:
                big_list.append(link)

            for string in line.strings:
                big_list.append(str(string))

        # Cleaning lists, these are unnecessary extras
        to_remove = ["United Kingdom", "N.Macedonia", ".", "egovina", " "]
        big_list = [x for x in big_list if x not in to_remove]

        # Slice out
        list1 = big_list[0::5]
        list2 = big_list[1::5]
        list3 = big_list[2::5]
        list4 = big_list[3::5]
        list5 = big_list[4::5]

        d = {
            'href':     list2,      # Don't know why these two are the other way round...
            "Country":  list1,
            "Track":    list3,
            "Artist":   list4,
            "Points":   list5
        }

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.transpose()

        df['year'] = tuple[1]

        list_of_dfs.append(df)

    return pd.concat(list_of_dfs, ignore_index=True)

def add_lyrics(df: pd.DataFrame) -> pd.DataFrame:
    # Get links
    list_of_links = df['href'].values.tolist()


    # Get soups
    soups = get_soups(list_of_links, base_url='https://eurovisionworld.com', wait_id='lyrics_0')

    list_of_lyrics = []

    for tuple in soups:
        soup = tuple[0]

        lyric_soup = soup.find('div',
                               attrs={'id': 'lyrics_0'})

        # Cleaning up into one string
        lyrics = [str(x) for x in lyric_soup.find_all('p')]
        lyrics = [x.replace('<p>', '').replace('<br/>', ' ~ ').replace('</p>', '') for x in lyrics]
        lyrics = ' _ '.join(lyrics)

        list_of_lyrics.append(lyrics)

    # Assign list of lyrics to the lyrics column of df
    df['lyrics'] = list_of_lyrics

    return df
