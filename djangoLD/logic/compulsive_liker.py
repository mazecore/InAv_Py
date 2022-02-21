
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from .login import LogIn
from bs4 import BeautifulSoup
import json
import winsound
import random
import djangoLD.test_file as test_file
import os
# import lxml, lxml.html

class LikerFollower:
    
    def __init__(self, uzr_name, p_word, inputt, numberOfPics, shut_down):
        self.input = inputt
        self.number = numberOfPics
        self.browser = LogIn(uzr_name, p_word).browser
        self.last_liked = None
        self.message = None
        self.picsURLs = []
        self.photolinks = None
        self.shut_down = shut_down
        
    def loadFollowers(self):
        with open(self.input + '.json', 'r') as f:
            return json.load(f)

    def get_manual_stopper(self):
        try:
            with open('stopper.json', 'r') as f:
                value = json.load(f)["manual_stop"]
                print('manual_stopper: %s' % value)
                return value
        except:
            print('couldnt get manual stopper')
        
    def reset_manual_stopper(self):
        with open('stopper.json', 'w') as file:
            json.dump({"manual_stop" : False}, file)

    def loadPics(self):
        try:
            with open(self.input + '_photolinks' + '.json', 'r') as f:
                return json.load(f)
        except:
            return {"links": []}

    def updateIndex(self, content, index):
        print('Updading index of followers links and adding photolinks...')
        content['index'] = index
        file = open(self.input + '.json', 'w')
        file = json.dump(content, file)
        print(self.picsURLs)
        self.photolinks = self.loadPics()
        self.photolinks["links"] += self.picsURLs
        if "index" not in self.photolinks:
           self.photolinks["index"] = 0
        self.photolinks["total"] = len(self.photolinks["links"])
        self.updatePhotoLinks()
    
    def updatePhotoLinks(self):
        print('Updading photolinks...')
        file = open(self.input + '_photolinks' + '.json', 'w')
        file = json.dump(self.photolinks, file)

    def collectFirstPhotosOfFollowers(self):
        content = self.loadFollowers()
        i = content['index']
        manual_stop = False
        #last_index = i + self.number
        while len(self.picsURLs) < self.number and i < len(content['followers']) and not manual_stop:
            try:
                self.browser.get('https://www.instagram.com' + content['followers'][i])
                manual_stop = self.get_manual_stopper()
                sleep(random.randint(3,8))
                link = self.browser.find_element_by_xpath('//article[@*]/div/div/div/div/a').get_attribute('href')
                if link:
                    print('great success => ', link)
                    self.picsURLs.append(link)
                i += 1
                print('added number inside the loop =>', i)
                print('collected %s pictures' % len(self.picsURLs))
                sleep(random.randint(4,20))
            except:
                try:
                    print(content['followers'][i].replace("/", ""))
                    private_account = self.browser.find_element_by_xpath('//*[text() = "%s"]' % content['followers'][i].replace("/", ""))
                    i += 1
                    print('added number on private account error =>', i)
                    sleep(3)
                except:
                    try:
                       unavailble = self.browser.find_element_by_xpath ('//*[text() =  "Sorry, this page isn\'t available."]')
                       i+=1
                       print('added number on unavailable account error =>', i)
                       sleep(1)
                    except:
                        try:
                            finsh = self.browser.find_element_by_xpath ('//*[text() =  "Please wait a few minutes before you try again."]')
                            winsound.PlaySound('C:\Windows\Media\Windows Proximity Connection.wav', winsound.SND_FILENAME)
                            print('this is it. stopping on ', i)
                            break
                        except:
                            winsound.PlaySound('C:\Windows\Media\Windows Proximity Connection.wav', winsound.SND_FILENAME)
                            print('encountered shitty error on ', i)
                            break
                    continue
                continue
        self.updateIndex(content, i)
        self.reset_manual_stopper()
        if self.shut_down:
            os.system("shutdown /s /t 1")
        return  {"urls": self.picsURLs, "message": "Liking is complete!", "error": False }

    def likeAnothersFollowers(self):
        # self.collectFirstPhotosOfFollowers()
        self.photolinks = self.loadPics()
        self.picsURLs = self.photolinks["links"][self.photolinks["index"]:self.photolinks["index"]+250]
        if len(self.picsURLs) < 1:
            print('There are no photolinks to like.')
        else:
            print(self.picsURLs)
            self.like()
            self.browser.close()
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
        t = 1
        for i in self.picsURLs:
            self.browser.get(i)
            sleep(4)
            actions = ActionChains(self.browser)
            try:
               like = self.browser.find_element_by_xpath("//span[@class='fr66n']/button")
               user_now_liked = self.browser.find_element_by_xpath("//div[@class='_7UhW9   xLCgt        qyrsm KV-D4          uL8Hv        T0kll ']/span/a").text
               likeNodes = like.get_attribute('innerHTML')
               likeSoup = BeautifulSoup(likeNodes, 'lxml')
               if likeSoup.findAll('svg', {"aria-label": "Like"}) and self.last_liked != user_now_liked and user_now_liked not in test_file.skips:
                   print('==============================> PIC # ',j )
                   actions.pause(3)
                   actions.move_to_element(like)
                   actions.pause(2)
                   actions.click(like)
                   self.last_liked = user_now_liked
                   print('Liked %s !' % user_now_liked)
                   j = j + 1
               else:
                   print('conditions of the like buttons were not met')
                   print('like button: %s' % like)
                   print('user_now_liked: %s' % user_now_liked)
               t = t + 1
               print('total:', t)
            except:
                print('error occured')
                print('like button: %s' % like)
                print('user_now_liked: %s' % user_now_liked)
                actions.pause(2)
            actions.perform()
            # if j > self.number:
            #            break
        if self.photolinks:
            self.photolinks["index"] = self.photolinks["index"] + t
            self.updatePhotoLinks()
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
                self.browser.close()
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
