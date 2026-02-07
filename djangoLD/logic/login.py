
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import djangoLD.test_file as test_file
from selenium.webdriver.common.by import By

class LogIn:
    
    def __init__(self, uzr_name, p_word):
        self.uzr_name = uzr_name
        self.p_word = p_word
        
        self.service = Service(executable_path=r"C:/chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors-spki-list')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        
        # self.chrome_options = Options()
        # # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        # self.chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        # self.browser = webdriver.Chrome(test_file.chrome_location, options=self.chrome_options)
        self.logInnn()
        self.refusingToTurnNotificationsOn()
        sleep(3)

    def logInnn(self):
        self.browser.get('https://www.instagram.com')
  #     self.browser.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%227561286020%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D)
        sleep(2)
        try:
            usrNameInput = self.browser.find_element_by_name('username')
        except:
            print('trying email name')
            # usrNameInput = self.browser.find_element_by_name('email')
            usrNameInput = self.browser.find_element(By.XPATH, "//*[@name='email']")
            print(usrNameInput)
        sleep(2)

        # pWordInput = self.browser.find_element_by_name('password')
        pWordInput = self.browser.find_element(By.XPATH, "//*[@name='pass']")
        

        print('logging in...')
        actions = ActionChains(self.browser)
        actions.move_to_element(usrNameInput)
        actions.click(usrNameInput)
        actions.send_keys(self.uzr_name)
        actions.move_to_element(pWordInput)
        actions.click(pWordInput)
        actions.send_keys(self.p_word)
        actions.perform()
        
        actions = ActionChains(self.browser)
        # try:
        #     sleep(2)
        #     signInButton = self.browser.find_element(By.XPATH, '//*[@type="submit"]')
        # except:
        signInButton = self.browser.find_elements(By.XPATH, "//*[@role='button']")
        actions.move_to_element(signInButton[1])
        actions.click()
        actions.perform()
    
    def refusingToTurnNotificationsOn(self):
        print('waiting for 7 sec...')
        sleep(7)
        print('6 sec more..')
        sleep(6)
        print('refusing to turn notifications on...')
        try:
            # notNowButton = self.browser.find_element(By.XPATH, "//*[contains(text(),'Not Now')]")
            # actions = ActionChains(self.browser)
            # actions.move_to_element(notNowButton)
            # actions.click(notNowButton)
            # actions.perform()
            sleep(2)
            self.goingToProfilePage()
        except:
            print("There was an error at login!")
            self.browser.close()
            self.browser = "Logged in but there was an error."
            

    def goingToProfilePage(self):
        print('going to my profile page...')
        self.browser.get('https://www.instagram.com/%s/' % self.uzr_name)
#        profileIcon = self.browser.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')
        
#        ActionChains(self.browser)\
#                  .move_to_element(profileIcon).click()\
#                  .perform()
