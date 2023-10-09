'''
Python script to scrape LinkedIn job posts
'''
# It seems like the only approach that works is to scrape job descriptions by XPATH and then cleaning it yourself
# chrome webdriver must be added to the system PATH for driver = webdriver.Chrome() to work automatically
# make sure you have the most up-to-date selenium package (4.9.0 as of 10/6/2023): https://github.com/appium/python-client/issues/863
# Something like "from selenium.webdriver.common.by import By" is required for "By.NAME" to work.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import regex

# set our query parameters
query = 'data scientist'
location = 'United States'

# initialize a new instance of the Chrome driver
# the option variable and .add_argument() function below allow you to customize how your Chrome window will show up
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
driver = webdriver.Chrome() # if you want to add options, use the options= parameter and uncomment the two lines above

# set a wait time for the driver
driver.implicitly_wait(10)

# log into LinkedIn
driver.get('https://www.linkedin.com/login')

# insert username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# tell the driver to log in
email_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")
email_input.send_keys(username)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN) # what's the difference bewteen this and Keys.ENTER?

# let the server wait 10sec to log in
time.sleep(30)

# scrape job descriptions
# incomplete: getting multiple job descriptions from 1 page (25 max)
for page_num in range(15):
    url = f'https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&start={25 * (page_num - 1)}'
    driver.get(url)

    # scroll down on a LinkedIn page
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    # NOTE: find_element() will only give you the 1st element
    # use find_elements() to loop through a list of elements
    job_details = driver.find_elements(By.XPATH, '//*[@id="job-details"]')
    data = []
    for j in range(len(job_details)):
        try:
            data.append({'Job_Description': job_details[j].text})
        except AttributeError:
            data.append(0)

    # the html codes for location and company_name need to be updated
    location = driver.find_elements(By.XPATH, '//span[@class="jobs-unified-top-card__bullet"]')
    for l in range(len(location)):
        try:
            data.append({'Location': location[l].text})
        except AttributeError:
            data.append(0)

    company_name = driver.find_elements(By.XPATH, '//h1[@class="t-24 t-bold"]')
    for c in range(len(company_name)):
        try:
            data.append({'Company_Name': company_name[c].text})
        except AttributeError:
            data.append(0)

    print(data)

    df = pd.DataFrame(data)
    df.to_csv(f"LinkedIn Jobs{page_num}.csv", encoding='utf-8', index=False)


driver.quit()

