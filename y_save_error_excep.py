



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# e_compare_info.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
import os
import csv
import time
import shutil
import datetime
import traceback
import subprocess
import c_navigation
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# -----------------------------------------------------------------------------------
# y_save_error_excep.py beggin
# -----------------------------------------------------------------------------------

# ---------------------------------------------------------------
# Terminal clear screen function
def clear_screen():
    #"""Clear the terminal screen."""
    if os.name == 'nt':  # Windows
        subprocess.call('cls', shell=True)
    else:  # macOS and Linux
        subprocess.call('clear', shell=True)
# ---------------------------------------------------------------
        
# ---------------------------------------------------------------
# Step 1: Run Directory Initialization Function
# Global variable to store the last created run directory
last_run_directory = None

def initialize_run_directory(base_path="results"):
    global last_run_directory
    
    # Create a unique directory for the current run
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_directory = os.path.join(base_path, f"run-{timestamp}")
    
    # Check if we've already created a directory for this timestamp
    if last_run_directory and os.path.exists(last_run_directory):
        print(f"Run directory {last_run_directory} already exists.")
        return last_run_directory
    else:
        os.makedirs(run_directory, exist_ok=True)
        print(f"Run directory {run_directory} created.")
        last_run_directory = run_directory  # Update the last created run directory
        return run_directory
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Step 2: Updated handle_exception Function
def handle_exception(e, driver, run_directory, error_subfolder="errors"):
    #"""Handle exceptions by taking a screenshot and saving the error details."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    report_path = os.path.join(run_directory, f"error_report_{timestamp}.txt")
    with open(report_path, 'w', encoding='utf-8-sig') as file:
        file.write("Exception caught:\n")
        file.write(f"{str(e)}\n\n")
        file.write("Traceback:\n")
        traceback.print_exc(file=file)  # Write the traceback to the file

    print(f"Error handled: details saved in directory {run_directory}")
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Step 3: Generalized Data File Organization Function
def create_data_directories(base_path, data_structure):
    #"""Create directories based on the specified data structure."""
    for category, structure in data_structure.items():
        category_path = os.path.join(base_path, category)
        os.makedirs(category_path, exist_ok=True)
        
        for item in structure:
            item_path = os.path.join(category_path, item)
            os.makedirs(item_path, exist_ok=True)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Step 4: Enhanced Directory Cleanup Function
def remove_directory(path, max_retries=3):
    #Attempt to remove a directory with retries.
    for attempt in range(max_retries):
        try:
            shutil.rmtree(path, ignore_errors=True)
            break
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait a bit before retrying
            else:
                print(f"Failed to remove directory {path} after {max_retries} attempts due to: {e}")
# ---------------------------------------------------------------
    
# ---------------------------------------------------------------
# Function to save the extracted data to a CSV file
def save_csv(extracted_data_escolar, headers, csv_filename):
    # Save combined data to CSV
    print("Saving extracted data to CSV file...")
    with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for row in extracted_data_escolar:
            writer.writerow(row)   
    # After saving, code shall return to previous function
    return  

# ---------------------------------------------------------------
    
# ---------------------------------------------------------------
# y_save_error_excep.py end
# ---------------------------------------------------------------


    


