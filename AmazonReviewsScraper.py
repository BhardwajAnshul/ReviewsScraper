import init_chrome
import time
import re
from dateutil.parser import parse
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
import csv
from urllib.parse import urlparse
import os

driver = init_chrome.init_chrome(executable_path='./chromedriver.exe')

def remove_non_ascii(text, include_new_line=False):
    if include_new_line:
        return re.sub(r'[^a-zA-Z0-9_(.,<>:;?/{}|~`!@#$%^&*+=)\n\r\'\"\-\[\]\\]+',' ', text)
    else:
        return re.sub(r'[^a-zA-Z0-9_(.,<>:;?/{}|~`!@#$%^&*+=)\'\"\-\[\]\\]+',' ', text)

#Scroll down the page to load all elements
def scroll_down_page():
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        speed = driver.get_window_size()['height']/5
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(5*speed/new_height)

#checks if the next page exists and loads the next page if it exists
def nextPage(page, css_selector):
    if len(page.find_elements_by_css_selector(css_selector))>=1:
        actions = ActionChains(driver)
        actions.move_to_element(driver.find_element_by_css_selector(css_selector)).perform()
        driver.find_element_by_css_selector(css_selector).click()
        return True
    else:
        return False

def click(csspath):
    if len(driver.find_elements_by_css_selector(csspath))>=1:
        actions = ActionChains(driver)
        actions.move_to_element(driver.find_element_by_css_selector(csspath)).perform()
        driver.find_element_by_css_selector(csspath).click()
    else:
        pass #do nothing 

def get_date(string):
    return parse(" ".join(string.split()[-3::])).date()

def get_rating(string):
    return string.split()[0]

def get_upvotes(string):
    upvotes = string.split()[0]
    if upvotes == "one":
        return "1"
    else:
        return upvotes

elementpath = '.a-section [data-hook="review"]'
titlepath = '[data-hook="review-title"] span'
title_attr = 'innerText'
commentpath = '[data-hook="review-body"] span'
comment_attr = 'innerText'
userpath = '[class="a-profile-name"]'
user_attr = 'innerText'
reviewdatepath = '[data-hook="review-date"]'
reviewdate_attr = 'innerText'
ratingpath = '[class="a-icon-alt"]'
rating_attr = 'innerText'
typepath = '[data-hook="avp-badge"]'
type_attr = 'innerText'
upvotespath = '[data-hook="helpful-vote-statement"]'
upvotes_attr = 'innerText'
nextPagepath = '.a-last:not(.a-disabled) a'
seeallreviews = '[data-hook="see-all-reviews-link-foot"]'
sortReviews = '[data-a-class="cr-sort-dropdown"]'
byMostRecent = '#sort-order-dropdown_1'


link = "https://www.amazon.in/Approaching-Almost-Machine-Learning-Problem/dp/8269211508"

driver.get(link)
scroll_down_page()
click(csspath=seeallreviews)
scroll_down_page()
click(csspath=sortReviews)
time.sleep(1)
click(csspath=byMostRecent)
time.sleep(5)


fieldnames = ['title', 'comment', 'user', 'reviewdate', 'rating', 'type', 'upvotes']

out_file = 'AmazonReviewsOutput.csv'


if not os.path.isfile(out_file):
    csvfile = open(out_file, 'a', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
else:
    csvfile = open(out_file, 'a', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


ifNextPage = True
while ifNextPage:
    scroll_down_page()
    for element in driver.find_elements_by_css_selector(elementpath):
        elem = element.find_elements_by_css_selector(titlepath)
        title = remove_non_ascii(elem[0].get_attribute(title_attr))
        elem = element.find_elements_by_css_selector(commentpath)
        comment = remove_non_ascii(elem[0].get_attribute(comment_attr))
        elem = element.find_elements_by_css_selector(userpath)
        user = remove_non_ascii(elem[0].get_attribute(user_attr))
        elem = element.find_elements_by_css_selector(reviewdatepath)
        reviewdate = get_date(elem[0].get_attribute(reviewdate_attr))
        try:
            elem = element.find_elements_by_css_selector(ratingpath)
            rating = get_rating(elem[0].get_attribute(rating_attr))
        except:
            rating = 'NA'
        try:
            elem = element.find_elements_by_css_selector(typepath)
            type = elem[0].get_attribute(type_attr)
            if type == "Verified Purchase":
                type = "Verified"
        except:
            type = 'Unverified'
        try:
            elem = element.find_elements_by_css_selector(upvotespath)
            upvotes = get_upvotes(elem[0].get_attribute(upvotes_attr))
        except:
            upvotes = 0
        row = {'title':title, 'comment':comment, 'user':user, 'reviewdate':reviewdate, 'rating':rating, 'type':type, 'upvotes':upvotes}
        writer.writerow(row)
    ifNextPage = nextPage(page=driver, css_selector=nextPagepath)

driver.close()

        



