
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class LogIn:
    
    def __init__(self, uzr_name, p_word):
        self.uzr_name = uzr_name
        self.p_word = p_word
        self.browser = webdriver.Chrome('C:\chromedriver')
        self.logInnn()
        sleep(2)
        self.refusingToTurnNotificationsOn()
        self.goingToProfilePage()
        sleep(3)

    def logInnn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
   #     self.browser.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%227561286020%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D)
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
        try:
            sleep(1)
            notNowButton = self.browser.find_element_by_xpath("//*[contains(text(),'Not Now')]")
            actions = ActionChains(self.browser)
            actions.move_to_element(notNowButton)
            actions.click(notNowButton)
            actions.perform()
            sleep(1)
        except:
            self.browser.close()
            

    def goingToProfilePage(self):
        print('going to my profile page...')
        profileIcon = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')
        
        ActionChains(self.browser)\
                  .move_to_element(profileIcon).click()\
                  .perform()