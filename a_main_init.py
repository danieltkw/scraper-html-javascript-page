



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
import os
import sys
import time
import shutil
import pandas as pd
import datetime
import w_window
import traceback
import subprocess
import b_entry_login
import c_navigation
import d_insert_data
#import e_compare_info
#import f_extract_data
#import g_order_data
import y_save_error_excep 
from bs4 import BeautifulSoup
from collections import OrderedDict
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# ---------------------------------------------------------------


# ---------------------------------------------------------------
# a_main_init.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Configure driver function
def configure_driver():
    # Specify the correct path to chromedriver.exe
    # path_to_chromedriver = r"F://GDrive//My Drive//code//test----------//map01//chrome_driver//chromedriver-win64//chromedriver.exe"  # Update this path
    # path_to_chromedriver = r"G://My Drive//code//test----------//map01//chrome_driver//chromedriver-win64//chromedriver-win64//chromedriver.exe"  # Update this path
    # # "G://My Drive//code//test----------//map01//chromedriver.exe"
    # G:\My Drive\code\test----------\map01\chrome_driver\chromedriver
    #path_to_chromedriver = r"G://My Drive//code//test----------//map01//chromedriver.exe"  # Update this path 
    
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the ChromeDriver
    path_to_chromedriver = os.path.join(dir_path, 'chromedriver.exe')
    
    service = Service(executable_path=path_to_chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver   
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Chosen NIF
# 222490497
# 271970278
# 307277003
# ---------------------------------------------------------------

# ---------------------------------------------------------------
class Frontend:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Process Status")
        self.root.geometry("1200x700")  # Set the window size

        self.status_label = tk.Label(self.root, text="Ready...", font=('Helvetica', 16), pady=20)
        self.status_label.pack()

        # Hide the main window for now
        self.root.withdraw()

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()  # Update the status label

    def get_user_input(self, prompt):
        self.root.deiconify()  # Show the main window for user input
        user_input = simpledialog.askstring("Input Required", prompt, parent=self.root)
        self.root.withdraw()  # Hide the main window again
        return user_input

    def run(self):
        self.root.deiconify()  # Show the main window when running the frontend
        self.root.mainloop()
# ---------------------------------------------------------------

# entrada de nif por meio de um arquivo csv 
# entrada de users


# ---------------------------------------------------------------
# Initialize the system
def initialize_system(frontend):
    # Clear the screen and print a message to indicate the start of the program
    y_save_error_excep.clear_screen()
    frontend.update_status("0:Init main")

    # Create directories and start the program
    run_directory = y_save_error_excep.initialize_run_directory()
    frontend.update_status(f"Directory created: {run_directory}")
    
    # Defeut wt timing
    wt = 1

    # Initialize the web driver
    driver = configure_driver()
    frontend.update_status("Driver started")

    # Ask user if the website keeps the same login page 'sigo.pt', if not, ask user to input the correct URL
    # If the website is the same, the user can press Enter to continue


    frontend.update_status("Site padrão: sigo.pt/login.jsp - Pressione Enter para continuar ou insira o URL correto:")
    # If the user provides a URL, navigate to that URL, if not, use the default URL
    web_choice = frontend.get_user_input("Insira URL ou aperte Enter para prosseguir:")
    
    # If user doesn't enter anything, use default values
    if not web_choice:
        web_choice =frontend.update_status("URL: https://www.sigo.pt/Login.jsp")
        web_choice = 'https://www.sigo.pt/Login.jsp'


    driver.get(web_choice)

    frontend.update_status("Insira o seu número de utilizador e a sua palavra-passe: ")

    # Initialize variables to None
    username = None
    passw = None
    valid_nifs = []
    invalid_nifs = []   

    # Loop until both username and password are provided
    while not username or not passw:
        if username is None:
            username = frontend.get_user_input("Por favor insira o seu número de utilizador: ")
        if passw is None:
            passw = frontend.get_user_input("Por favor insira a sua palavra-passe: ")

        # Check if either the username or password is still not provided
        if not username or not passw:
            frontend.update_status("Por favor insira um número de utilizador e uma palavra-passe válidos.")
            # Reset the variables if the input is invalid
            username = None
            passw = None

        # If user doesn't enter anything, use default values
        if not username or not passw:
            frontend.update_status("Utilizador e palavra-passe predefinidos")
            username = '13986'
            passw = 'ativoe'
        
        frontend.update_status("Insira um NIF ou escolha uma opção:")
        # Prompt the user to enter a NIF or use a default value from a .csv file
        nif_choice = frontend.get_user_input("Insira um NIF ou press Enter para usar um valor predefinido:")
        # NIF must be numeric and 9 digits, code check if it is 
        if not nif_choice:
            # Code will search for a .csv file with default NIF values, if not found, it will use a default value
            frontend.update_status("NIF predefinido (planilha ou escolha manual)")
            valid_nifs = y_save_error_excep.open_nif_csv()
            # nif = '271970278'
            # Chose the first number of nif from the valid_nifs list, and convert it to string
            #nif = str(valid_nifs['NIF'].iloc[0])
            nif = valid_nifs
            
        else:
            if nif_choice.isdigit() and len(nif_choice) == 9:
                nif = nif_choice
            else:
                frontend.update_status("Invalid NIF. Please enter a numeric value with 9 digits.")
                nif = None
             


    # Start the login process and other backend tasks
    try:
        b_entry_login.login(driver, username, passw, nif, wt, run_directory)
        frontend.update_status("Logged in successfully")

    except TimeoutException as e:
        frontend.update_status("TimeoutException occurred")
        y_save_error_excep.handle_exception(e, driver, run_directory)
    except Exception as e:
        frontend.update_status("An unexpected error occurred")
        y_save_error_excep.handle_exception(e, driver, run_directory)
    finally:
        driver.quit()
        frontend.update_status("Process completed. Driver session ended.")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Check user credentials
def check_credentials():
    # 11234261
    print("Esta autorizado por PEDRO MIGUEL CAMARA LOPES?")
    bi_cc = input("Se sim, digite o BI/CC: ")
    if bi_cc != '11234261':
        print("Acesso não autorizado. BI/CC incorreto.")
        sys.exit(1)
    
    # 222490497
    nif = input("Digite o NIF: ")
    if nif != '222490497':
        print("Acesso não autorizado. NIF incorreto.")
        sys.exit(1)

    # 516106228
    nipc = input("Digite o NIPC: ")
    if nipc != '516106228':
        print("Acesso não autorizado. NIPC incorreto.")
        sys.exit(1)

    print("Acesso autorizado.")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    
    check_credentials()  # Check user credentials

    # Initialize the frontend and start the program
    frontend = Frontend()
    initialize_system(frontend)
    frontend.run()
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# a_main_init.py end
# -----------------------------------------------------------------------------------






