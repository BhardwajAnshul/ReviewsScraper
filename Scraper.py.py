#!/usr/bin/env python
# coding: utf-8

# In[1]:


#to succesfully run this script make sure all libraries are available in the system
try:
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from dateutil.parser import parse
    from datetime import date
    import pandas as pd
    from selenium.webdriver.common.action_chains import ActionChains
except:
    print('Required Python libraries not available')

PATH = "C:\Program Files (x86)\chromedriver.exe" #Put here the location of chromedriver


# In[2]:


lastdate = parse('December 31, 2020').date()

#Review must be newer than this date. 


# In[3]:


#creating a functions to find rating of the product
def ratings(row):
    ratinghtml = row.find(attrs={'class':'stars-container'}).findAll(attrs={'class':'elc-icon star star-small star-rated elc-icon-star-rating'})
    t  = 0
    for x in ratinghtml:
        t = t + 1
    return t


# In[4]:


try:
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()  
except:
    print("chromedriver not found. Please add chromedriver file location in the script and run it again")


# In[5]:


#put the product link here
productLink = "https://www.walmart.com/ip/Clorox-Disinfecting-Wipes-225-Count-Value-Pack-Crisp-Lemon-and-Fresh-Scent-3-Pack-75-Count-Each/14898365"
driver.get(productLink)


# In[6]:


element = driver.find_element_by_class_name('ReviewsFooter-container')
actions = ActionChains(driver)
actions.move_to_element(element).perform()


# In[7]:


#Clicking on See all reviews
for c in driver.find_elements_by_css_selector('#customer-reviews > div.CustomerReviews-footer > div > div > div > a'):
    c.click()


# In[8]:


#Sorting reviews by newest to oldest
for c in driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[5]/div/div[2]/div/div[2]/div/div[2]/select/option[3]'):
    c.click()


# In[9]:


date = date.today()
output = pd.DataFrame(columns =['Date', 'Name', 'Title','Description', 'Rating'])
while date > lastdate:
    soup = BeautifulSoup(driver.page_source)
    table = soup.findAll('div' , attrs = {'class':'Grid-col customer-review-body'}) 

    for row in table:
        daterow = parse(row.find(attrs = {'class':'review-date-submissionTime'}).text).date()
        namerow = row.find(attrs = {'class':'review-footer-userNickname'}).text
        try:
            titlerow = row.find(attrs={'class':'review-title font-bold'}).text
        except:
            titlerow = 'No review title'
        descriptionrow = row.find(attrs = {'class':'review-text'}).text
        ratingrow = ratings(row)
        dfrow =  pd.DataFrame({"Date":[daterow], "Name":[namerow], "Title":[titlerow], "Description":[descriptionrow], "Rating":[ratingrow]})
        output = output.append(dfrow)

    driver.find_element_by_css_selector('body > div.js-content > div > div > div > div.page-content-wrapper > div > div:nth-child(7) > div.product-review-footer > div > div > button.paginator-btn.paginator-btn-next').click()
            
    date = daterow


# In[10]:


output.reset_index(inplace=True)
output.drop(['index'], axis=1, inplace=True)
output.to_csv('output.csv')


# In[11]:


driver.close()

