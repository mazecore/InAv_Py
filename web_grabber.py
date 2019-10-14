
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup
from . import test_file
#import xml.etree.ElementTree as ET

#import requests


#r = requests.get('https://www.investing.com/crypto/currencies')

#soup = bs.BeautifulSoup(r.text, 'xml')

#soup.find_all('a', {'class':'left noWrap elp symb js-currency-symbol'})

browser = webdriver.Chrome('C:\chromedriver')


browser.get('https://www.instagram.com')

print('waiting for 3 seconds...')

sleep(3)

loginButton = browser.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[2]/p/a')


#inputs = browser.find_elements_by_tag_name('input')

ActionChains(browser)\
          .move_to_element(loginButton).click()\
          .perform()

print('waiting 2 seconds....')

sleep(2)

usrNameInput = browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
pWordInput = browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')

signInButton = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')

sleep(3)

print('logging in...')

actions = ActionChains(browser)
actions.move_to_element(usrNameInput)
actions.click(usrNameInput)
actions.pause(2)
actions.send_keys(test_file.login)
actions.move_to_element(pWordInput)
actions.click(pWordInput)
actions.pause(1)
actions.send_keys(test_file.password)
actions.move_to_element(signInButton)
actions.click()
actions.perform()


sleep(3)
print('refusing to turn notifications on...')
notNowButton = browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]')
sleep(1)
actions = ActionChains(browser)
actions.move_to_element(notNowButton)
actions.click(notNowButton)
actions.perform()

sleep(1)

print('going to my profile page...')
profileIcon = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')

ActionChains(browser)\
          .move_to_element(profileIcon).click()\
          .perform()

sleep(3)
print('getting followers...')
followersLink = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
numberOfFollowers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
print('number of followers is {}'.format(numberOfFollowers))

ActionChains(browser)\
          .move_to_element(followersLink).click()\
          .perform()

sleep(1)

followersModal = browser.find_element_by_xpath('/html/body/div[3]/div/div[2]')


sleep(1)
pre_scroll_height = browser.execute_script('return (document.getElementsByClassName("isgrP"))[0].scrollHeight;')
print('pre_scroll_height...')
print(pre_scroll_height)
sleep(1)

multiple = .5
theList = []
def createList(body):
    for li in body:
        print('-----------------------------------------------------usrName-----------------------------------------------------')
        usrName = li.find_all(href = True)
        print(usrName)
        img = li.find_all('img', src=True)
        if usrName != []:
            f = { 
                  "username": usrName[0]['href'], 
                  "userpic": img[0]['src']
                  }
            if f not in theList:
               theList.append(f)
        print(f)
try:
    while len(theList) != int(numberOfFollowers):
        print(len(theList))
        browser.execute_script('(document.getElementsByClassName("isgrP"))[0].scrollTo(0, {}*(document.getElementsByClassName("isgrP"))[0].scrollHeight);'.format(multiple))
        print('executed 1...')
        sleep(2)
        print('executed 2...')
        multiple = multiple + 0.1
        
        browser.execute_script('(document.getElementsByClassName("isgrP"))[0].scrollTo(0, {}*(document.getElementsByClassName("isgrP"))[0].scrollHeight);'.format(multiple))
        sleep(1)
        followersList = browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul')
        ActionChains(browser)\
              .move_to_element(followersList).click()\
              .perform()
        followersListNodes = followersList.get_attribute('innerHTML')
        followerSoup = BeautifulSoup(followersListNodes, 'lxml')
        sleep(2)
        createList(followerSoup.html.body.div)
except:
    browser.close()

sleep(5)



print('passed lxml...')
#print(followerSoup)
print('----------------------------------------------------------------------------------------------------------')


print(theList)

browser.close()

print('----------------------------------------------------------------------------------------------------------')

#ActionChains(browser)\
#          .move_to_element(signInButton)\
#          .click()\
#          .perform()
# 
# 
# 
# t = Timer(20.0, print('yo {}'.format(len(bitcoin) )))

#t.start()
