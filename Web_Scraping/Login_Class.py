#import statements
import tkinter as tk
from tkinter import Tk, Label, PhotoImage , Button
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

class MainClass():
    
    def __init__(self, mainurl, username, password, username_css_selector,
                 password_css_selector, captcha_image_css_selector, captcah_css_selector)  -> None:
        
        self.mainurl = mainurl
        self.username = username
        self.password = password
        self.username_css_selector = username_css_selector
        self.password_css_selector = password_css_selector
        self.captcha_image_css_selector = captcha_image_css_selector
        self.captcha_css_selector = captcah_css_selector
        
        # Setting driver for selenium    
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Firefox() 
 

    
    # To prevent from opening multiple sessions
    def get_driver(self):
        return self.driver
    
    # Closing driver
    def close_driver(self):
        self.driver.quit()
    

    def update_func(self):
        global driver, captcha_input, captcha_label, send_captcha_button, recaptcha_button
        
        # To remove update button after clicking
        update_button.destroy()
        logo_image.__del__()
        
        
        
        # Recaptcha button
        recaptcha_button = tk.Button(frame, text="Recaptcha", bg="white", command=self.captcha_func)
        recaptcha_button.pack(pady=5)
        
        
        # Captcha input text
        captcha_label = tk.Label(frame, text="Enter the captcha :", bg="white")
        captcha_label.pack()

        # Calling captcha func to get and shows captcha image to the user
        self.captcha_func()
        
        # Getting captcha from user
        captcha_input = tk.Entry(frame)
        captcha_input.pack()
        
        # Button to send captcha input to the site
        send_captcha_button = tk.Button(frame, text="Send", bg="white", command=self.send_info_site)
        send_captcha_button.pack(pady=5)
        
        
        
        
    # Defining captcha function that gets and shows captcha image
    def captcha_func(self):
        
        url = self.mainurl
        self.driver.get(url)
        
        # Getting captcha image
        captcha_image = self.driver.find_element(By.CSS_SELECTOR, self.captcha_image_css_selector)

        # Saving captcha image
        with open("captcha.png", "wb") as file:
            file.write(captcha_image.screenshot_as_png)
            
        
        # Showing captcha image in tkinter frame
        img = Image.open("captcha.png")
        img = img.resize((150, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        captcha_image_label.config(image=photo)
        captcha_image_label.image = photo
            
        

    # Define the function to run when the button is clicked
    def send_info_site(self):

        # Because after destroying a button we wont have access to it, we save this input to use afterward
        captcha_value = captcha_input.get()

        # Remove captcha's text field & input button & send captcha button and image field
        captcha_input.destroy()  
        captcha_label.destroy()
        send_captcha_button.destroy()
        captcha_image_label.destroy()
        recaptcha_button.destroy()

        # Find and fill in the login form
        username_field = self.driver.find_element(By.CSS_SELECTOR, self.username_css_selector)  
        password_field = self.driver.find_element(By.CSS_SELECTOR, self.password_css_selector)
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)


        # Sending captcha to the site
        captcha_field = self.driver.find_element(By.CSS_SELECTOR, self.captcha_css_selector)
        captcha_field.send_keys(captcha_value)
        
        # Pressing login button
        password_field.send_keys(Keys.RETURN)

        # Waiting for the site to get uploaded
        time.sleep(1)
        root.destroy()
            

        
        
    # Creating main tkinter window function

    def main_window(self):
        global root, frame, captcha_image_label, update_button , logo_image
        
        # Create the tkinter window
        root = tk.Tk()
        root.title("Saoshyant")
        # Changing root back ground
        root.config(bg="white")
        
        # create label with image
        logo_image = PhotoImage(file="logo.png")
        logo_label = Label(root, image=logo_image, bg="white")
        logo_label.pack(pady=10)


        # Set the window size and position it in the center of the screen
        win_width = 300
        win_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (win_width // 2)
        y = (screen_height // 2) - (win_height // 2)
        root.geometry('{}x{}+{}+{}'.format(win_width, win_height, x, y))

        # Making window unresizable
        root.resizable(height=False, width=False)


        # Create a frame to hold the button and captcha image
        frame = tk.Frame(root, bg="white")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the captcha image label
        captcha_image_label = tk.Label(frame, bg="white")
        captcha_image_label.pack()

        # Create the button and add it to the frame
        update_button = Button(root, text="Login", font=("Arial", 16), bg="#4CAF50", fg="white",
                           padx=20, pady=10, bd=0, command=self.update_func , width=9, height=2)
        update_button.place(relx=0.5, rely=0.6, anchor="center")

        # Change button style
        update_button.config(font=("Helvetica", 14), fg="white", bg="#006600",
                             activebackground="#009900", activeforeground="white")
        
        # Start the tkinter event loop
        root.mainloop()
    