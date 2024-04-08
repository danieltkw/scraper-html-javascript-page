



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# c_navigation beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import y_save_error_excep 
import time
import os
import subprocess
import d_insert_data 
from d_insert_data import extract_and_save_data
# ---------------------------------------------------------------

global_checker = None

# ---------------------------------------------------------------
# Function to enter the NIF and navigate to the 'Formandos e Inscrições' page
def navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory):
    
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary

    print("2:On navigation")
    global global_checker
    
    if (global_checker != 1):   
        y_save_error_excep.clear_screen()    
        try:
            
            # Use partial link text to find and click the 'Formandos e Inscrições' link
            formandos_e_inscricoes_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Formandos e')))
            formandos_e_inscricoes_link.click()
            
            # After clicking, wait for the transition and for the NIF input to appear
            time.sleep(wt)  # Sleep for a duration that ensures the next page or form is loaded
            
            # Now find the NIF input field by its ID and enter the NIF number
            nif_field = wait.until(EC.element_to_be_clickable((By.ID, "form1:tfNif")))
            nif_field.clear()
            nif_field.send_keys(nif)
            
            # After clicking, wait for the transition and for the NIF input to appear
            time.sleep(wt)  # Sleep for a duration that ensures the next page or form is loaded
            
            # After entering the NIF, simulate pressing Enter to search
            nif_field.send_keys(Keys.RETURN)

            # Wait for the 'Inscrições' link to appear in the results
            inscricoes_links = wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, 'Inscrições')))
            
            # After clicking, wait for the transition and for the NIF input to appear
            time.sleep(wt)  # Sleep for a duration that ensures the next page or form is loaded
            

            # We want to click the first 'Inscrições' link only
            if inscricoes_links:
                inscricoes_links[0].click()

                # Wait for the 'Passaporte Qualifica' button/link to appear
                passaporte_qualifica_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Passaporte Qualifica')))
                passaporte_qualifica_button.click()

                # Assuming a new tab/window is opened, you might need to switch to it
                driver.switch_to.window(driver.window_handles[-1])

                # Wait for the 'Competências' link to appear    

        except TimeoutException as e:
            print("TimeoutException: An element could not be found or interacted with.")
            y_save_error_excep.handle_exception(e, driver, run_directory)
        except Exception as e:
            print("An unexpected error occurred.")
            y_save_error_excep.handle_exception(e, driver, run_directory)

            
        finally:
            print("2-3:Going to extract data")
            global_checker = 1
            d_insert_data.extract_and_save_data(driver, wait, run_directory, wt, nif)
    
    else: 
        print("2:Already navigated, press enter to continue")
        # Wait for the user to press Enter before continuing
        input("Press Enter to continue...")      
        d_insert_data.extract_and_save_data(driver, wait, run_directory, wt, nif)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# c_navigation end  
# ---------------------------------------------------------------

    
    