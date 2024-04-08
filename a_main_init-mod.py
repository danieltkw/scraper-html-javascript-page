



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# b_entry_login.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
import os
import time
import subprocess
import b_entry_login
#import c_navigation
#import d_insert_data
#import e_compare_info
#import f_extract_data
#import g_order_data
import y_save_error_excep 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains



# -----------------------------------------------------------------------------------
# a_main_init.py beggin
# -----------------------------------------------------------------------------------

# ---------------------------------------------------------------
# Configure driver function
def configure_driver():
    # Specify the correct path to chromedriver.exe
    path_to_chromedriver = r"C://Users//Administrator//Desktop//test//map01//chrome_driver//chromedriver-win64//chromedriver.exe"  # Update this path
    service = Service(executable_path=path_to_chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver   
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Main function to initialize the system
def initialize_system():
    
    # Clear the screen and print a message to indicate the start of the program
    y_save_error_excep.clear_screen()
    print("0:Init main")
    
    # Create the directories 
    run_directory = y_save_error_excep.initialize_run_directory()
    print("Directory created: ", run_directory)    
    
    # Wait time
    wt = 2
    # Main user for start the program
    username = ''
    passw = ''
    # Chosen NIF

    nif = ''    
    print("Basic user: ", username, " ", passw, " ", nif)    
    
    # Start up the driver
    driver = configure_driver()
    print("Driver started")

    try:
        # Call your login function and pass the driver      
        print("Goin to 1-login")
        b_entry_login.login(driver, username, passw, nif, wt, run_directory)
        
        # c_navigation.navigate(driver, wait)
        # d_insert_data.insert(driver, wait)
        # e_access_links.access(driver, wait)
        # f_extract_data.extract(driver, wait)
        # g_order_data.order(driver, wait)

    except TimeoutException as e:
        print("TimeoutException: An element could not be found or interacted with.")
        y_save_error_excep.handle_exception(e, driver, run_directory)
    except Exception as e:
        print("An unexpected error occurred.")
        y_save_error_excep.handle_exception(e, driver, run_directory)
    finally:
        # Close the driver at the end of the session, or handle as needed
        driver.quit()
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    initialize_system()
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# a_main_init.py end
# -----------------------------------------------------------------------------------






