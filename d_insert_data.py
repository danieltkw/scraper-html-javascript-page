



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
    
    # Wait for the paginator to be present
    paginator = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ui-paginator-pages")))
    # Use a more specific selector if possible to only find elements representing pages
    page_xpaths = paginator.find_elements(By.CSS_SELECTOR, ".ui-paginator-page.ui-state-default.ui-corner-all")
    # The total number of pages is directly the count of these elements
    max_page_number = len(page_xpaths)
    print(page_xpaths)

    return max_page_number, page_xpaths     
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

# ---------------------------------------------------------------
def navigate_and_collect_data(driver, wait, run_directory, table_id):
    extracted_data = []
    page_number = 1  # Start with the first page
    while True:
        try:
            # Check if pagination is available and if there's a next page
            next_page_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next page"]')
            if not next_page_btn.is_enabled():
                break  # No more pages

            # Extract data from the current page using the given table_id
            courses_table_html = wait.until(
                EC.presence_of_element_located((By.ID, table_id))
            ).get_attribute('outerHTML')
            soup = BeautifulSoup(courses_table_html, 'html.parser')
            extracted_data.extend(extract_data_from_page(soup, table_id))

            # Navigate to the next page
            next_page_btn.click()
            page_number += 1
            wait.until(EC.staleness_of(courses_table_html))  # Wait for the old table to go stale
            
        except NoSuchElementException:
            # If there's no next page button, break from the loop
            break
        except TimeoutException as e:
            # Handle cases where the page did not load in time
            y_save_error_excep.handle_exception(e, driver, run_directory)  
            break
        
    return extracted_data
# ---------------------------------------------------------------

# ---------------------------------------------------------------    
# Function to extract and save data to CSV files
def extract_and_save_data(driver, wait, run_directory, wt, nif=None, name=None, sigo_number=None):
    
    # Beggin the code
    y_save_error_excep.clear_screen()
    print("3: On data extraction")
    
    # Initialize the extracted data list outside the loop
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary
    error_occurred = False  # Initialize a flag to check if an error occurred
    
    # Define headers based on the expected columns and file path
    headers = ['Código', 'Unidade', 'Duração', 'Data de Certificação', 'Estado', 'Pontos de Crédito']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = os.path.join(run_directory, f"cdg_{timestamp}.csv")
    
    # Check if there is more than one page
    max_page_number, page_xpaths = get_max_page_number(driver, wait)
    print(f"Total pages: {max_page_number}")

    # Initialize the extracted data list outside the loop
    extracted_data_escolar = []

    # Find tables dynamically based on the known titles
    escolar_table = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Componente de formação Escolar/Base') or contains(., 'Componente de formação Profissional/Tecnológica')]/ancestor::div[contains(@id, 'j_idt')]")))
    
    # Extract data from tables
    extracted_data_escolar = extract_data_from_table(escolar_table) if escolar_table else []


    try:
        for i in range(1, max_page_number + 1):
            try:
                # Wait for the paginator container to be present
                paginator = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ui-paginator-pages"))
                )
                
                # Find the page link by text, which should work regardless of the hover state
                page_element_xpath = f"//span[contains(@class, 'ui-paginator-page')][not(contains(@class, 'ui-state-hover'))][text()='{i}']"
                page_elements = paginator.find_elements(By.XPATH, page_element_xpath)
                
                # There should be only one element matching the page number without the hover state
                if len(page_elements) == 1:
                    page_element_to_click = page_elements[0]
                    driver.execute_script("arguments[0].click();", page_element_to_click)
                    
                    # Wait for the active page number to reflect the clicked page
                    WebDriverWait(driver, 10).until(
                        EC.text_to_be_present_in_element(
                            (By.XPATH, f"//span[@class='ui-paginator-page ui-state-active'][text()='{i}']"),
                            str(i)
                        )
                    )
                    
                    # Re-find the escolar_table for the new page content
                    escolar_table = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "your_table_css_selector"))
                    )
                    
                    # Extract and append new data from the table
                    new_data = extract_data_from_table(escolar_table)
                    extracted_data_escolar.extend(new_data)
                else:
                    raise Exception(f"Expected one element for page {i} but found {len(page_elements)}")

           
    except TimeoutException as e:
        print(f"TimeoutException: An element could not be found or interacted with. Error: {e}")
        y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename)
        y_save_error_excep.handle_exception(e, driver, run_directory)
        c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
    except Exception as e:
        error_occurred = True  # Set the flag if an error occurs
        print(f"An unexpected error occurred. Error: {e}")
        y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename)
        y_save_error_excep.handle_exception(e, driver, run_directory)
        c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)

    finally: 
        # Save combined data to CSV
        y_save_error_excep.save_csv(extracted_data_escolar, headers, csv_filename)
    c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)

    if error_occurred:
        print(f"Data partially extracted and saved to '{csv_filename}' due to an error. Total {len(extracted_data_escolar)} records found.")
    else:
        print(f"Data extracted and saved to '{csv_filename}'. Total {len(extracted_data_escolar)} records found.")# ---------------------------------------------------------------
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# d_insert_data.py end
# ---------------------------------------------------------------




    