
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

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
        actions.send_keys(self.uzr_name)
        actions.move_to_element(pWordInput)
        actions.click(pWordInput)
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
                  
    def loadTagsPage(self, theTag):
        self.browser.get('https://www.instagram.com/explore/tags/%s/' % theTag)
        self.picsURLs = []
        self.counter = 0
        self.thePics = []

        while len(self.picsURLs) < 100 and self.counter < 20:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
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
            sleep(2)

        print('going to next loop. The urls length is ', len(self.picsURLs))
        

        for i in self.picsURLs:
            self.browser.get(i)
            actions = ActionChains(self.browser)
            actions.pause(2)
            try:
               like = self.browser.find_element_by_xpath("//span[@class='glyphsSpriteHeart__outline__24__grey_9 u-__7']")
               actions.move_to_element(like)
               actions.pause(1)
               actions.click(like)
            except:
                actions.pause(1)
            print('==============================> NEXT PIC')
            actions.pause(1)
            actions.perform()
        self.browser.close()


    def likyLiky(self):
        self.logInnn()
        sleep(4)
        self.refusingToTurnNotificationsOn()
        self.goingToProfilePage()
        sleep(3)
        self.loadTagsPage('Nietzsche')
        return self.thePics