



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# d_insert_data.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
import os
import csv
import time
import datetime
import traceback
import subprocess
import e_compare_info
import y_save_error_excep 
import c_navigation
from fuzzywuzzy import process
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
# ---------------------------------------------------------------



# ---------------------------------------------------------------
# Helper function to get the maximum page number
def get_max_page_number(driver, wait):

    try:
        # Specific container selector for the paginator
        paginator_container_selector = "div#color-trs\\:j_idt99\\:j_idt125\\:j_idt126_paginator_bottom.ui-paginator.ui-paginator-bottom.ui-widget-header.ui-corner-bottom"

        # Wait for the specific container to be present
        paginator_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, paginator_container_selector)))

        # Within this container, find elements representing pages
        page_xpaths = paginator_container.find_elements(By.CSS_SELECTOR, ".ui-paginator-page.ui-state-default.ui-corner-all")
        max_page_number = len(page_xpaths) if page_xpaths else 1  # Ensure there's at least one page

    except TimeoutException:
        # Handle the case where the paginator is not found within the timeout
        max_page_number = 1  # Assume there is only one page if no paginator is found

    return max_page_number    
# ---------------------------------------------------------------   
   
# --------------------------------------------------------------- 
# Helper function to extract data from a table element
def extract_data_from_table(table_element):
    extracted_data = []
    # Get the HTML content of the table element
    table_html = table_element.get_attribute('outerHTML')
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(table_html, 'html.parser')
    # Iterate over all rows in the table, skipping the header row
    rows = soup.find_all('tr')[1:]
    for row in rows:
        cells = row.find_all('td')
        if cells:
            first_cell_text = cells[0].get_text(strip=True)
            # Check the first cell for a continuous string with a max length of 20 characters
            if ('_' in first_cell_text or first_cell_text.isnumeric()) and len(first_cell_text) <= 20:
                row_data = []
                for i, cell in enumerate(cells):
                    if i == len(cells) - 2:  # If this is the 'Estado' image cell
                        image_element = cell.find('img')
                        estado_image_name = extract_image_filename(image_element)
                        row_data.append(estado_image_name)
                    else:
                        row_data.append(cell.get_text(strip=True))
                extracted_data.append(row_data)
    return extracted_data
# --------------------------------------------------------------- 

# ---------------------------------------------------------------
# Helper function to extract the image filename from the Estado column
def extract_image_filename(image_element):
    if image_element and 'src' in image_element.attrs:
        image_url = image_element['src']
        image_name = os.path.basename(urlparse(image_url).path)
        return image_name
    return "No image"
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Function to extract and save data to a CSV file
def extract_data_from_page(soup, table_id):
    extracted_data = []
    table = soup.find('div', id=table_id)
    if table:
        rows = table.find_all('tr', role="row")[1:]  # Skip the header row
        for row in rows:
            cells = row.find_all('td', role="gridcell")
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells[:-1]]  # Exclude the image cell
                # Handle the image cell separately
                image_element = cells[-1].find('img')
                estado_image_name = extract_image_filename(image_element)
                row_data.append(estado_image_name)
                extracted_data.append(row_data)
            else:
                extracted_data.append(["No data found in row"])
    return extracted_data
# ---------------------------------------------------------------

# final_nif_results = [] is a global list for store all nif results
global_final_nif_results = []
name_nif_list = [] 

# ---------------------------------------------------------------    
# Function to extract and save data to CSV files
def extract_and_save_data(driver, wait, run_directory, wt, main_tab_handle, nif=None, next_nif = None, name=None, sigo_number=None):
    

    y_save_error_excep.clear_screen()
    print("3: On data extraction")

    # Show current NIF

    print(f"Processing NIF: {nif}")
    print(f"Processing NIF: {next_nif}")


    wait = WebDriverWait(driver, 10)
    error_occurred = False

    headers = ['Codigo', 'Unidade', 'Duracao', 'Data de Certificacao', 'Estado', 'Pontos de Credito']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = os.path.join(run_directory, f"{next_nif}_cdg_{timestamp}.csv")

    max_page_number = get_max_page_number(driver, wait)
    print(f"Total pages: {max_page_number}")
    # sleep for 10s for testing
    #time.sleep(10)

    # 233517910 catia 

    extracted_data_escolar = []
    name_nif = [name, next_nif] 

    # init global variable final_nif_results = [] to store a list with everything 
    global global_final_nif_results 
    global name_nif_list

    global_final_nif_results.append(extracted_data_escolar)
    name_nif_list.append(name_nif)  # Store it in the global li

    if max_page_number == 1:
        escolar_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Componente de formação Escolar/Base') or contains(., 'Componente de formação Profissional/Tecnológica')]/ancestor::div[contains(@id, 'j_idt')]")))
        new_data = extract_data_from_table(escolar_table)
        extracted_data_escolar.extend(new_data)
        y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename, next_nif, name)
        # name_nif stores the moment nif and name, and store in the list of name_nif for pass to the final csv
        name_nif = [next_nif, name]
        name_nif.append(name_nif) 
        y_save_error_excep.save_final_csv(global_final_nif_results, run_directory, name_nif_list)

        c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)    

    if max_page_number > 1:
        try:
            for i in range(2, max_page_number + 1):
                paginator_container_selector = "div#color-trs\\:j_idt99\\:j_idt125\\:j_idt126_paginator_bottom.ui-paginator.ui-paginator-bottom.ui-widget-header.ui-corner-bottom"
                paginator_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, paginator_container_selector)))
        
                escolar_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Componente de formação Escolar/Base') or contains(., 'Componente de formação Profissional/Tecnológica')]/ancestor::div[contains(@id, 'j_idt')]")))
                new_data = extract_data_from_table(escolar_table)
                extracted_data_escolar.extend(new_data)

                try:
                    if i <= max_page_number:
                        page_number_element = paginator_container.find_element(By.XPATH, f".//span[@class='ui-paginator-page ui-state-default ui-corner-all'][text()='{i}']")
                        driver.execute_script("arguments[0].click();", page_number_element)
                        
                        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, paginator_container_selector + " .ui-paginator-page.ui-state-active"), str(i)))

                        escolar_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Componente de formação Escolar/Base') or contains(., 'Componente de formação Profissional/Tecnológica')]/ancestor::div[contains(@id, 'j_idt')]")))
                        new_data = extract_data_from_table(escolar_table)
                        extracted_data_escolar.extend(new_data)

                        # name_nif stores the moment nif and name, and store in the list of name_nif for pass to the final csv
                        new_data = extract_data_from_table(escolar_table)
                        extracted_data_escolar.extend(new_data)
                        
                        # sleep to wait page load 
                        time.sleep(1)   
                        
                    else:
                        print(f"Reached the last page: {i-1}. No further pages to navigate.")
                        break
                except Exception as e:
                    print(f"Could not navigate to page {i} or extract data. Error: {e}")

            #y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename, next_nif, name)
        
        except Exception as e:
            error_occurred = True
            print(f"An unexpected error occurred during pagination or data extraction. Error: {e}")
            y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename, next_nif, name)
            y_save_error_excep.handle_exception(e, driver, run_directory)

            # nif is a data frame with NIFs
            # Check if the next_nif has already been processed, comparing with the last nif on the list, if not, go switch tab to navigate_to_formandos_e_inscricoes

            if next_nif != nif[-1]:
                driver.switch_to.window(driver.window_handles[-1])
                c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
            else:
                print("E: All NIFs have been processed.")
                y_save_error_excep.save_final_csv(global_final_nif_results, run_directory, name_nif_list)
                
                

            c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)

        except TimeoutError or TimeoutException as e:
            error_occurred = True
            print(f"An Time out error occurred during pagination or data extraction. Error: {e}")
            y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename, next_nif, name)
            y_save_error_excep.handle_exception(e, driver, run_directory)

            if next_nif != nif[-1]:
                driver.switch_to.window(driver.window_handles[-1])
                c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
            else:
                print("Te: All NIFs have been processed.")
                

            c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
            
        finally:
            y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename, next_nif, name)

    if error_occurred:
        print(f"Data partially extracted and saved to '{csv_filename}' due to an error. Please check the error log.")
        y_save_error_excep.save_final_csv(global_final_nif_results, run_directory, name_nif_list)
    else:
        print(f"Data extracted and saved to '{csv_filename}' - going back if there is more NIF to process.")
    

        # Check if the next_nif has already been processed, comparing with the last nif on the list, if not, go switch tab to navigate_to_formandos_e_inscricoes 
        if next_nif != nif[-1]:
            # Switch back to the main tab
            driver.switch_to.window(main_tab_handle)
            c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
        else:
            print("3: All NIFs have been processed.")
            y_save_error_excep.save_final_csv(global_final_nif_results, run_directory, name_nif_list)      
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# d_insert_data.py end
# ---------------------------------------------------------------




    