
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup
from login import LogIn

class Followers:
    
    def __init__(self, uzr_name, p_word):
        self.browser = LogIn(uzr_name, p_word).browser
        
        
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
                      "user_name": usrName[0]['href'], 
                      "user_pic": img[0]['src'],
                      "MyUser": self.uzr_name
                      }
                if f not in self.theList:
                   self.theList.append(f)
            print(f)

    def get_followers(self):
        sleep(3)
        self.gettingNumberOfFollowers()
        self.goingToFollowersList()
        sleep(1)
        self.loopThisToScrollTheListOfFollowers()
        return self.theList