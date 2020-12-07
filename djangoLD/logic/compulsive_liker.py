
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from .login import LogIn
from bs4 import BeautifulSoup
import json
import winsound

class LikerFollower:
    
    def __init__(self, uzr_name, p_word, inputt, numberOfPics):
        self.input = inputt
        self.number = numberOfPics
        self.browser = LogIn(uzr_name, p_word).browser
        self.last_liked = None
        self.message = None
        self.picsURLs = []
        
    def loadFollowers(self):
        with open(self.input + '.json', 'r') as f:
            return json.load(f)

    def updateIndex(self, content, index):
        content['index'] = index
        file = open(self.input + '.json', 'w')
        file = json.dump(content, file)

    def collectFirstPhotosOfFollowers(self):
        content = self.loadFollowers()
        i = content['index']
        #last_index = i + self.number
        while len(self.picsURLs) < self.number + 20:
            try:
                self.browser.get('https://www.instagram.com' + content['followers'][i])
                sleep(3)
                link = self.browser.find_element_by_xpath('//article[@*]/div/div/div/div/a').get_attribute('href')
                if link:
                    print('great success => ', link)
                    self.picsURLs.append(link)
                i += 1
                print('added number inside the loop =>', i)
                print('collected %s pictures' % len(self.picsURLs))
                sleep(1)
            except:
                print(content['followers'][i].replace("/", ""))
                try:
                    private_account = self.browser.find_element_by_xpath('//*[text() = "%s"]' % content['followers'][i].replace("/", ""))
                    i += 1
                    print('added number on private account error =>', i)
                    sleep(1)
                except:
                    try:
                       unavailble = self.browser.find_element_by_xpath ('//*[text() =  "Sorry, this page isn\'t available."]')
                       i+=1
                       print('added number on unavailable account error =>', i)
                       sleep(1)
                    except:
                        winsound.PlaySound('C:\Windows\Media\Windows Proximity Connection.wav', winsound.SND_FILENAME)
                        print('encountered shitty error. waiting for input')
                        sleep(50)
                    continue
                continue
        self.updateIndex(content, i)

    def likeAnothersFollowers(self):
        self.collectFirstPhotosOfFollowers()
        self.like()
        return  {"urls": self.picsURLs, "message": "Liking is complete!", "error": False }

                  
    def loadTagsPage(self):
        self.message = "Tags didn't load"
        self.browser.get('https://www.instagram.com/explore/tags/%s/' % self.input)
        self.counter = 0
        self.thePics = []

        while len(self.picsURLs) < self.number + 20 and self.counter < 100:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            self.thePics = self.browser.find_elements_by_xpath('//a[contains(@href,"/p/")]')
            sleep(2)
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
        t = 0
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
                   print('==============================> PIC # ',j )
                   actions.pause(2)
                   actions.move_to_element(like)
                   actions.click(like)
                   self.last_liked = user_now_liked
                   print('Liked %s !' % user_now_liked)
                   j = j + 1
               t = t + 1
               print('total:', t)
            except:
                actions.pause(1)
            actions.perform()
            # if j > self.number:
            #            break
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
                self.like()
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
