




# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# b_entry_login.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import y_save_error_excep 
import time
import os
import subprocess
import c_navigation
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Login function
def login(driver, username, password, nif, wt, run_directory):

    # Clear screen terminal 
    #y_save_error_excep.clear_screen  
    print(" :On login")    
        
    try:

        # After clicking, wait for the transition and for the NIF input to appear
        time.sleep(wt)  # Sleep for a duration that ensures the next page or form is loaded
        
        # Website
        #driver.get('https://www.sigo.pt/Login.jsp')

        # Wait for the initial animation or load
        #time.sleep(wt)  # Sleep for 2 seconds to wait for the cursor to be in the login field

        # Assuming the cursor is in the username field on page load,
        # we send the username, a Tab key to switch to the password field, and then the password
        actions = webdriver.ActionChains(driver)
        actions.send_keys(username)
        actions.send_keys(Keys.TAB)
        actions.send_keys(password)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        
        # Go to extract info
        print("1-2:Going to navigation")
        c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
        
    except TimeoutException as e:
        print("TimeoutException: An element could not be found or interacted with.")
        y_save_error_excep.handle_exception(e, driver, run_directory)
    except Exception as e:
        print("An unexpected error occurred.")
        y_save_error_excep.handle_exception(e, driver, run_directory)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# b_entry_login.py end
# ---------------------------------------------------------------











