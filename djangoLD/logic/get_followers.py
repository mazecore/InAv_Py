
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup
from .login import LogIn
import json
from selenium.webdriver.common.by import By

class FollowingFollowers:
    
    def __init__(self, uzr_name, p_word, following_or_followers, different_user):
        self.uzr_name = uzr_name
        self.followers_or_following = following_or_followers
        self.different_user = different_user
        self.browser = LogIn(uzr_name, p_word).browser
        self.json_content = { 'followers': [], 'pictures': {},'index': 0, 'total': 0 }
        
    def getDifferentUserFollowers(self):
        self.browser.get('https://www.instagram.com/{}'.format(self.different_user))
        try:
            with open(self.different_user + '.json', 'r') as f:
                self.json_content = json.load(f)
        except FileNotFoundError:
            print(self.different_user + '.json file was not previously created.')
        new_followers = self.get_em()
        self.json_content['followers'] += new_followers
        self.json_content['total'] = len(self.json_content['followers'])
        file = open(self.different_user + '.json', 'w')
        file = json.dump(self.json_content, file)
        return new_followers
        
    def gettingTotalNumber(self):
        print('getting %s...' % self.followers_or_following)
        n = (self.browser.find_element(By.XPATH, '//a[contains(@href,"%s")]/span' % self.followers_or_following).text).replace('k', '000')
        n = n.split()[0]
        n = n.replace('.', '')
        n = n.replace(',', '')
        n = n.replace('K', '000')
        n = n.replace('m', '000000')
        n = n.replace('M', '000000')
        print(n)
        self.numberOfFollowers = int(n)
        print('number of {} is {}'.format(self.followers_or_following, self.numberOfFollowers))
        
    def goingToTheList(self):
        self.followersLink = self.browser.find_element(By.XPATH, '//a[contains(@href, "%s")]' % self.followers_or_following)
        print(self.followersLink)
        ActionChains(self.browser)\
          .move_to_element(self.followersLink).click()\
          .perform()
        sleep(1)
#        try:
#           self.followersModal = self.browser.find_element(By.XPATH, '//div[@class="isgrP"]')
#        except:
#            ActionChains(self.browser)\
#              .move_to_element(self.followersLink).click()\
#              .perform()
#            self.followersModal = self.browser.find_element(By.XPATH, '//div[@class="isgrP"]')

    def loopThisToScrollTheListOfFollowers(self):
        print('starting to loop...')
        multiple = .5
        self.theList = []
        loop = 1
        dead_end_detector = []
        try:
            while len(self.theList) != self.numberOfFollowers:
                print('list length on loop start:', len(self.theList))
                dead_end_detector.append(len(self.theList))
                self.browser.execute_script('(document.getElementsByClassName("_aano"))[0].scrollTo(0, {}*(document.getElementsByClassName("_aano"))[0].scrollHeight);'.format(multiple))
                print('executing loop number ', loop)
                sleep(1)
                multiple = multiple + 0.1
                self.browser.execute_script('(document.getElementsByClassName("_aano"))[0].scrollTo(0, {}*(document.getElementsByClassName("_aano"))[0].scrollHeight);'.format(multiple))
                sleep(1)
                followersList = self.browser.find_element(By.XPATH, '//div[@class="_aano"]/div/div')
                ActionChains(self.browser)\
                      .move_to_element(followersList)\
                      .perform()
                followersListNodes = followersList.get_attribute('innerHTML')
                followerSoup = BeautifulSoup(followersListNodes, 'lxml')
                print('creating the list...')
                sleep(2)
                self.createList(followerSoup.html.body)
                loop = loop + 1

                if len(self.theList) >= self.numberOfFollowers - 2:
                    print('got all the %s!' % self.followers_or_following)
                    self.close()
                    break

                if dead_end_detector[-1] == len(self.theList):
                    dead_end_detector.append(len(self.theList))
                    if len(dead_end_detector) > 10:
                        self.close()
                else:
                    if len(dead_end_detector):
                        dead_end_detector.pop()
                    
        except Exception as e:
            print('list on error:', self.theList)
            if (len(self.theList)):
                return self.theList
            print('shit didnt work')
            print(e)
            self.browser.close()       
    
    def close(self):
        # return self.theList
        # self.browser.close()
        try:
            close = self.browser.find_element(By.XPATH, '//button[@class="_abl-"]')
            ActionChains(self.browser)\
                .move_to_element(close).click()\
                .perform()
        except Exception as e:
            print('nyeettt', e)
            return self.theList

    def createList(self, body):
        for li in body:
            print('-------------------------------------------------usrName-------------------------------------------------')
            user = li.find_all(href = True)
            #  print(user)
            img = li.find_all('img', src=True)
            if user != []:
               if user[0]['href'] not in self.json_content['pictures']:
                   self.json_content['pictures'][user[0]['href']] = img[0]['src']
                   self.theList.append(user[0]['href'])
                   print('added user: ', user[0]['href'])

    def get_unfollowers(self):
        unfollowers = []
        self.followers_or_following = 'followers'
        followers = self.get_em()
        self.followers_or_following = 'following'
        self.json_content['pictures'] = {}
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
                button = self.browser.find_element(By.XPATH, '//button[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]')
                ActionChains(self.browser)\
                          .move_to_element(button).click()\
                          .perform()
                sleep(2)
                unfollow_button = self.browser.find_element(By.XPATH, '//button[text()="Unfollow"]')
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
        sleep(13)
        self.loopThisToScrollTheListOfFollowers()
        return self.theList