import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def list_topics(*, key: str = '', geo: str = 'IT', wait: int = 3, full: bool = True):
    """
    accepts a keyword, sends it to Google Trends, processes the response and returns a list with a selection of the data (aka: related topics)

    key: sets the keyword to search
    geo: sets the locality for the query
    wait: sets the time in seconds that the driver should wait for the page to load the lists' container elements
    full: if true sets that the search will keep going as far there is a "next results" button to click
    """
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.add_argument('--headless')
    topics = []
    try:
        with webdriver.Firefox(options=firefoxOptions) as driver:
            try:
                # the first query will return a 429 error, the second one should go through most of the times
                driver.get(
                    f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
                driver.get(
                    f'https://trends.google.com/trends/explore?q={key}&geo={geo}')
                # naively test that the page was loaded, managed as AssertionError
                assert 'Trends' in driver.title
                assert key in driver.title

                # wait for all of the appropriate container class to be loaded
                # this program needs a specific one but because of implementation
                # details it doesn't make a difference to wait for them all
                relatedqueries = WebDriverWait(driver, wait).until(
                    expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'fe-related-queries')))
                # select the correct list container based on the contents of its title child
                # selects the first (and only) element of the list comprehension, managed as IndexError
                relatedquery = [rq for rq in relatedqueries if rq.find_element_by_class_name(
                    'fe-atoms-generic-title').text.find('Related topics help_outline') > -1][0]
                # selects the single list itmes and place them in a list
                # in case the search didn't find any results this list will be empty
                topics = [
                    rq.text for rq in relatedquery.find_elements_by_class_name('label-text')]
                # checks if there are list items and appends a meaningful message in the return list
                if len(topics) < 1:
                    full = False
                    topics.append(['the search found no results'])
                # conditional logic for advancing the search until the end
                if full:
                    next = relatedquery.find_elements_by_class_name(
                        'arrow-right-active')
                    while (len(next) > 0):
                        next[0].click()
                        topics.extend(
                            [rq.text for rq in relatedquery.find_elements_by_class_name('label-text')])
                        next = relatedquery.find_elements_by_class_name(
                            'arrow-right-active')
                # if the program makes it to this point the query is considered a success
                logging.info(
                    f'the query for {key} was successful')

            # exception handling, the info log messages are reasonable assumptions based on
            # the obeserved behavior during development, the exception logs should be exact
            except AssertionError as e:
                logging.info(
                    f'the query for {key} was timed out by the source')
                logging.exception(repr(e), exc_info=True)
            except IndexError as e:
                logging.info(
                    f'the query for {key} couldn\'t find the target element')
                logging.error(repr(e), exc_info=True)
            except Exception as e:
                logging.info(
                    f'the query for {key} failed for an unknown reason')
                logging.error(repr(e), exc_info=True)
    except Exception as e:
        logging.info(
            f'the webdriver failed to open')
        logging.error(repr(e), exc_info=True)
    finally:
        # last opportunity to append a meaningful message
        if len(topics) < 1:
            topics.append(['there was an error'])
        return topics
