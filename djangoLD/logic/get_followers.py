
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup
from .login import LogIn

class FollowingFollowers:
    
    def __init__(self, uzr_name, p_word, following_or_followers):
        self.uzr_name = uzr_name
        self.followers_or_following = following_or_followers
        self.browser = LogIn(uzr_name, p_word).browser
        
        
    def gettingTotalNumber(self):
        print('getting %s...' % self.followers_or_following)
        self.numberOfFollowers = self.browser.find_element_by_xpath('//a[contains(@href,"%s")]/span' % self.followers_or_following).text
        print('number of {} is {}'.format(self.followers_or_following, self.numberOfFollowers))
        
    def goingToTheList(self):
        self.followersLink = self.browser.find_element_by_xpath('//a[contains(@href, "%s")]' % self.followers_or_following)
        ActionChains(self.browser)\
          .move_to_element(self.followersLink).click()\
          .perform()
        sleep(1)
#        try:
#           self.followersModal = self.browser.find_element_by_xpath('//div[@class="isgrP"]')
#        except:
#            ActionChains(self.browser)\
#              .move_to_element(self.followersLink).click()\
#              .perform()
#            self.followersModal = self.browser.find_element_by_xpath('//div[@class="isgrP"]')

    def loopThisToScrollTheListOfFollowers(self):
        print('starting to loop...')
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
                followersList = self.browser.find_element_by_xpath('//div[@class="isgrP"]/ul')
                ActionChains(self.browser)\
                      .move_to_element(followersList)\
                      .perform()
                followersListNodes = followersList.get_attribute('innerHTML')
                followerSoup = BeautifulSoup(followersListNodes, 'lxml')
                print('creating the list...')
                sleep(2)
                self.createList(followerSoup.html.body.div)
                loop = loop + 1

                if len(self.theList) >= int(self.numberOfFollowers) - 1:
                    print('got all the %s!' % self.followers_or_following)
                    close = self.browser.find_element_by_xpath('//button[@class="wpO6b "]')
                    ActionChains(self.browser)\
                      .move_to_element(close).click()\
                      .perform()
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
    #        img = li.find_all('img', src=True)
            if usrName != []:
                f = { 
                      "user_name": usrName[0]['href'], 
#                      "user_pic": img[0]['src'],
#                      "MyUser": self.uzr_name
                      }
                if f not in self.theList:
                   self.theList.append(f)
            print(f)
            
    def get_unfollowers(self):
        unfollowers = []
        self.followers_or_following = 'followers'
        followers = self.get_em()
        self.followers_or_following = 'following'
        following = self.get_em()
        for i in following:
           if i not in followers:
              unfollowers.append(i)
        print('\n There are %s nonfollowers. \n' % len(unfollowers))
        return unfollowers
    
    def unfollow_unfollowers(self):
        unfollowers = self.get_unfollowers()
        for i in unfollowers:
            try:
                self.browser.get('https://www.instagram.com%s' % i['user_name'])
                sleep(2)
                button = self.browser.find_element_by_xpath('//button[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]')
                ActionChains(self.browser)\
                          .move_to_element(button).click()\
                          .perform()
                sleep(2)
                unfollow_button = self.browser.find_element_by_xpath('//button[text()="Unfollow"]')
                if unfollow_button:
                    ActionChains(self.browser)\
                              .move_to_element(unfollow_button).click()\
                              .perform()
                    sleep(1)
                else:
                    print('\n \n Not a nonfollower! \n \n')
            except Exception as e:
                print('didnt work for %s' % i)
                print(e)
        return unfollowers

    def get_em(self):
        sleep(3)
        self.gettingTotalNumber()
        self.goingToTheList()
        sleep(1)
        self.loopThisToScrollTheListOfFollowers()
        return self.theList