
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup

class InstaHub:
    
    def __init__(self, uzr_name, p_word):
        self.uzr_name = uzr_name
        self.p_word = p_word
        self.browser = webdriver.Chrome('C:\chromedriver')
        

    def logInnn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        sleep(2)
        usrNameInput = self.browser.find_element_by_name('username')
        pWordInput = self.browser.find_element_by_name('password')
        signInButton = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
        print('logging in...')
        actions = ActionChains(self.browser)
        actions.move_to_element(usrNameInput)
        actions.click(usrNameInput)
        actions.pause(1)
        actions.send_keys(self.uzr_name)
        actions.move_to_element(pWordInput)
        actions.click(pWordInput)
        actions.pause(1)
        actions.send_keys(self.p_word)
        actions.move_to_element(signInButton)
        actions.click()
        actions.perform()
    
    def refusingToTurnNotificationsOn(self):
        print('refusing to turn notifications on...')
        notNowButton = self.browser.find_element_by_xpath("//*[contains(text(),'Not Now')]")
        sleep(1)
        actions = ActionChains(self.browser)
        actions.move_to_element(notNowButton)
        actions.click(notNowButton)
        actions.perform()
        sleep(1)
        
    def goingToProfilePage(self):
        print('going to my profile page...')
        profileIcon = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')
        
        ActionChains(self.browser)\
                  .move_to_element(profileIcon).click()\
                  .perform()
        
    def gettingNumberOfFollowers(self):
        print('getting followers...')
        self.numberOfFollowers = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
        print('number of followers is {}'.format(self.numberOfFollowers))
        
    def goingToFollowersList(self):
        self.followersLink = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        ActionChains(self.browser)\
          .move_to_element(self.followersLink).click()\
          .perform()
        sleep(1)
        self.followersModal = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]')
            
    def loopThisToScrollTheListOfFollowers(self):
        multiple = .5
        self.theList = []
        loop = 1
        try:
            while len(self.theList) != int(self.numberOfFollowers):
                print(len(self.theList))
                self.browser.execute_script('(document.getElementsByClassName("isgrP"))[0].scrollTo(0, {}*(document.getElementsByClassName("isgrP"))[0].scrollHeight);'.format(multiple))
                print('executing loop number ', loop)
                sleep(1)
                multiple = multiple + 0.1
                self.browser.execute_script('(document.getElementsByClassName("isgrP"))[0].scrollTo(0, {}*(document.getElementsByClassName("isgrP"))[0].scrollHeight);'.format(multiple))
                sleep(1)
                followersList = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul')
                ActionChains(self.browser)\
                      .move_to_element(followersList)\
                      .perform()
                followersListNodes = followersList.get_attribute('innerHTML')
                followerSoup = BeautifulSoup(followersListNodes, 'lxml')
                print('creating the list...')
                sleep(2)
                self.createList(followerSoup.html.body.div)
                loop = loop + 1

                if len(self.theList) > int(self.numberOfFollowers) - 1:
                    print('got all the followers!')
                    break
        except Exception as e:
            print(len(self.theList))
            print('shit didnt work')
            print(e)
            self.browser.close()        

    def createList(self, body):
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
                if f not in self.theList:
                   self.theList.append(f)
            print(f)

    def get_followers(self):
        self.logInnn()
        sleep(4)
        self.refusingToTurnNotificationsOn()
        self.goingToProfilePage()
        sleep(3)
        self.gettingNumberOfFollowers()
        self.goingToFollowersList()
        sleep(1)
        self.loopThisToScrollTheListOfFollowers()
        return self.theList