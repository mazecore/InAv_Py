
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from .login import LogIn
from bs4 import BeautifulSoup

class LikerFollower:
    
    def __init__(self, uzr_name, p_word, tag, numberOfPics):
        self.tag = tag
        self.number = numberOfPics
        self.browser = LogIn(uzr_name, p_word).browser
        self.last_liked = None

                  
    def loadTagsPage(self):
        self.browser.get('https://www.instagram.com/explore/tags/%s/' % self.tag)
        self.picsURLs = []
        self.counter = 0
        self.thePics = []

        while len(self.picsURLs) < self.number + 20 and self.counter < 100:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            self.thePics = self.browser.find_elements_by_xpath('//a[contains(@href,"/p/")]')
            sleep(1)
            for pic in self.thePics:
                try:
                    url = pic.get_attribute('href')
                    if url not in self.picsURLs:
                       self.picsURLs.append(url)
                except:
                    print('didnt work')
            print('number of pictures collected ========>', len(self.picsURLs))
            self.counter = self.counter + 1
            sleep(2)
        self.picsURLs = self.picsURLs[9:]


    def like(self):
        print('going to like. There are %s urls' % len(self.picsURLs))
        j = 0
        for i in self.picsURLs:
            self.browser.get(i)
            sleep(2)
            actions = ActionChains(self.browser)
            try:
               like = self.browser.find_element_by_xpath("//span[@class='fr66n']/button")
               user_now_liked = self.browser.find_element_by_xpath("//div[@class='e1e1d']/span/a").text
               likeNodes = like.get_attribute('innerHTML')
               likeSoup = BeautifulSoup(likeNodes, 'lxml')
               if likeSoup.body.svg['aria-label'] == "Like" and self.last_liked != user_now_liked:
                   print('Liked!')
                   actions.pause(2)
                   actions.move_to_element(like)
                   actions.click(like)
                   self.last_liked = user_now_liked
                   print('==============================> PIC # ',j )
                   j = j + 1
            except:
                actions.pause(1) 
            actions.perform()
            if j > self.number:
                       break
        self.browser.close()
        
    def follow(self):
        print('going to follow. There are %s urls' % len(self.picsURLs))
        j = 0
        for i in self.picsURLs:
            self.browser.get(i)
            sleep(2)
            actions = ActionChains(self.browser)
            try:
               follow = self.browser.find_element_by_xpath("//button[text()='Follow']")
               if follow:
                   actions.pause(2)
                   actions.move_to_element(follow)
                   actions.click(follow)
                   print('Followed!')
               else: 
                  print('Did not follow..')
            except:
                actions.pause(1)
                print('Shit didnt work!')
            print('==============================> PIC # ',j )
            actions.perform()
            j = j + 1
        self.browser.close()


    def likyLiky(self):
        self.loadTagsPage()
        self.like()
        return self.picsURLs
    
    def followFollow(self):
        self.loadTagsPage()
        self.follow()
        return 'success!'
