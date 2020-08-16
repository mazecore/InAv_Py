
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
        self.message = None
        self.picsURLs = []

                  
    def loadTagsPage(self):
        self.message = "Tags didn't load"
        self.browser.get('https://www.instagram.com/explore/tags/%s/' % self.tag)
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
        self.message = "Tags did load"


    def like(self):
        self.message = "Login and tagged list of photos did load. Liking didn't work."
        print('going to like. There are %s urls' % len(self.picsURLs))
        j = 0
        for i in self.picsURLs:
            self.browser.get(i)
            sleep(3)
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
        self.message = "Liking did work."

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
        if self.thereAreNoErrors():
            try:
                self.loadTagsPage()
                # self.like()
                return  {"urls": self.picsURLs, "message": "Liking is complete!", "error": False }
            except:
                self.browser.close()
                return {"urls": self.picsURLs, "message": self.message, "error": True }
        else:
            return {"urls": None, "message": self.message, "error": True }
            

    
    def thereAreNoErrors(self):
        print('checking if there is an error...')
        if isinstance(self.browser, str):
            self.message = self.browser
            return False
        try:
            error = self.browser.find_element_by_xpath("//*[@id='slfErrorAlert']")
            print(error.text)
            self.message = error.text
            self.browser.close()
            return False
        except:
            return True

    def followFollow(self):
        self.loadTagsPage()
        self.follow()
        return 'success!'
