#!/usr/bin/python3
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
from Login_Class import MainClass
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import Tk, Label, PhotoImage , Button
from selenium import webdriver
import time
import logging

WARNING = '\033[93m'
ENDC = '\033[0m'
GREEN = '\033[92m'

logging.basicConfig(
    filename='log.log'
)
logger = logging.getLogger(__name__)

# Main class
class Update():

    def __init__(self) -> None:

        # Base data frame that their has been collected
        self.df = pd.DataFrame()
        # If the web scraper code stops in the middle, uncomment the below line and comment the top line (put the correct name for .csv file)
        # self.df = pd.read_csv("Center7_Form_Getter.csv")
        self.form_pazriresh_df = None
        self.form_arzyabi_avalie_df = None
        self.form_a_df = None
        self.form_b_df = None
        self.form_g_df = None
        self.except_list = list()
        self.soup = None
    
    # collect the text fields content
    def text_field_collector(self, tag):
            try:
                if tag.has_attr("value"):
                    value = tag.get("value")
                else:
                    value = None
                return value
            except:
                return None

    # check for which option in select input tag has been chosen
    def check(self, checklist):
            global holder
            holder = None
            try:
                for i in checklist:
                    tag = self.soup.select_one(i)

                    if tag.has_attr("checked"):
                        holder = self.soup.select_one(checklist[i]).text
                        break

                    else:
                        continue
                        
                return holder

            except:
                return holder


    # Main Page interface
    def main_window(self):
        global window, update_button

        # Create a tkinter window
        window = Tk()
        window.title("Saoshyant")

        # Set the size and position of the window
        window.geometry("300x400")
        window.resizable(False, False)

        # Set the window background color to white
        window.configure(bg="white")

        logo_image = PhotoImage(file="logo.png")

        # create label with image
        logo_label = Label(window, image=logo_image, bg="white")
        logo_label.pack(pady=10)

        # Create a button in the center of the window
        update_button = Button(window, text="Continue", font=("Arial", 16), bg="#4CAF50", fg="white",
                           padx=20, pady=10, bd=0, command=self.update , width=9, height=2)
        update_button.place(relx=0.5, rely=0.6, anchor="center")

        # Change button style
        update_button.config(font=("Helvetica", 14), fg="white", bg="#006600", activebackground="#009900", activeforeground="white")

        # Change label style
        logo_label.config(font=("Arial", 20), fg="#009900")

        # Start the tkinter event loop
        window.mainloop()

    # get the form paziresh
    def form_paziresh(self, id):

        # Dataset to add data to it by loop
        dataset = pd.DataFrame()

        try:

            # Getting target page for each id
            url = f"https://tasmim.behzisti.net/edit_darkhast.aspx?id={id}"
            driver.get(url)

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            #Get page source to find elements in
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            self.soup = soup

            #Divorce Type
            divorce_type_checklist = {'#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh_0' : '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh_1' : '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh_2' : '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh_3' : '#ContentPlaceHolder1_RadioButtonList_motaghazi_talagh > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)'
            }
            divorce_type = self.check(divorce_type_checklist)


            #Vekaalat Nameh
            does_have_vekaalat_nameh_checklist = {'#ContentPlaceHolder1_radio_vekalat_0' : '#ContentPlaceHolder1_radio_vekalat > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)',
                                    '#ContentPlaceHolder1_radio_vekalat_1' : '#ContentPlaceHolder1_radio_vekalat > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'
            }
            does_have_vekaalat_nameh = self.check(does_have_vekaalat_nameh_checklist)


            # Citizenship

            # Husband
            husband_citizenship_checklist = {'#ContentPlaceHolder1_Radiolist_tabeiat_zoj_0' : '#ContentPlaceHolder1_Radiolist_tabeiat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                '#ContentPlaceHolder1_Radiolist_tabeiat_zoj_1' : '#ContentPlaceHolder1_Radiolist_tabeiat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'
            }
            husband_citizenship = self.check(husband_citizenship_checklist)


            # Reception Date
            tag = soup.select_one("#ContentPlaceHolder1_tb_tarikhe_paziresh")
            reception_date_text_field = self.text_field_collector(tag)

            # International ID

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_code_meli_mard")
            husband_international_id_textfield = self.text_field_collector(tag)

            # Staying Code

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_code_eghamat_zoj")
            husband_staying_code_textfield = self.text_field_collector(tag)
            # First Name

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_name_mard")
            husband_first_name_textfield = self.text_field_collector(tag)
            

            # Last Name

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_family_mard")
            husband_last_name_textfield = self.text_field_collector(tag)


            # Birth Date

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_tavalod_mard")
            husband_birth_date_textfield = self.text_field_collector(tag)

            

            # Birth Location

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_mahale_tavalode_mard")
            husband_birth_location_textfield = self.text_field_collector(tag)

            # Passport Number

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_shomare_menasname_mard")
            husband_passport_number_textfield = self.text_field_collector(tag)


            # Husband
            tag = soup.select_one('#ContentPlaceHolder1_tb_seryal_mard')
            husband_passport_serial_textfield = self.text_field_collector(tag)


            # Father Name

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_pedar_mard")
            husband_father_name_textfield = self.text_field_collector(tag)

            # Mobile Phone

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_mobile_mard")
            husband_mobile_phone_textfield = self.text_field_collector(tag)
            
            # Adderess Type

            #Husband
            husband_address_type_checklist = {'#ContentPlaceHolder1_Radio_list_noe_address_zoj_0' : '#ContentPlaceHolder1_Radio_list_noe_address_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radio_list_noe_address_zoj_1' : '#ContentPlaceHolder1_Radio_list_noe_address_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radio_list_noe_address_zoj_2' : '#ContentPlaceHolder1_Radio_list_noe_address_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
            }
            husband_address_type = self.check(husband_address_type_checklist)


            # Village Name

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_name_rosta_zoj")
            husband_village_name_textfield = self.text_field_collector(tag)


            # Adderess

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_address_mard")
            husband_address_textfield = self.text_field_collector(tag)

            # Education

            # Husband
            husband_education_cheklist = {'#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_0' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_1' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_2' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_3' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_4' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_5' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_6' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(7) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard_7' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(8) > label:nth-child(2)' ,
            }
            husband_education = self.check(husband_education_cheklist)





            # Staying State

            # Husband
            husband_staying_state_checklist = {'#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_0' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_1' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_2' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_3' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_4' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_5' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard_6' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(7) > span:nth-child(1) > label:nth-child(2)'

            }

            husband_staying_state = self.check(husband_staying_state_checklist)



            # Home Tel

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_telephone_sabet_mard")
            husband_home_tel_textfield = self.text_field_collector(tag)



            # Family Dimension

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_boode_khanvar_mard")
            husband_family_dim_textfield = self.text_field_collector(tag)


            # Referral Method

            # Husband
            husband_referral_method_checklist = {'#ContentPlaceHolder1_RadioButtonList_nahve_erja_mard_0' : '#ContentPlaceHolder1_RadioButtonList_nahve_erja_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_nahve_erja_mard_1' : '#ContentPlaceHolder1_RadioButtonList_nahve_erja_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_nahve_erja_mard_2' : '#ContentPlaceHolder1_RadioButtonList_nahve_erja_mard > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)'
            }
            husband_referral_method = self.check(husband_referral_method_checklist)


            # Referred To Center
            referred_to_center_checklist = {'#ContentPlaceHolder1_RadioButtonList_morajeat_konande_0' : '#ContentPlaceHolder1_RadioButtonList_morajeat_konande > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_morajeat_konande_1' : '#ContentPlaceHolder1_RadioButtonList_morajeat_konande > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_morajeat_konande_2' : '#ContentPlaceHolder1_RadioButtonList_morajeat_konande > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_morajeat_konande_3' : '#ContentPlaceHolder1_RadioButtonList_morajeat_konande > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_morajeat_konande_4' : '#ContentPlaceHolder1_RadioButtonList_morajeat_konande > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)' ,

            }
            referred_to_center = self.check(referred_to_center_checklist)


            # Couple Housing State
            couple_housing_state_checklist = {'#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein_0' : '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)',
                                            '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein_1' : '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)',
                                            '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein_2' : '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)',
                                            '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein_3' : '#ContentPlaceHolder1_RadioButtonList_vaziate_maskan_zojein > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)'

            }
            couple_housing_state = self.check(couple_housing_state_checklist)

            #############
            
            # Second page
            go_to_wife_page_button = driver.find_element(By.ID , 'wizard-t-1')
            go_to_wife_page_button.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            # Wife
            wife_citizenship_checklist = {'#ContentPlaceHolder1_Radiolist_tabeiate_zoje_0' : '#ContentPlaceHolder1_Radiolist_tabeiate_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                '#ContentPlaceHolder1_Radiolist_tabeiate_zoje_1' : '#ContentPlaceHolder1_Radiolist_tabeiate_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'
            }
            wife_citizenship = self.check(wife_citizenship_checklist)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_code_meli_zan")
            wife_international_id_textfield = self.text_field_collector(tag)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_code_eghamat_zoje")
            wife_staying_code_textfield = self.text_field_collector(tag)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_name_zan")
            wife_first_name_textfield = self.text_field_collector(tag)

            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_family_zan")
            wife_last_name_textfield = self.text_field_collector(tag)

            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_tavalood_zan")
            wife_birth_date_textfield = self.text_field_collector(tag)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_mahale_tavalode_zan")
            wife_birth_location_textfield = self.text_field_collector(tag)

            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_shomare_shenasname_zan")
            wife_passport_number_textfield = self.text_field_collector(tag)


            #Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_seryal_zan")
            wife_passport_serial_textfield = self.text_field_collector(tag)

            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_pedar_zan")
            wife_father_name_textfield = self.text_field_collector(tag)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_mobile_zan")
            wife_mobile_phone_textfield = self.text_field_collector(tag)


            # Wife
            wife_address_type_checklist = {'#ContentPlaceHolder1_Radio_list_noe_address_zoje_0' : '#ContentPlaceHolder1_Radio_list_noe_address_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radio_list_noe_address_zoje_1' : '#ContentPlaceHolder1_Radio_list_noe_address_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radio_list_noe_address_zoje_2' : '#ContentPlaceHolder1_Radio_list_noe_address_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
            }
            wife_address_type = self.check(wife_address_type_checklist)

            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_name_rosta_zoje")
            wife_village_name_textfield = self.text_field_collector(tag)




            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_address_zan")
            wife_address_textfield = self.text_field_collector(tag)




            # Wife
            wife_education_cheklist = {'#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_0' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_1' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_2' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_3' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_4' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_5' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_6' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(7) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan_7' : '#ContentPlaceHolder1_RadioButtonList_tahsilat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(8) > label:nth-child(2)' ,

            }
            wife_education = self.check(wife_education_cheklist)


            #  Wife
            wife_staying_state_checklist = {'#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_0' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_1' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_2' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_3' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_4' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_5' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan_6' : '#ContentPlaceHolder1_RadioButtonList_mahal_sokonat_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(7) > span:nth-child(1) > label:nth-child(2)' ,
            }
            wife_staying_state = self.check(wife_staying_state_checklist)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_telephone_sabet_zan")
            wife_home_tel_textfield = self.text_field_collector(tag)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_boode_khanevar_zan")
            wife_family_dim_textfield = self.text_field_collector(tag)


            # Wife
            wife_referral_method_checklist = {'#ContentPlaceHolder1_RadioButtonList_nahve_erja_zan_0' : '#ContentPlaceHolder1_RadioButtonList_nahve_erja_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_nahve_erja_zan_1' : '#ContentPlaceHolder1_RadioButtonList_nahve_erja_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_nahve_erja_zan_2' : '#ContentPlaceHolder1_RadioButtonList_nahve_erja_zan > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)'
            }
            wife_referral_method = self.check(wife_referral_method_checklist)



            data_dict = {
                        "تاریخ پذیرش" :[reception_date_text_field] ,
                        "نوع درخواست طلاق" : [divorce_type],
                        "ایا برای طلاق یکی از زوجین وکالت نامه رسمی دارد؟" : [does_have_vekaalat_nameh],
                        "تابعیت زوج" : [husband_citizenship] ,
                        "تابعیت زوجه" : [wife_citizenship] ,
                        "کد ملی زوج" : [husband_international_id_textfield] ,
                        "کد ملی زوجه" : [wife_international_id_textfield] ,
                        "کد اقامت زوج" : [husband_staying_code_textfield] ,
                        "کد اقامت زوجه" : [wife_staying_code_textfield] ,
                        "نام زوج" : [husband_first_name_textfield] ,
                        "نام زوجه" : [wife_first_name_textfield] ,
                        "نام خانوادگی زوج" : [husband_last_name_textfield] ,
                        "نام خانوادگی زوجه" : [wife_last_name_textfield] ,
                        "تاریخ تولد زوج" : [husband_birth_date_textfield] ,
                        "تاریخ تولد زوجه " : [wife_birth_date_textfield] ,
                        "محل تولد زوج " : [husband_birth_location_textfield] ,
                        "محل تولد زوجه " : [wife_birth_location_textfield] ,
                        "شماره شناسنامه زوج" : [husband_passport_number_textfield] ,
                        "شماره شناسنامه زوجه" : [wife_passport_number_textfield] ,
                        "سریال شناسنامه  زوج" : [husband_passport_serial_textfield] ,
                        "سریال شناسنامه زوجه" : [wife_passport_serial_textfield] ,
                        "نام پدر زوج" : [husband_father_name_textfield] ,
                        "نام پدر وزجه" :[wife_father_name_textfield] ,
                        "تلفن همراه زوج " : [husband_mobile_phone_textfield] ,
                        "تلفن همراه زوجه" : [wife_mobile_phone_textfield] ,
                        "نوع آدرس زوج" : [husband_address_type] ,
                        "نوع آدرس زوجه ": [wife_address_type] ,
                        "نام روستا زوج" : [husband_village_name_textfield] ,
                        "نام روستا زوجه" : [wife_village_name_textfield] ,
                        "آدرس زوج" : [husband_address_textfield] ,
                        "آدرس زوجه" : [wife_address_textfield] ,
                        "تحصیلات زوج ": [husband_education] ,
                        "تحصیلات زوجه" : [wife_education] ,
                        "وضعیت محل سکونت زوج" : [husband_staying_state] ,
                        "وضعیت محل سکونت زوجه" : [wife_staying_state] ,
                        "تلفن ثابت زوج" : [husband_home_tel_textfield] ,
                        "تلفن ثابت زوجه" : [wife_home_tel_textfield] ,
                        "بعد خانوار زوج " : [husband_family_dim_textfield] ,
                        "بعد خانوار زوجه" : [wife_family_dim_textfield] ,
                        "نحوه ارجاع زوج" : [husband_referral_method] ,
                        "نحوه ارجاع زوجه" : [wife_referral_method] ,
                        "مراجعه کننده به مرکز" : [referred_to_center] ,
                        "وضعیت مسکن زوجین" : [couple_housing_state]

            }



            # Adding each data to the main dataframe
            self.form_paziresh_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)

        except:
            data_dict = {
                        "تاریخ پذیرش" :[None] ,
                        "نوع درخواست طلاق" : [None],
                        "ایا برای طلاق یکی از زوجین وکالت نامه رسمی دارد؟" : [None],
                        "تابعیت زوج" : [None] ,
                        "تابعیت زوجه" : [None] ,
                        "کد ملی زوج" : [None] ,
                        "کد ملی زوجه" : [None] ,
                        "کد اقامت زوج" : [None] ,
                        "کد اقامت زوجه" : [None] ,
                        "نام زوج" : [None] ,
                        "نام زوجه" : [None] ,
                        "نام خانوادگی زوج" : [None] ,
                        "نام خانوادگی زوجه" : [None] ,
                        "تاریخ تولد زوج" : [None] ,
                        "تاریخ تولد زوجه " : [None] ,
                        "محل تولد زوج " : [None] ,
                        "محل تولد زوجه " : [None] ,
                        "شماره شناسنامه زوج" : [None] ,
                        "شماره شناسنامه زوجه" : [None] ,
                        "سریال شناسنامه  زوج" : [None] ,
                        "سریال شناسنامه زوجه" : [None] ,
                        "نام پدر زوج" : [None] ,
                        "نام پدر وزجه" :[None] ,
                        "تلفن همراه زوج " : [None] ,
                        "تلفن همراه زوجه" : [None] ,
                        "نوع آدرس زوج" : [None] ,
                        "نوع آدرس زوجه ": [None] ,
                        "نام روستا زوج" : [None] ,
                        "نام روستا زوجه" : [None] ,
                        "آدرس زوج" : [None] ,
                        "آدرس زوجه" : [None] ,
                        "تحصیلات زوج ": [None] ,
                        "تحصیلات زوجه" : [None] ,
                        "وضعیت محل سکونت زوج" : [None] ,
                        "وضعیت محل سکونت زوجه" : [None] ,
                        "تلفن ثابت زوج" : [None] ,
                        "تلفن ثابت زوجه" : [None] ,
                        "بعد خانوار زوج " : [None] ,
                        "بعد خانوار زوجه" : [None] ,
                        "نحوه ارجاع زوج" : [None] ,
                        "نحوه ارجاع زوجه" : [None] ,
                        "مراجعه کننده به مرکز" : [None] ,
                        "وضعیت مسکن زوجین" : [None]

            }
            
            
            self.form_paziresh_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)
            
            self.except_list.append(id)
            print(f"{WARNING}an exception occurred in form paziresh...{ENDC}")
            logger.exception('exception in form paziresh')


    # get the form arzyabi avalie
    def form_arzyabi_avalie(self, id):

        # Dataset to add data to it by loop
        dataset = pd.DataFrame()
        
        try:

            # Getting target page for each id
            url = f"https://tasmim.behzisti.net/ghtarikhche_zojein.aspx?id={id}"
            driver.get(url)

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            #Get page source to find elements in
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            self.soup = soup

            # Divorce definition
            divorce_type_textfield = soup.select_one("#ContentPlaceHolder1_lb_noe_talagh").text


            # Divorce applicant
            Consensual_divorce_applicant_checklist = {"#ContentPlaceHolder1_Radiolist_motaghazi_talaghe_tavafoghi_0" : "#ContentPlaceHolder1_Radiolist_motaghazi_talaghe_tavafoghi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_Radiolist_motaghazi_talaghe_tavafoghi_1" : "#ContentPlaceHolder1_Radiolist_motaghazi_talaghe_tavafoghi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_Radiolist_motaghazi_talaghe_tavafoghi_2" : "#ContentPlaceHolder1_Radiolist_motaghazi_talaghe_tavafoghi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)"}

            Consensual_divorce_applicant = self.check(Consensual_divorce_applicant_checklist)

            # Marriage date
            tag = soup.select_one("#ContentPlaceHolder1_tb_tarikhe_ezdevaj")
           
            marriage_date = self.text_field_collector(tag)


            # Man & Woman marriage age
            tag = soup.select_one("#ContentPlaceHolder1_tb_sen_mard_hengame_ezdevaj")
         
            husband_Marriage_age_textfield = self.text_field_collector(tag)
                
            tag = soup.select_one("#ContentPlaceHolder1_tb_sen_zan_hengame_ezdevaj")
            wife_marriage_age_textfield = self.text_field_collector(tag)


            # Marriage duration
            tag = soup.select_one("#ContentPlaceHolder1_tb_modat_zaman_zendegi_moshtarak_sal")
            marriage_duration_year_textfield = self.text_field_collector(tag)
                
            tag = soup.select_one("#ContentPlaceHolder1_tb_modat_zaman_zendegi_moshtarak_mah")
            marriage_duration_month_textfield = self.text_field_collector(tag)


            # Marriage situation
            marriage_situation_checklist = {"#ContentPlaceHolder1_vaziate_feli_zendegi_moshtarak_0" : "#ContentPlaceHolder1_vaziate_feli_zendegi_moshtarak > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                            "#ContentPlaceHolder1_vaziate_feli_zendegi_moshtarak_1" : "#ContentPlaceHolder1_vaziate_feli_zendegi_moshtarak > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                            "#ContentPlaceHolder1_vaziate_feli_zendegi_moshtarak_2" : "#ContentPlaceHolder1_vaziate_feli_zendegi_moshtarak > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)"}


            marriage_situation = self.check(marriage_situation_checklist)


            # Dating history
            dating_history_check_list = {"#ContentPlaceHolder1_Radiolist_ashenayi_ghabli_0" : "#ContentPlaceHolder1_Radiolist_ashenayi_ghabli > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                            "#ContentPlaceHolder1_Radiolist_ashenayi_ghabli_1" : "#ContentPlaceHolder1_Radiolist_ashenayi_ghabli > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            dating_history = self.check(dating_history_check_list)


            # Acquaintance's type
            acquaintance_type_checklist = {"#ContentPlaceHolder1_Radiolist_noe_ashenaei_0" : "#ContentPlaceHolder1_Radiolist_noe_ashenaei > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_ashenaei_1" : "#ContentPlaceHolder1_Radiolist_noe_ashenaei > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_ashenaei_2" : "#ContentPlaceHolder1_Radiolist_noe_ashenaei > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_ashenaei_3" : "#ContentPlaceHolder1_Radiolist_noe_ashenaei > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_ashenaei_4" : "#ContentPlaceHolder1_Radiolist_noe_ashenaei > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_ashenaei_5" : "#ContentPlaceHolder1_Radiolist_noe_ashenaei > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)"}

            acquaintance_type = self.check(acquaintance_type_checklist)


            # Migration situation
            husband_migration_checklist = {"#ContentPlaceHolder1_RadioButtonList_mohajerat_zoj_0" : "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoj_1" : "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoj_2" : "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)"}
            husband_migration = self.check(husband_migration_checklist)

            wife_migration_checklist = {"#ContentPlaceHolder1_RadioButtonList_mohajerat_zoje_0" : "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                    "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoje_1" : "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                    "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoje_2" : "#ContentPlaceHolder1_RadioButtonList_mohajerat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)"}
            wife_migration = self.check(wife_migration_checklist)


            # Marriage type
            # husband
            husband_marriage_type_checklist = {"#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoj_0" : "#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                    "#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoj_1" : "#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_marriage_type = self.check(husband_marriage_type_checklist)


            # wife
            wife_marriage_type_checklist = {"#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoje_0" : "#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                    "#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoje_1" : "#ContentPlaceHolder1_Radiolist_noe_ezdevaj_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_marriage_type = self.check(wife_marriage_type_checklist)


            # parents consent
            husband_parents_consent_checklist = {"#ContentPlaceHolder1_Radiolist_rezayat_valedin_zoj_0" : "#ContentPlaceHolder1_Radiolist_rezayat_valedin_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_rezayat_valedin_zoj_1" : "#ContentPlaceHolder1_Radiolist_rezayat_valedin_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            now_husband_parents_consent_checklis = {"#ContentPlaceHolder1_Radiolist_iscontinue_zoj_0" : "#ContentPlaceHolder1_Radiolist_iscontinue_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_iscontinue_zoj_1" : "#ContentPlaceHolder1_Radiolist_iscontinue_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            wife_parents_consent_checklist = {"#ContentPlaceHolder1_Radiolist_rezayat_valedin_zojee_0" : "#ContentPlaceHolder1_Radiolist_rezayat_valedin_zojee > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_rezayat_valedin_zojee_1" : "#ContentPlaceHolder1_Radiolist_rezayat_valedin_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            now_wife_parents_consent_checklis = {"#ContentPlaceHolder1_Radiolist_iscontinue_zoje_0" : "#ContentPlaceHolder1_Radiolist_iscontinue_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_iscontinue_zoje_1" : "#ContentPlaceHolder1_Radiolist_iscontinue_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_parents_consent = self.check(husband_parents_consent_checklist)
            now_husband_parents_consent = self.check(now_husband_parents_consent_checklis)

            wife_parents_consent = self.check(wife_parents_consent_checklist)
            now_wife_parents_consent = self.check(now_wife_parents_consent_checklis)

            # Data set dictionary
            data_dict = {"نوع طلاق" : [divorce_type_textfield],
                        "متقاضی طلاق توافقی" : [Consensual_divorce_applicant],
                        "تاریخ ازدواج" : [marriage_date],
                        "سن زوج هنگام ازدواج" : [husband_Marriage_age_textfield],
                        "سن زوجه هنگام ازدواج" : [wife_marriage_age_textfield],
                        "تعداد سال زندگی مشترک" : [marriage_duration_year_textfield],
                        "تعداد ماه زندگی مشترک" : [marriage_duration_month_textfield],
                        "وضعیت فعلی زندگی مشترک" : [marriage_situation],
                        "سابقه آشنایی قبلی" : [dating_history],
                        "نوع آشنایی" : [acquaintance_type],
                        "وضعیت مهاجرت زوج" : [husband_migration],
                        "وضعیت مهاجرت زوجه" : [wife_migration],
                        "نوع ازدواج زوج" : [husband_marriage_type],
                        "نوع ازدواج زوجه" : [wife_marriage_type],
                        "وضعیت رضایت والدین زوج" : [husband_parents_consent],
                        "آیا ادامه دارد" : [now_husband_parents_consent],
                        "وضعیت رضایت والدین زوجه" : [wife_parents_consent],
                        "آیا ادامه دارد؟" : [now_wife_parents_consent]}

            # Adding each data to a
            self.form_arzyabi_avalie_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)

        except:
            data_dict = {"نوع طلاق" : [None],
                        "متقاضی طلاق توافقی" : [None],
                        "تاریخ ازدواج" : [None],
                        "سن زوج هنگام ازدواج" : [None],
                        "سن زوجه هنگام ازدواج" : [None],
                        "تعداد سال زندگی مشترک" : [None],
                        "تعداد ماه زندگی مشترک" : [None],
                        "وضعیت فعلی زندگی مشترک" : [None],
                        "سابقه آشنایی قبلی" : [None],
                        "نوع آشنایی" : [None],
                        "وضعیت مهاجرت زوج" : [None],
                        "وضعیت مهاجرت زوجه" : [None],
                        "نوع ازدواج زوج" : [None],
                        "نوع ازدواج زوجه" : [None],
                        "وضعیت رضایت والدین زوج" : [None],
                        "آیا ادامه دارد" : [None],
                        "وضعیت رضایت والدین زوجه" : [None],
                        "آیا ادامه دارد؟" : [None]}
            

            self.form_arzyabi_avalie_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)
            
            self.except_list.append(id)
            print(f"{WARNING}an exception occurred in arzyabi avalie..{ENDC}")
            logger.exception('an exception occurred in form arzyabi avalie')


    # get the form a
    def form_a(self, id):


        # Dataset to add data to it by loop
        dataset = pd.DataFrame()

        try:

            # Getting target page for each id
            url = f"https://tasmim.behzisti.net/gh_alef.aspx?id={id}"
            driver.get(url)

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            #Get page source to find elements in
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            self.soup = soup


            #Part 1

            # Child Involvement in Marital Relationship
            tag = soup.select_one("#ContentPlaceHolder1_tb_mizan_dekhalate_farzandan")
            child_involvement_in_marital_relationship_textfield = self.text_field_collector(tag)



            # The mount of agreement in children's education
            tag = soup.select_one("#ContentPlaceHolder1_tb_mizan_tavafogh_tarbiat_farzandan")
            agreement_in_child_education_textfield = self.text_field_collector(tag)


            # Children's social and physical problems and issues
            tag = soup.select_one("#ContentPlaceHolder1_tb_moshkelat_farzandan")
            children_social_and_physical_problems_textfield = self.text_field_collector(tag)


            # How long has it been since the problem started?
            time_spended_scince_start_checklist =  {'#ContentPlaceHolder1_Radiolist_aghaze_moshkel_0' : '#ContentPlaceHolder1_Radiolist_aghaze_moshkel > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_aghaze_moshkel_1' : '#ContentPlaceHolder1_Radiolist_aghaze_moshkel > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_aghaze_moshkel_2' : '#ContentPlaceHolder1_Radiolist_aghaze_moshkel > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_aghaze_moshkel_3' : '#ContentPlaceHolder1_Radiolist_aghaze_moshkel > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)'

            }
            time_spended_scince_start = self.check(time_spended_scince_start_checklist)

            # Is there a history of reconciliation?
            history_of_reconciliation_checklist = {'#ContentPlaceHolder1_Radiolist_motareke_0' : '#ContentPlaceHolder1_Radiolist_motareke > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_motareke_1' : '#ContentPlaceHolder1_Radiolist_motareke > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            history_of_reconciliation = self.check(history_of_reconciliation_checklist)


            # The duration of the truce

            # Day
            tag = soup.select_one("#ContentPlaceHolder1_tb_modate_motareke_rooz")
            truce_day_textfield = self.text_field_collector(tag)

            # Month
            tag = soup.select_one("#ContentPlaceHolder1_tb_modat_motareke_mah")
            truce_month_textfield = self.text_field_collector(tag)


            # Year
            tag = soup.select_one("#ContentPlaceHolder1_tb_modate_motareke_sal")
            truce_year_textfield = self.text_field_collector(tag)


            # Number of times
            tag = soup.select_one("#ContentPlaceHolder1_tb_tadad_motareke")
            truce_times_textfield = self.text_field_collector(tag)


            ###################################

            # Part 2

            go_to_part_2_button = driver.find_element(By.ID , 'wizard-t-1')
            go_to_part_2_button.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            # History of divorce in couples

            # Husband
            husband_divorce_history_checklist  = {'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoj_0':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoj_1':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_divorce_history = self.check(husband_divorce_history_checklist)

            # Wife
            wife_divorce_history_checklist  = {'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoje_0':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoje_1':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_divorce_history = self.check(wife_divorce_history_checklist)


            #Previous marriage history in couples

            # Husband
            husband_marriage_history_checklist  = {'#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoj_0':'#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoj_1':'#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_marriage_history = self.check(husband_marriage_history_checklist)


            # Wife
            wife_marriage_history_checklist  = {'#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoje_0':'#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoje_1':'#ContentPlaceHolder1_Radiolist_sabeghe_ezdevaj_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_marriage_history = self.check(wife_marriage_history_checklist)


            # History of divorce in the couple's family:

            # Husband
            husband_family_divorce_history_checklist  = {'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoj_0':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoj_1':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_family_divorce_history = self.check(husband_family_divorce_history_checklist)


            # Wife
            wife_family_divorce_history_checklist  = {'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoje_0':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoje_0':'#ContentPlaceHolder1_Radiolist_sabeghe_talaghe_khanevade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_family_divorce_history = self.check(wife_family_divorce_history_checklist)


            # The degree of adherence to religious issues:

            # Husband
            husband_religious_level_checklist  = {'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj_0':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj_1':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj_2':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj_3':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj_4':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)'

            }
            husband_religious_level = self.check(husband_religious_level_checklist)


            # Wife
            wife_religious_level_checklist  = {'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje_0':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje_1':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje_2':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje_3':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)'  ,
                                    '#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj_4':'#ContentPlaceHolder1_RadioButtonList_mizan_paybandi_mazhabi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)'

            }
            wife_religious_level = self.check(wife_religious_level_checklist)


            # Are the couples related to each other religiously?
            related_religiously_couples_checklist = {'#ContentPlaceHolder1_RadioButtonList_senkhaiat_mazhabi_0' : '#ContentPlaceHolder1_RadioButtonList_senkhaiat_mazhabi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_RadioButtonList_senkhaiat_mazhabi_1' : '#ContentPlaceHolder1_RadioButtonList_senkhaiat_mazhabi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_RadioButtonList_senkhaiat_mazhabi_2' : '#ContentPlaceHolder1_RadioButtonList_senkhaiat_mazhabi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)'}

            related_religiously_couples = self.check(related_religiously_couples_checklist)



            ###################################

            # Part 3
            go_to_part_3_button = driver.find_element(By.ID , 'wizard-t-2')
            go_to_part_3_button.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))


            #Employment status of the couple

            # Husband
            husband_employment_status_checklist = {'#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj_0' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj_1' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj_2' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj_3' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj_4' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj_5' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > span:nth-child(1) > label:nth-child(2)' ,

            }
            husband_employment_status = self.check(husband_employment_status_checklist)


            # Wife
            wife_employment_status_checklist = {'#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje_0' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje_1' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje_2' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje_3' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje_4' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1) > label:nth-child(2)' ,
                                    '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje_5' : '#ContentPlaceHolder1_Radio_vaziate_shoghle_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > span:nth-child(1) > label:nth-child(2)' ,

            }
            wife_employment_status = self.check(wife_employment_status_checklist)



            # Job Title

            # Husband
            tag =  soup.select_one("#ContentPlaceHolder1_tb_shoghle_jaz")
            husband_job_title_textfield = self.text_field_collector(tag)


            # Wife
            tag =  soup.select_one("#ContentPlaceHolder1_tb_shoghle_jaze")
            wife_job_title_textfield = self.text_field_collector(tag)



            # Income (Toman)

            # Husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_mizan_daramad_zoj")
            husband_income_textfield = self.text_field_collector(tag)


            # Wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_mizan_daramad_zoje")
            wife_income_textfield = self.text_field_collector(tag)

            #How to cover living expenses

            cover_living_expenses_checklist = {'#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi_0' : '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi_1' : '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi_2' : '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi_3' : '#ContentPlaceHolder1_Radiolist_tamin_hazineha_zendegi > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)'


            }
            cover_living_expenses = self.check(cover_living_expenses_checklist)




            # Financial responsibility

            # Husband
            husband_finance_responsiblity_checklist = { '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoj_0' : '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                        '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoj_1' : '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_finance_responsiblity = self.check(husband_finance_responsiblity_checklist)



            # Wife
            wife_finance_responsiblity_checklist = { '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoje_0' : '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                        '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoje_1' : '#ContentPlaceHolder1_Radiolist_masoliat_mali_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_finance_responsiblity = self.check(wife_finance_responsiblity_checklist)


            # Has financial bankruptcy ever happened in married couples' families

            # Husband
            husband_bankruptcy_in_family_checklist  = {'#ContentPlaceHolder1_Radiolist_varshekasti_zoj_0' : '#ContentPlaceHolder1_Radiolist_varshekasti_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_varshekasti_zoj_1' : '#ContentPlaceHolder1_Radiolist_varshekasti_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_bankruptcy_in_family = self.check(husband_bankruptcy_in_family_checklist)


            # Wife
            wife_bankruptcy_in_family_checklist = {'#ContentPlaceHolder1_Radiolist_varshekasti_zoje_0' : '#ContentPlaceHolder1_Radiolist_varshekasti_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_varshekasti_zoje_1' : '#ContentPlaceHolder1_Radiolist_varshekasti_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_bankruptcy_in_family = self.check(wife_bankruptcy_in_family_checklist)


            data_dict = { 'میزان دخالت فرزندان بر روابط زناشویی زوجین:' : [child_involvement_in_marital_relationship_textfield] ,
                        'میزان توافق در امورتربیتی فرزندان :' : [agreement_in_child_education_textfield] ,
                        'مشکلات و مسائل اجتماعی و جسمانی فرزندان :' : [children_social_and_physical_problems_textfield] ,
                        'از زمان شروع مشکل چقدر گذشته است ؟' : [time_spended_scince_start] ,
                        'سابقه متارکه ؟' : [history_of_reconciliation] ,
                        'تعداد روز متارکه' : [truce_day_textfield] ,
                        'تعداد ماه متارکه' : [truce_month_textfield] ,
                        'تعداد ماه متارکه ' : [truce_year_textfield] ,
                        'تعداد دفعات متارکه' : [truce_times_textfield],
                        'سابقه طلاق در زوج' : [husband_divorce_history] ,
                        'سابقه طلاق در زوجه' : [wife_divorce_history] ,
                        'سابقه ازدواج قبلی در زوج' : [husband_marriage_history] ,
                        'سابقه ازدواج قبلی در زوجه' : [wife_marriage_history] ,
                        'سابقه طلاق در خانواده زوج' : [husband_family_divorce_history] ,
                        'سابقه طلاق در خانواده زوجه' : [wife_family_divorce_history] ,
                        'میزان پایبندی زوج به مسائل مذهبی' : [husband_religious_level] ,
                        'میزان پایبندی زوجه به مسائل مذهبی' : [wife_religious_level] ,
                        'آیا از بعد مذهبی زوجین با یکدیگر سنخیت دارند؟' : [related_religiously_couples] ,
                        'وضعیت شغلی زوج' : [husband_employment_status] ,
                        'شغل زوج' : [husband_job_title_textfield] ,
                        'میزان درامد زوج' : [husband_income_textfield] ,
                        'وضعیت شغلی زوجه' : [wife_employment_status] ,
                        'شغل زوجه' : [wife_job_title_textfield] ,
                        'میزان درامد زوجه' : [wife_income_textfield] ,
                        'نحوه تامین هزینه های زندگی' : [cover_living_expenses] ,
                        'مسئولیت پذیری مالی زوج' : [husband_finance_responsiblity] ,
                        'مسئولیت پذیری مالی زوجه' : [wife_finance_responsiblity] ,
                        'ایا تا کنون ورشکستگی مالی در خانواده زوج اتفاق افتاده است ؟' : [husband_bankruptcy_in_family] ,
                        'ایا تا کنون ورشکستگی مالی در خانواده زوجه اتفاق افتاده است ؟' : [wife_bankruptcy_in_family]

            }


            # Adding each data to a
            self.form_a_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)


        except:
            data_dict = { 'میزان دخالت فرزندان بر روابط زناشویی زوجین:' : [None] ,
                        'میزان توافق در امورتربیتی فرزندان :' : [None] ,
                        'مشکلات و مسائل اجتماعی و جسمانی فرزندان :' : [None] ,
                        'از زمان شروع مشکل چقدر گذشته است ؟' : [None] ,
                        'سابقه متارکه ؟' : [None] ,
                        'تعداد روز متارکه' : [None] ,
                        'تعداد ماه متارکه' : [None] ,
                        'تعداد ماه متارکه ' : [None] ,
                        'تعداد دفعات متارکه' : [None],
                        'سابقه طلاق در زوج' : [None] ,
                        'سابقه طلاق در زوجه' : [None] ,
                        'سابقه ازدواج قبلی در زوج' : [None] ,
                        'سابقه ازدواج قبلی در زوجه' : [None] ,
                        'سابقه طلاق در خانواده زوج' : [None] ,
                        'سابقه طلاق در خانواده زوجه' : [None] ,
                        'میزان پایبندی زوج به مسائل مذهبی' : [None] ,
                        'میزان پایبندی زوجه به مسائل مذهبی' : [None] ,
                        'آیا از بعد مذهبی زوجین با یکدیگر سنخیت دارند؟' : [None] ,
                        'وضعیت شغلی زوج' : [None] ,
                        'شغل زوج' : [None] ,
                        'میزان درامد زوج' : [None] ,
                        'وضعیت شغلی زوجه' : [None] ,
                        'شغل زوجه' : [None] ,
                        'میزان درامد زوجه' : [None] ,
                        'نحوه تامین هزینه های زندگی' : [None] ,
                        'مسئولیت پذیری مالی زوج' : [None] ,
                        'مسئولیت پذیری مالی زوجه' : [None] ,
                        'ایا تا کنون ورشکستگی مالی در خانواده زوج اتفاق افتاده است ؟' : [None] ,
                        'ایا تا کنون ورشکستگی مالی در خانواده زوجه اتفاق افتاده است ؟' : [None]

            }

            

            self.form_a_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)
            
            self.except_list.append(id)
            print(f"{WARNING}an exception occurred in form alef..{ENDC}")
            logger.exception('exception in form a')


    # get the form b
    def form_b(self, id):

        # Dataset to add data to it by loop
        dataset = pd.DataFrame()

        try:
            # Getting target page for each id
            url = f"https://tasmim.behzisti.net/gh_be.aspx?id={id}"
            driver.get(url)

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            #Get page source to find elements in
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            self.soup = soup


            #Part 1

            # Addection History

            # Husband
            husband_addiction_history_checklist = {'#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoj_0' : '#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoj_1' : '#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'
            }
            husband_addiction_history = self.check(husband_addiction_history_checklist)

            # Wife
            wife_addiction_history_checklist = {'#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoje_0' : '#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoje_1' : '#ContentPlaceHolder1_Radiolist_sabeghe_etiad_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'
            }
            wife_addiction_history = self.check(wife_addiction_history_checklist)

            # Addiction Type

            # Husband
            husband_addiction_type_checkbox = {'#ContentPlaceHolder1_CheckList_noe_etiad_zoj_0' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckList_noe_etiad_zoj_1' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckList_noe_etiad_zoj_2' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckList_noe_etiad_zoj_3' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckList_noe_etiad_zoj_4' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckList_noe_etiad_zoj_5' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckList_noe_etiad_zoj_6' : '#ContentPlaceHolder1_CheckList_noe_etiad_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(7) > label:nth-child(2)'

            }
            husband_addiction_type = self.check(husband_addiction_type_checkbox)

            # Wife
            wife_addiction_type_checkbox = {'#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_0' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_1' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_2' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_3' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_4' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_5' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje_6' : '#ContentPlaceHolder1_CheckBoxList_noe_etiade_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(7) > label:nth-child(2)'

            }
            wife_addiction_type = self.check(wife_addiction_type_checkbox)


            # Consumption of alcoholic

            # Husband
            husband_alchol_consumption_checklist = { '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoj_0' : '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoj_1' : '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_alchol_consumption = self.check(husband_alchol_consumption_checklist)


            # Wife
            wife_alchol_consumption_checklist = { '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoje_0' : '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoje_1' : '#ContentPlaceHolder1_Radiolist_masraf_mashrobat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_alchol_consumption = self.check(wife_alchol_consumption_checklist)


            ###########################
            
            
            # Part 2

            go_to_part_2_button = driver.find_element(By.ID , 'wizard-t-1')
            go_to_part_2_button.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))


            is_the_husband_interested_in_the_wife_checklist = {'#ContentPlaceHolder1_Radiolist_alaghe_zoj_be_zoje_0' : '#ContentPlaceHolder1_Radiolist_alaghe_zoj_be_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                            '#ContentPlaceHolder1_Radiolist_alaghe_zoj_be_zoje_1' : '#ContentPlaceHolder1_Radiolist_alaghe_zoj_be_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            is_the_husband_interested_in_the_wife = self.check(is_the_husband_interested_in_the_wife_checklist)

            is_the_wife_interested_in_the_husband_checklist = {'#ContentPlaceHolder1_Radiolist_alaghe_zoje_be_zoj_0' : '#ContentPlaceHolder1_Radiolist_alaghe_zoje_be_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                            '#ContentPlaceHolder1_Radiolist_alaghe_zoje_be_zoj_1' : '#ContentPlaceHolder1_Radiolist_alaghe_zoje_be_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            is_the_wife_interested_in_the_husband = self.check(is_the_wife_interested_in_the_husband_checklist)

            # History of visiting the counseling center

            # Husband
            husband_counseling_visiting_checklist = {'#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoj_0' : '#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)',
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoj_1' : '#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_counseling_visiting = self.check(husband_counseling_visiting_checklist)

            tag = soup.select_one("#ContentPlaceHolder1_tb_noe_moshkel_moshavere_zoj")
            husband_problem_type_textfield = self.text_field_collector(tag)

                

            tag = soup.select_one("#ContentPlaceHolder1_tb_nazar_karshenas_baraye_moshavere_zoj")
            husband_expert_opinion_textfield = self.text_field_collector(tag)


            # Wife
            wife_counseling_visiting_checklist = {'#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoje_0' : '#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)',
                                                '#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoje_1' : '#ContentPlaceHolder1_Radiolist_sabeghe_morajee_be_moshavere_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_counseling_visiting = self.check(wife_counseling_visiting_checklist)

            tag = soup.select_one("#ContentPlaceHolder1_tb_noe_moshkel_moshavere_zoje")
            wife_problem_type_textfield = self.text_field_collector(tag)

            

            tag = soup.select_one("#ContentPlaceHolder1_tb_nazar_karshenas_baraye_moshavere_zoje")
            wife_expert_opinion_textfield = self.text_field_collector(tag)


            # Do couples have supportive families or do not

            # Husband
            husband_supportive_family_checklist = {'#ContentPlaceHolder1_Radiolist_hemayatgar_zoj_0' : '#ContentPlaceHolder1_Radiolist_hemayatgar_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_hemayatgar_zoj_1' : '#ContentPlaceHolder1_Radiolist_hemayatgar_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            husband_supportive_family = self.check(husband_supportive_family_checklist)

            # Wife
            wife_supportive_family_checklist = {'#ContentPlaceHolder1_Radiolist_hemayatgar_zoje_0' : '#ContentPlaceHolder1_Radiolist_hemayatgar_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_hemayatgar_zoje_1' : '#ContentPlaceHolder1_Radiolist_hemayatgar_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            wife_supportive_family = self.check(wife_supportive_family_checklist)


            ######################################


            # Part 3

            go_to_part_3_button = driver.find_element(By.ID , 'wizard-t-2')
            go_to_part_3_button.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            # Do couples have an interfering family ot do not

            # husband
            husband_interfering_family_checklist = {'#ContentPlaceHolder1_Radiolist_modakhelegar_zoj_0' : '#ContentPlaceHolder1_Radiolist_modakhelegar_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_modakhelegar_zoj_1' : '#ContentPlaceHolder1_Radiolist_modakhelegar_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,

            }
            husband_interfering_family = self.check(husband_interfering_family_checklist)

            # Wife
            wife_interfering_family_checklist = {'#ContentPlaceHolder1_Radiolist_modakhelegar_zoje_0' : '#ContentPlaceHolder1_Radiolist_modakhelegar_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                '#ContentPlaceHolder1_Radiolist_modakhelegar_zoje_1' : '#ContentPlaceHolder1_Radiolist_modakhelegar_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,

            }
            wife_interfering_family = self.check(wife_interfering_family_checklist)

            # Does the couple have a history of physical illness or doesn't

            # Husband
            is_husband_physical_illness_history_checklist = {'#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoj_0' : '#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                            '#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoj_1' : '#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            is_husband_physical_illness_history = self.check(is_husband_physical_illness_history_checklist)

            tag = soup.select_one("#ContentPlaceHolder1_tb_noe_bimari_zoj")
            husband_physical_illness_type_textfield = self.text_field_collector(tag)


            # Wife
            is_wife_physical_illness_history_checklist = {'#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoje_0' : '#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                                            '#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoje_1' : '#ContentPlaceHolder1_Radiolist_sabeghe_bimari_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'

            }
            is_wife_physical_illness_history= self.check(is_wife_physical_illness_history_checklist)
            
            tag = soup.select_one("#ContentPlaceHolder1_tb_noe_bimari_zoje")
            wife_physical_illness_type_textfield = self.text_field_collector(tag)


            # Husband
            husband_disability_checklist = {'#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoj_0': '#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoj_1': '#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,

            }
            husband_disability = self.check(husband_disability_checklist)

            # Wife
            wife_disability_checklist = {'#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoje_0': '#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)' ,
                                            '#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoje_1': '#ContentPlaceHolder1_Radiolist_ekhtelale_fiziki_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)' ,

            }
            wife_disability = self.check(wife_disability_checklist)



            data_dict = {
            'سابقه اعتیاد زوج ' : [husband_addiction_history] ,
            'سابقه اعتیاد زوجه' : [wife_addiction_history] ,
            'نوع اعتیاد زوج' : [husband_addiction_type] ,
            'نوع اعتیاد زوجه' : [wife_addiction_type] ,
            'مصرف مشروبات الکلی زوج' : [husband_alchol_consumption] ,
            'مصرف مشروبات الکلی زوجه' : [wife_alchol_consumption] ,
            'آیا زوج به زوجه علاقه مند است' : [is_the_husband_interested_in_the_wife] ,
            'آیا زوجه به زوج علاقه مند است' : [is_the_wife_interested_in_the_husband] ,
            'سابقه مراجعه زوج به مرکز مشاوره' : [husband_counseling_visiting] ,
            'سابقه مراجعه زوجه به مرکز مشاوره' : [wife_counseling_visiting] ,
            'نوع مشکل زوج در هنگام مراجعه به مرکز مشاوره' : [husband_problem_type_textfield] ,
            'نوع مشکل زوجه در هنگام مراجعه به مرکز مشاوره' : [wife_problem_type_textfield] ,
            ' نظر کارشناس در مراجعه زوج به مرکز مشاوره' : [husband_expert_opinion_textfield] ,
            ' نظر کارشناس در مراجعه زوجه به مرکز مشاوره' : [wife_expert_opinion_textfield] ,
            'آیا زوج خانواده حمایتگری دارد ' : [husband_supportive_family] ,
            'آیا زوجه خانواده حمایتگری دارد ' : [wife_supportive_family] ,
            'آیا زوج خانواده مداخله گر دارد' : [husband_interfering_family] ,
            'آیا زوجه خانواده مداخله گر دارد' : [wife_interfering_family] ,
            'آیا زوج سابقه بیماری جسمی دارد' : [is_husband_physical_illness_history] ,
            'آیا زوجه سابقه بیماری جسمی دارد' : [is_wife_physical_illness_history] ,
            'نوع بیماری زوج' : [husband_physical_illness_type_textfield] ,
            'نوع بیماری زوجه' : [wife_physical_illness_type_textfield] ,
            'اختلال فیزیکی (معلولیت) زوج' : [husband_disability] ,
            'اختلال فیزیکی (معلولیت) زوجه' : [wife_disability]

            }


            # Adding each data to b dataframe
            self.form_b_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)


        except:
            data_dict = {
            'سابقه اعتیاد زوج ' : [None] ,
            'سابقه اعتیاد زوجه' : [None] ,
            'نوع اعتیاد زوج' : [None] ,
            'نوع اعتیاد زوجه' : [None] ,
            'مصرف مشروبات الکلی زوج' : [None] ,
            'مصرف مشروبات الکلی زوجه' : [None] ,
            'آیا زوج به زوجه علاقه مند است' : [None] ,
            'آیا زوجه به زوج علاقه مند است' : [None] ,
            'سابقه مراجعه زوج به مرکز مشاوره' : [None] ,
            'سابقه مراجعه زوجه به مرکز مشاوره' : [None] ,
            'نوع مشکل زوج در هنگام مراجعه به مرکز مشاوره' : [None] ,
            'نوع مشکل زوجه در هنگام مراجعه به مرکز مشاوره' : [None] ,
            ' نظر کارشناس در مراجعه زوج به مرکز مشاوره' : [None] ,
            ' نظر کارشناس در مراجعه زوجه به مرکز مشاوره' :[None] ,
            'آیا زوج خانواده حمایتگری دارد ' : [None] ,
            'آیا زوجه خانواده حمایتگری دارد ' : [None] ,
            'آیا زوج خانواده مداخله گر دارد' : [None] ,
            'آیا زوجه خانواده مداخله گر دارد' : [None] ,
            'آیا زوج سابقه بیماری جسمی دارد' : [None] ,
            'آیا زوجه سابقه بیماری جسمی دارد' : [None] ,
            'نوع بیماری زوج' : [None] ,
            'نوع بیماری زوجه' : [None] ,
            'اختلال فیزیکی (معلولیت) زوج' : [None] ,
            'اختلال فیزیکی (معلولیت) زوجه' : [None]

            }
            
            self.form_b_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)

            self.except_list.append(id)
            print(f"{WARNING}an exception occurred in form b..{ENDC}")
            logger.exception('exception in form b')


    # get the form g
    def form_g(self, id):

        # Function to check checkboxes
        def checkbox(checklist):
            for i in checklist:
                if driver.find_element(By.CSS_SELECTOR, i).is_selected():
                    return driver.find_element(By.CSS_SELECTOR, checklist[i]).text
                else:
                    pass


        # Dataset to add data to it by loop
        dataset = pd.DataFrame()


        try:

            # First page
            # Getting target's data
            url = f"https://tasmim.behzisti.net/gh_jim.aspx?id={id}"
            driver.get(url)

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            #Get page source to find elements in
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            self.soup = soup


            # mental illness hostory
            husband_mental_illness_history_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoj_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoj_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            husband_mental_illness_history = self.check(husband_mental_illness_history_checklist)


            wife_mental_illness_history_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoje_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                            "#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoje_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_bimari_ravani_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            wife_mental_illness_history = self.check(wife_mental_illness_history_checklist)


            # psychiatric hospital hospitalization history check
            husband_psychiatric_hospital_hospitalization_history_checklist = {"#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoj_0" : "#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                                    "#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoj_1" : "#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            husband_psychiatric_hospital_hospitalization_history = self.check(husband_psychiatric_hospital_hospitalization_history_checklist)

            wife_psychiatric_hospital_hospitalization_history_checklist = {"#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoje_0" : "#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                                            "#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoje_1" : "#ContentPlaceHolder1_Radiolist_bastari_asabo_ravan_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            wife_psychiatric_hospital_hospitalization_history = self.check(wife_psychiatric_hospital_hospitalization_history_checklist)

            # History of domestic violence
            husband_domestic_violence_History_checklist = {"#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj_0" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj_1" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj_2" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj_3" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)"}
            husband_domestic_violence_History = checkbox(husband_domestic_violence_History_checklist)

            wife_domestic_violence_History_checklist = {"#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje_0" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje_1" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje_2" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje_3" : "#ContentPlaceHolder1_CheckBoxList_sabeghe_khoshonat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > label:nth-child(2)"}
            wife_domestic_violence_History = checkbox(wife_domestic_violence_History_checklist)

            # Forensic medicine
            husband_forensic_medicine_reference_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoj_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoj_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_forensic_medicine_reference = self.check(husband_forensic_medicine_reference_checklist)

            wife_forensic_medicine_reference_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoje_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoje_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_pezeshki_khoshonat_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_forensic_medicine_reference = self.check(wife_forensic_medicine_reference_checklist)

            # Reference to police
            husband_police_reference_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoj_0" :"#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoj_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_police_reference = self.check(husband_police_reference_checklist)

            wife_police_reference_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoje_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                            "#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoje_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_moraje_be_marje_gazaei_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}

            wife_police_reference = self.check(wife_police_reference_checklist)


            ################

            # Second page
            # Clicking on the next page link
            next_page_link = driver.find_element(By.CSS_SELECTOR, "#wizard-t-1")
            next_page_link.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))


            # Getting new page's content
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")



            # Checking how to have sex
            husband_have_sex_checklist = {"#ContentPlaceHolder1_Radiolist_rabete_jensi_zoj_0" : "#ContentPlaceHolder1_Radiolist_rabete_jensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_rabete_jensi_zoj_1" : "#ContentPlaceHolder1_Radiolist_rabete_jensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_have_sex = self.check(husband_have_sex_checklist)
            wife_have_sex_checklist = {"#ContentPlaceHolder1_Radiolist_rabete_jensi_zoje_0" : "#ContentPlaceHolder1_Radiolist_rabete_jensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                    "#ContentPlaceHolder1_Radiolist_rabete_jensi_zoje_1" : "#ContentPlaceHolder1_Radiolist_rabete_jensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_have_sex = self.check(wife_have_sex_checklist)


            # Checking sex type
            husband_sex_type_checklist = {"#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoj_0" : "#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoj_1" : "#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_sex_type = self.check(husband_sex_type_checklist)

            wife_sex_type_checklist =   {"#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoje_0" : "#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                        "#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoje_1" : "#ContentPlaceHolder1_Radiolist_noe_rabete_jensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_sex_type = self.check(wife_sex_type_checklist)


            # checking Sexual dysfunction
            husband_sexual_dysfunction_checklist = {"#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoj_0" : "#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoj_1" : "#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_sexual_dysfunction = self.check(husband_sexual_dysfunction_checklist)

            wife_sexual_dysfunction_checklist = {"#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoje_0" : "#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoje_1" : "#ContentPlaceHolder1_Radiolist_ekhtele_dar_konesh_jensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_sexual_dysfunction = self.check(wife_sexual_dysfunction_checklist)


            # Checking sexual dissatisfaction
            husband_sexual_dissatisfaction_checklist = {"#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoj_0" : "#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                            "#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoj_1" : "#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_sexual_dissatisfaction = self.check(husband_sexual_dissatisfaction_checklist)

            wife_sexual_dissatisfaction_checklist = {"#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoje_0" : "#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoje_1" : "#ContentPlaceHolder1_RadioButtonList_narezayati_gensi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_sexual_dissatisfaction = self.check(wife_sexual_dissatisfaction_checklist)


            # Checking Extramarital relationships
            husband_extramarital_relationships_checklist = {"#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoj_0" : "#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                            "#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoj_1" : "#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_extramarital_relationships = self.check(husband_extramarital_relationships_checklist)

            wife_extramarital_relationships_checklist = {"#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoje_0" : "#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoje_1" : '#ContentPlaceHolder1_Radiolist_ravabete_fara_jazashoei_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)'}
            wife_extramarital_relationships = self.check(wife_extramarital_relationships_checklist)


            # Cehcking history of judicial action for divorce
            husband_divorce_judicial_action_history_checklit = {"#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoj_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoj_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_divorce_judicial_action_history = self.check(husband_divorce_judicial_action_history_checklit)

            wife_divorce_judicial_action_history_checklit = {"#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoje_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                            "#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoje_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_eghdame_ghazaei_talaghe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_divorce_judicial_action_history = self.check(wife_divorce_judicial_action_history_checklit)


            # divorce judicial action counter
            # husband
            tag = soup.select_one("#ContentPlaceHolder1_tb_tedad_eghdame_ghazaei_talagh_zoj")
            husband_divorce_judicial_action_number_textfield = self.text_field_collector(tag)

                
            
            # wife
            tag = soup.select_one("#ContentPlaceHolder1_tb_tedad_eghdame_ghazaei_talagh_zoje")
            wife_divorce_judicial_action_number_textfield = self.text_field_collector(tag)


            ###############

            # Third page
            # Clicking on the next page link
            next_page_link = driver.find_element(By.CSS_SELECTOR, "#wizard-t-2")
            next_page_link.click()

            # wait for all elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))

            # Getting new page's content
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")



            # checking Conviction record
            husband_conviction_record_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoj_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoj_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_conviction_record = self.check(husband_conviction_record_checklist)

            wife_conviction_record_checklist = {"#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoje_0" : "#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                "#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoje_1" : "#ContentPlaceHolder1_Radiolist_sabeghe_mahkomit_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_conviction_record = self.check(wife_conviction_record_checklist)

            # husband conviction type
            tag = soup.select_one("#ContentPlaceHolder1_tb_noe_mahkomiat_zoj")
            husband_conviction_type_textfield = self.text_field_collector(tag)


            # husband conviction type
            tag = soup.select_one("#ContentPlaceHolder1_tb_noe_mahkomiat_zoje")
            wife_conviction_type_textfield = self.text_field_collector(tag)


            # checking Consequences of family disputes
            husband_family_disputes_consequences_checklist = {"#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_0" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_1" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_2" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_3" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_4" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_5" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_6" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_7" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_8" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_9" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_10" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj_11" : "#ContentPlaceHolder1_CheckList_tabaate_ekhtelafe_zoj > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3) > label:nth-child(2)"}
            husband_family_disputes_consequences = checkbox(husband_family_disputes_consequences_checklist)

            wife_family_disputes_consequences_checklist = {"#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_0" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                            "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_1" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)",
                                                            "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_2" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > label:nth-child(2)",
                                                            "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_3" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_4" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_5" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_6" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_7" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_8" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_9" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_10" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje_11" : "#ContentPlaceHolder1_CheckBoxList_tabaate_ekhtelafe_zoje > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3) > label:nth-child(2)"}
            wife_family_disputes_consequences = checkbox(wife_family_disputes_consequences_checklist)

            # Collecting divorce reason
            # clicking to go to part 3
            wait = WebDriverWait(driver, 10)
            part_3 = driver.find_element(By.ID ,'wizard-t-2')
            part_3.click()
            # time.sleep(1)
            open_bar_1 =  driver.find_element(By.CSS_SELECTOR , 'div.input-field:nth-child(9) > div:nth-child(2) > input:nth-child(2)')
            open_bar_1.click()
            active_li_elements1 = driver.find_elements(By.CSS_SELECTOR , 'li.active')
            husband_divorce_reason_textfield =[]
            for li_element in active_li_elements1:
                span_elements = li_element.find_elements(By.TAG_NAME , "span")
                for span_element in span_elements:
                    husband_divorce_reason_textfield.append(span_element.text)
                
            
            # # click to go to part 2 to hide the opened bar
            # time.sleep(1)
            open_bar_2 =  driver.find_element(By.CSS_SELECTOR , 'div.s12:nth-child(11) > div:nth-child(2) > input:nth-child(2)')
            open_bar_2.click()
            active_li_elements2 = driver.find_elements(By.CSS_SELECTOR , 'li.active')

            wife_divorce_reason_textfield =[]
            for li_element in active_li_elements2:
                span_elements = li_element.find_elements(By.TAG_NAME , "span")
                for span_element in span_elements:
                    wife_divorce_reason_textfield.append(span_element.text)
            
            
      

            # mental status check need
            husband_mental_status_check_need_checklist = {"#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoj_0" : "#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                        "#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoj_1" : "#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoj > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            husband_mental_status_check_need = self.check(husband_mental_status_check_need_checklist)

            wife_mental_status_check_need_checklist = {"#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoje_0" : "#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > label:nth-child(2)",
                                                    "#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoje_1" : "#ContentPlaceHolder1_Radiolist_neyaz_baresi_roohi_zoje > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2)"}
            wife_mental_status_check_need = self.check(wife_mental_status_check_need_checklist)



            data_dict = {"سابقه بیماری روانی زوج" : [husband_mental_illness_history],
                        "سابقه بیماری روانی زوجه" : [wife_mental_illness_history],
                        "سابقه بستری در بیمارستان اعصاب و روان زوج" : [husband_psychiatric_hospital_hospitalization_history],
                        "سابقه بستری در بیمارستان اعصاب و روان زوجه" : [wife_psychiatric_hospital_hospitalization_history],
                        "سابقه خشونت های خانگی زوج" : [husband_domestic_violence_History],
                        "سابقه خشونت های خانگی زوجه" : [wife_domestic_violence_History],
                        "سابقه مراجعه به پزشکی قانونی به دلیل خشونت خانگی، زوج" : [husband_forensic_medicine_reference],
                        "سابقه مراجعه به پزشکی قانونی به دلیل خشونت خانگی، زوجه" : [wife_forensic_medicine_reference],
                        "سابقه مراجعه به مراجع انتظامی به دلیل خشونت، زوج" : [husband_police_reference],
                        "سابقه مراجعه به مراجع انتظامی به دلیل خشونت، زوجه" : [wife_police_reference],
                        "نحوه رابطه جنسی زوج" : [husband_have_sex],
                        "نحوه رابطه جنسی زوجه" : [wife_have_sex],
                        "نوع رابطه جنسی زوج" : [husband_sex_type],
                        "نوع رابطه جنسی زوجه" : [wife_sex_type],
                        "اختلال در مراحل کنش جنسی زوج" : [husband_sexual_dysfunction],
                        "اختلال در مراحل کنش جنسی زوجه" : [wife_sexual_dysfunction],
                        "نارضایتی جنسی زوج" : [husband_sexual_dissatisfaction],
                        "نارضایتی جنسی زوجه" : [wife_sexual_dissatisfaction],
                        "روابط فرا زناشویی، زوج" : [husband_extramarital_relationships],
                        "روابط فرا زناشویی، زوجه" : [wife_extramarital_relationships],
                        "سابقه اقدام قضایی قبلی در خصوص طلاق زوج" : [husband_divorce_judicial_action_history],
                        "تعداد اقدامات زوج" : [husband_divorce_judicial_action_number_textfield],
                        "تعداد اقدامات زوجه" : [wife_divorce_judicial_action_number_textfield],
                        "سابقه اقدام قضایی قبلی در خصوص طلاق زوجه" : [wife_divorce_judicial_action_history],
                        "سابقه محکومیت زوج" : [husband_conviction_record],
                        "نوع محکومیت زوج" : [husband_conviction_type_textfield],
                        "سابقه محکومیت زوجه" : [wife_conviction_record],
                        "نوع محکومیت زوجه" : [wife_conviction_type_textfield],
                        "تبعات اختلافات خانوادگی برای زوج" :  [husband_family_disputes_consequences],
                        "تبعات اختلافات خانوادگی برای زوجه" :  [wife_family_disputes_consequences],
                        "دلایل طلاق زوج" : [husband_divorce_reason_textfield],
                        "دلایل طلاق زوجه" : [wife_divorce_reason_textfield],
                        "نیاز به بررسی وضعیت روحی زوج" : [husband_mental_status_check_need],
                        "نیاز به بررسی وضعیت روحی زوجه" : [wife_mental_status_check_need]}


            self.form_g_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)

        except:
            data_dict = {"سابقه بیماری روانی زوج" : [None],
                        "سابقه بیماری روانی زوجه" : [None],
                        "سابقه بستری در بیمارستان اعصاب و روان زوج" : [None],
                        "سابقه بستری در بیمارستان اعصاب و روان زوجه" : [None],
                        "سابقه خشونت های خانگی زوج" : [None],
                        "سابقه خشونت های خانگی زوجه" : [None],
                        "سابقه مراجعه به پزشکی قانونی به دلیل خشونت خانگی، زوج" : [None],
                        "سابقه مراجعه به پزشکی قانونی به دلیل خشونت خانگی، زوجه" : [None],
                        "سابقه مراجعه به مراجع انتظامی به دلیل خشونت، زوج" : [None],
                        "سابقه مراجعه به مراجع انتظامی به دلیل خشونت، زوجه" : [None],
                        "نحوه رابطه جنسی زوج" : [None],
                        "نحوه رابطه جنسی زوجه" : [None],
                        "نوع رابطه جنسی زوج" : [None],
                        "نوع رابطه جنسی زوجه" : [None],
                        "اختلال در مراحل کنش جنسی زوج" : [None],
                        "اختلال در مراحل کنش جنسی زوجه" : [None],
                        "نارضایتی جنسی زوج" : [None],
                        "نارضایتی جنسی زوجه" : [None],
                        "روابط فرا زناشویی، زوج" : [None],
                        "روابط فرا زناشویی، زوجه" : [None],
                        "سابقه اقدام قضایی قبلی در خصوص طلاق زوج" : [None],
                        "تعداد اقدامات زوج" : [None],
                        "تعداد اقدامات زوجه" : [None],
                        "سابقه اقدام قضایی قبلی در خصوص طلاق زوجه" : [None],
                        "سابقه محکومیت زوج" : [None],
                        "نوع محکومیت زوج" : [None],
                        "سابقه محکومیت زوجه" : [None],
                        "نوع محکومیت زوجه" : [None],
                        "تبعات اختلافات خانوادگی برای زوج" :  [None],
                        "تبعات اختلافات خانوادگی برای زوجه" :  [None],
                        "دلایل طلاق زوج" : [None],
                        "دلایل طلاق زوجه" : [None],
                        "نیاز به بررسی وضعیت روحی زوج" : [None],
                        "نیاز به بررسی وضعیت روحی زوجه" : [None]}
            
            self.form_g_df = pd.concat([dataset, pd.DataFrame(data_dict)], ignore_index=True)
            
            self.except_list.append(id)
            print(f"{WARNING}an eception occurred in form g..{ENDC}")
            logger.exception('exception in form g')



    def update(self):

        # Loading old exception list to add new exceptions to it
        old_exception_list = np.load("Exception_ids.npy")

        # put your desired name for the file
        ids = np.load('Center7_ID_Getter.npy')
        ids = np.flip(ids)

        # Counter to save data after each 10 loops
        counter = 0

        for i in ids:

            counter += 1
            
            self.form_paziresh(i)
            self.form_arzyabi_avalie(i)
            self.form_a(i)
            self.form_b(i)
            self.form_g(i)

            self.df = pd.concat([self.df, pd.concat([self.form_paziresh_df, self.form_arzyabi_avalie_df,
                                            self.form_a_df, self.form_b_df, self.form_g_df], axis=1)], ignore_index=True)

            if counter % 10 == 0 or counter == ids.shape[0]:

                # Saving data
                self.df.to_csv("./Center7_Form_Getter.csv", index="False")
                print(f"{GREEN}The last id that it data has been collected: {counter}{ENDC} \n")
                
                # Saving exceptions
                np.save("Exception_ids.npy",
                np.concatenate((old_exception_list, np.array(self.except_list))))

            #sleep 120 secods per scraping 50 records to prevent memory leak problem
            if counter % 50 == 0:
                time.sleep(120)

        # Removing update button and showing message to user
        update_button.destroy()
        final_label = tk.Label(window, text="Successfully done", bg="white", font=("Arial", 12))
        final_label.place(relx=0.5, rely=0.5, anchor="center")



# Creating parameters for MainClass
mainurl = "https://tasmim.behzisti.net/login.aspx"

# TODO clear the hashtags and assign your website username and passwrd insteead , to login into your accout 
username = "###"
password = "###"
username_css_selector = "#tb_name"
password_css_selector = "#tb_pass"
captcha_image_css_selector = "#mycapcha_IMG"
captcha_css_selector = "#mycapcha_TB_I"


first_data = MainClass(mainurl, username, password, username_css_selector,
                       password_css_selector,captcha_image_css_selector, captcha_css_selector)

first_data.main_window()


driver = first_data.get_driver()

update1 = Update()

update1.main_window()






