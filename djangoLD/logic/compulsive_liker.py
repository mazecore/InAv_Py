
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from login import LogIn

class LikerFollower:
    
    def __init__(self, uzr_name, p_word, tag, numberOfPics):
        self.tag = tag
        self.number = numberOfPics
        self.browser = LogIn(uzr_name, p_word).browser

                  
    def loadTagsPage(self):
        self.browser.get('https://www.instagram.com/explore/tags/%s/' % self.tag)
        self.picsURLs = []
        self.counter = 0
        self.thePics = []

        while len(self.picsURLs) < self.number and self.counter < 20:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)
            self.thePics = self.browser.find_elements_by_xpath('//a[contains(@href,"/p/")]')
            for pic in self.thePics:
                try:
                    url = pic.get_attribute('href')
                    if url not in self.picsURLs:
                       self.picsURLs.append(url)
                except:
                    print('didnt work')
            print('pics length ========>', len(self.picsURLs))
            self.counter = self.counter + 1
            sleep(1)
        self.picsURLs = self.picsURLs[9:]


    def like(self):
        print('going to next loop. There are %s urls' % len(self.picsURLs))
        j = 0
        for i in self.picsURLs:
            self.browser.get(i)
            actions = ActionChains(self.browser)
            actions.pause(1)
            try:
               like = self.browser.find_element_by_xpath("//span[@class='glyphsSpriteHeart__outline__24__grey_9 u-__7']")
               follow = self.browser.find_element_by_xpath('//button[text()="Follow"]')
               actions.move_to_element(like)
#               actions.pause(1)
               actions.click(like)
#               actions.move_to_element(follow).click()
            except:
                actions.pause(1)
            print('==============================> PIC # ',j )
#            actions.pause(1)
            actions.perform()
            j = j + 1
        self.browser.close()


    def likyLiky(self):
        self.loadTagsPage()
        self.like()
        return self.thePics