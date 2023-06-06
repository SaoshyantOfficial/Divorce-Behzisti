import tkinter as tk
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import os

"""
usernames & passwords and rounds variables in data_read function vary from institue to institute
"""

def update_func():
    global driver, captcha_input, captcha_label, send_captcha_button, recaptcha_button
    
    # To remove update button after clicking
    update_button.destroy()
    
    
    # Setting driver for selenium    
    # options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    driver = webdriver.Firefox()
    
    # Recaptcha button
    recaptcha_button = tk.Button(frame, text="Recaptcha", bg="white", command=captcha_func)
    recaptcha_button.pack(pady=5)
    
    
    # Captcha input text
    captcha_label = tk.Label(frame, text="Enter the captcha :", bg="white")
    captcha_label.pack()

    # Calling captcha func to get and shows captcha image to the user
    captcha_func()
    
    # Getting captcha from user
    captcha_input = tk.Entry(frame)
    captcha_input.pack()
    
    # Button to send captcha input to the site
    send_captcha_button = tk.Button(frame, text="Send", bg="white", command=send_info_site)
    send_captcha_button.pack(pady=5)
    
    
    
# Defining captcha function that gets and shows captcha image
def captcha_func():
    
    url = "https://tasmim.behzisti.net/login.aspx"
    driver.get(url)
    
    # Destroying logo image
    logo_label.destroy()

    # Getting captcha image
    captcha_image = driver.find_element(By.XPATH, "//img[@id='mycapcha_IMG']")

    # Saving captcha image
    with open("captcha.png", "wb") as file:
        file.write(captcha_image.screenshot_as_png)
        
    # Showing captcha image in tkinter frame
    img = Image.open("captcha.png")
    img = img.resize((150, 100), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    captcha_image_label.config(image=photo)
    captcha_image_label.image = photo
        
    

# Function to send information to site(username, password, captcha)
def send_info_site():
    global datas

    # Getting captcha entered by user
    captcha_value = captcha_input.get()

    # Remove captcha's text field & input button & send captcha button and image field
    captcha_input.destroy()  
    captcha_label.destroy()
    send_captcha_button.destroy()
    captcha_image_label.destroy()
    recaptcha_button.destroy()

    # Find and fill in the login form
    username_field = driver.find_element(By.ID, 'tb_name')  
    password_field = driver.find_element(By.ID, 'tb_pass')
    username_field.send_keys('###')
    password_field.send_keys('###')

    # Sending captcha to the site
    captcha_field = driver.find_element(By.ID, "mycapcha_TB_I")
    captcha_field.send_keys(captcha_value)
    
    # Pressing login button
    password_field.send_keys(Keys.RETURN)

    # Waiting for the site to get uploaded
    time.sleep(5)
    
    # Error handling if captcha was wrong or something went wrong
    try:

        # getting target's content & checking if information is correct
        driver.find_element(By.CSS_SELECTOR, ".box2gredient > div:nth-child(1) > h3:nth-child(2)").click()
        driver.find_element(By.CSS_SELECTOR, "li.dropdown-toggle:nth-child(5) > a:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#mytopnav\:submenu\:11 > li:nth-child(2) > a:nth-child(1)").click()
        
    
    except:

        # Showing error label to the user
        error_label = tk.Label(frame, text="Wrong captcha or something went wrong..!", fg="red", bg="white")
        error_label.pack()
        
        restart_button = tk.Button(frame, text="Restart", bg="white", command=restart_func)
        restart_button.pack()
    
    else:
        
        # Getting all threee pages data and concatinating them as a pandas dataframe

        # List to store dataframes for concatinating
        datas = list()
        # First page
        read_data()

        # Second page
        driver.get("https://tasmim.behzisti.net/inbox.aspx?free=1")
        read_data()

        # Third page
        driver.get("https://tasmim.behzisti.net/inbox.aspx?free=2")
        read_data()

        # Concatinating and  saving final data as a csv file
        final_data = pd.concat(datas)
        final_data.to_csv("Center7_Main_Page_Getter.csv", index=False)


        # Showing final text for a successful try(collecting all data)
        successful_text = tk.Label(frame, text="Successfully Done.", bg="white")
        successful_text.pack() 
    
    finally:
        
        # Closing the browser
        driver.quit()



def read_data():
    global dataset, datas
    
    # Frame to hold and merge csv files to each other
    dataset = pd.DataFrame()
    
    def table_collector():
        global dataset
    
        # Saving the page source
        page_source = driver.page_source
            
        # Finding tables to get the values
        soup = BeautifulSoup(page_source, "html.parser")

        # Finding the table tag with id "ContentPlaceHolder1_ASPxGridView1_DXMainTable"
        table = soup.find('table', {'id': 'ContentPlaceHolder1_ASPxGridView1_DXMainTable'})

        #Converting the table to a Pandas DataFrame
        df = pd.read_html(str(table))[0]
            
        # Exporting the DataFrame to an csv file, adding it to the list and removing it
        df.to_csv('output.csv', index=False)

        csv_file = pd.read_csv("output.csv")
        dataset = pd.concat([dataset, csv_file])
        os.remove("output.csv")
    
    table_collector()


    # Creating a loop to collect all the page's tables
    try:
        while True:
            """Creating a loop for selenium to clicks on the pages and
            collect their table's content"""
        
            next_page_button = driver.find_element(By.CSS_SELECTOR, "a.dxp-button:nth-child(2)")
            next_page_button.click()

            table_collector()
    except:
        pass

    
    dataset = dataset.drop([col for col in dataset.columns if col not in ["2", "3", "4", "5", "6", "7", "8", "9",
     "10"]], axis=1)

    dataset.rename(columns={"10" : "نتیجه", 
                  "9": "وضعیت",
                 "8" : "تاریخ پذیرش",
                 "7" : "کد ملی زوجه",
                 "6" : "نام خانوادگی زوجه",
                 "5" : "نام زوجه",
                 "4" : "کد ملی زوج",
                 "3" : "نام خانوادگی زوج",
                 "2" : "نام زوج",
                 }, inplace=True)
        

    # Removing NaN rows that have been saved during scraping
    dataset.dropna(how="all", inplace=True)

    datas.append(dataset)
            


# Defining restart function
def restart_func():
    
    # Closing current window and opening a new root window
    root.destroy()
    
    main_window()
    
    
    
# Creating main tkinter window function
def main_window():
    global root, frame, captcha_image_label, update_button, logo_label
    
    # Create the tkinter window
    root = tk.Tk()
    root.title("Saoshyant")
    
    # Changing root back ground
    root.config(bg="white")
    
    # # logo text
    # logo_text = tk.Label(text="Sepehr Aramesh", bg="white")
    # logo_text.pack(pady=10)
    # create label with image
    logo_image = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo_image, bg="white")
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
    update_button = tk.Button(frame, text="Update", font=("Arial", 16), bg="#4CAF50", command=update_func, width=9, height=2,
    padx=20, pady=10)
    update_button.pack()

    # Start the tkinter event loop
    root.mainloop()
    
    

if __name__ == "__main__":
    main_window()
