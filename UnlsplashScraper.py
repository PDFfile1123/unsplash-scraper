import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
import os
import time
import io
from PIL import Image

#these are used to setup how chromedriver functions
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

#this is the path to where you downloaded the chromedriver, make sure you get the right chromedriver for your version of chrome
DRIVER_PATH= r"add path here"
driver = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)

class UnsplashImageScraper():
    
    def __init__(self, image_path, Search_key, num_images,):
        
        #this checks if the folder exists and if it doesnt, creates a folder
        image_path = os.path.join(image_path, Search_key)
        if not os.path.exists(image_path):
            print("[INFO] Image path not found. Creating a new folder.")
            os.makedirs(image_path)   
                 
        self.Search_key = Search_key
        self.num_images = num_images
        self.image_path = image_path
        self.url = "https://unsplash.com/s/photos/" + Search_key
        print (self.url)

        
    def find_image_urls(self):
        print("[INFO] beginning image link gathering")
        
        #this opens the webpage
        driver.get(self.url)
        
        #this clicks the load more button
        driver.find_element(By.XPATH,"//button[contains(text(),'Load more')]").click()
        
        #this scrolls so that images may load
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)
        
        #this selects images
        imgResults = driver.find_elements(By.XPATH,"//img[@class ='tB6UZ a5VGX']")
        
        #src are the image urls
        src = []
        for img in imgResults:
            src.append(str(img.get_attribute('src')))
        return src
            
    def save_images(self,image_urls, ):
        print("[INFO] saving images")
        
        if self.num_images < len(image_urls): 
            self.num_images = len(image_urls) 
            print("[INFO] less images than requested")
            
        for image_url in image_urls:  
            #gets the html of image source change timeout to control max how long will spend saving images
            image = requests.get(image_url,timeout=60)
            
            with Image.open(io.BytesIO(image.content)) as image_from_web:
                
                #extact filename without extension from URL
                o = urlparse(image_url)
                image_url = o.scheme + "://" + o.netloc + o.path
                name = os.path.splitext(os.path.basename(image_url))[0]
                
                #join filename and extension
                filename = "%s.%s"%(name,image_from_web.format.lower())
                image_path = os.path.join(self.image_path, filename)
                
                print(f"[INFO] {self.Search_key} Image saved at: {image_path}")
                
                image_from_web.save(image_path) 
                image_from_web.close()
            



image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

#input search key here
Search_Key="Computer%20Keyboard"

#input parameters
num_images = 100

#main
ImageScraper=UnsplashImageScraper(image_path, Search_Key, num_images)
image_urls = ImageScraper.find_image_urls()
ImageScraper.save_images(image_urls)
