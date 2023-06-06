from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
from Login_Class import MainClass
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
usernames & passwords variables vary from institue to institute
"""

# Creating parameters for login page
mainurl = "https://tasmim.behzisti.net/login.aspx"
target_url = "https://tasmim.behzisti.net/inbox.aspx?free=2"

# TODO clear the hashtags and assign your website username and passwrd insteead , to login into your accout 
username = "###"
password = "###"
username_css_selector = "#tb_name"
password_css_selector = "#tb_pass"
captcha_image_css_selector = "#mycapcha_IMG"
captcha_css_selector = "#mycapcha_TB_I"


class Getid():
    
    def __init__(self):
        
        self.driver = None
        
        # List to hold ids
        self.id_list = []


    def login(self):
        first_data = MainClass(mainurl, username, password, username_css_selector, 
        password_css_selector,captcha_image_css_selector, captcha_css_selector)
      
        first_data.main_window()
      
        self.driver = first_data.get_driver()
    

    # ID collector function
    def id_extractor(self):
        """
        method to extract id from site content
        """
        
        #Finding target elements
        links = self.driver.find_elements(By.XPATH , "//a[text()='عملیات']")
        
        #Extracting all ids from page
        for link in links:
            id_number = link.get_attribute("onclick").split(",")[1].replace("'","")
            id_number = id_number[1:]
            self.id_list.append(id_number)
            
    
    def id_collector(self):
        """
        method to loop over pages and collect their ids
        """

        # Login to the site
        self.login()
    
        # Pishkhan/Rayegan page
        self.driver.get("https://tasmim.behzisti.net/inbox.aspx?free=1") 
        click_button = self.driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_btn_search")
        click_button.click()
        self.id_extractor()

        try:
            while True:
                #Clicking on the next page
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, "a.dxp-button:nth-child(2)")
                next_page_button.click()
                self.id_extractor()

        except:
            pass
            
            
        # Pishkahn/Gheir Rayegan page
        self.driver.get("https://tasmim.behzisti.net/inbox.aspx?free=2")  
        click_button = self.driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_btn_search")
        click_button.click()     
        self.id_extractor()

        try:
            while True:
                #Clicking on the next page
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, "a.dxp-button:nth-child(2)")
                next_page_button.click()
                self.id_extractor()
        except:
            pass

        
        # Pishkahn/List Darkhastha  
        self.driver.get("https://tasmim.behzisti.net/changeRole.aspx")
        self.driver.find_element(By.CSS_SELECTOR, ".box2gredient > div:nth-child(1) > h3:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, "li.dropdown-toggle:nth-child(5) > a:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, "#mytopnav\:submenu\:11 > li:nth-child(2) > a:nth-child(1)").click()
        self.id_extractor()

        try:
            while True:
                #Clicking on the next page
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, "a.dxp-button:nth-child(2)")
                next_page_button.click()
                self.id_extractor()
        except:
            pass
        
        
        # Saving file as an array
        self.id_list = np.array(self.id_list)
        self.id_list = np.unique(self.id_list)
        with open('Center7_ID_Getter.npy', 'wb') as f:
            np.save(f, self.id_list)
        
        time.sleep(1)
        self.driver.quit()

id_getter = Getid()
id_getter.id_collector()
