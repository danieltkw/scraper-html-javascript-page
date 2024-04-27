



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
import y_save_error_excep 
import time
import os
import subprocess
import d_insert_data 
from d_insert_data import extract_and_save_data
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
# ---------------------------------------------------------------

global_nif_counter = 0

# ---------------------------------------------------------------
# Function to enter the NIF and navigate to the 'Formandos e Inscrições' page
def navigate_to_formandos_e_inscricoes(driver, nifs, wt, run_directory):

    y_save_error_excep.clear_screen()
    print("2: On navigation")

    global global_nif_counter
    main_tab_handle = driver.current_window_handle

    while global_nif_counter < len(nifs):
        current_nif = nifs[global_nif_counter]
        print(f"Processing NIF: {current_nif}")
        print(f"Current NIF counter: {global_nif_counter}/{len(nifs)}")

        try:

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Formandos e'))).click()
            nif_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "form1:tfNif")))
            nif_input.clear()
            nif_input.send_keys(current_nif)
            nif_input.send_keys(Keys.RETURN)

            # Wait briefly and check for the presence of 'Inscrições'
            time.sleep(wt)  # Small delay to allow any potential messages to load
            inscricoes_links = driver.find_elements(By.LINK_TEXT, 'Inscrições')
            if inscricoes_links:
                # If 'Inscrições' is found, click it
                inscricoes_links[0].click()
                
                # try to find the name in page to capture it too 
                nif_name = find_name(driver)
                
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Passaporte Qualifica'))).click()
                driver.switch_to.window(driver.window_handles[-1])
                global_nif_counter += 1
                d_insert_data.extract_and_save_data(driver, WebDriverWait(driver, 10), run_directory, wt, main_tab_handle, nifs, current_nif, name=nif_name)
            else:
                # No 'Inscrições' link found, implying no records
                print(f"No records found for NIF {current_nif}. Skipping to the next NIF.")
                global_nif_counter += 1
                if global_nif_counter < len(nifs):
                    # Reset by clicking 'Formandos e' to prepare for the next NIF entry
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Formandos e'))).click()
                    time.sleep(1)  # Allow the page to reset properly


        except Exception as e:
            print(f"Error processing NIF {current_nif}: {str(e)}")
            y_save_error_excep.handle_exception(e, driver, run_directory)


        if global_nif_counter >= len(nifs):
            print("All NIFs have been processed.")
            break

# ---------------------------------------------------------------

def find_name(driver):
    try:
        # Capture the name of the element with ID 'form1:staticText12'
        name_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form1:staticText12")))
        name_text = name_element.text
        print(f"Name found: {name_text}")
        return name_text
    except TimeoutException:
        print("Name element not found within the time limit.")
        return None

# ---------------------------------------------------------------
# c_navigation end  
# ---------------------------------------------------------------

    
    