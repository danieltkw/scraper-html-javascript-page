



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# e_compare_info.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
import os
import datetime
import glob
import pandas as pd
import y_save_error_excep
import c_navigation
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Function to find the most recent CSV file in the latest subfolder within 'results'
def find_latest_csv():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of the script
    results_dir = os.path.join(current_dir, 'results')  # Path to the 'results' directory

    # Check if 'results' directory exists
    if not os.path.exists(results_dir):
        print("The 'results' directory does not exist.")
        return None

    # Get all subdirectories in 'results'
    subdirs = [os.path.join(results_dir, d) for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d))]
    
    # Find the latest subdirectory based on modification time
    latest_subdir = max(subdirs, key=os.path.getmtime)

    # Get all CSV files in the latest subdirectory
    csv_files = glob.glob(os.path.join(latest_subdir, '*.csv'))

    # Find the latest CSV file based on modification time
    if not csv_files:
        print("No CSV files found in the latest results subdirectory.")
        return None
    
    latest_csv = max(csv_files, key=os.path.getmtime)

    # Attempt to open the latest CSV file
    try:
        with open(latest_csv, 'r') as file:
            print(f"Opening the latest CSV file: {latest_csv}")
            # Process the file here
            # ...
            return latest_csv
    except IOError as e:
        print(f"Could not open file: {latest_csv}")
        return None
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Function to load and compare the UFCD information
def load_and_compare_ufcd(csv_filename = None, driver = None, run_directory = None, nif = None, wt = None):
    y_save_error_excep.clear_screen()
    print("4: On load and compare UFCD")

    # Define the user choice
    option = 1

    # Call the function
    latest_csv_path = find_latest_csv()
    if csv_filename == None and latest_csv_path:
        print(f"Found and ready to process: {latest_csv_path}")


    while option == 1:

        # Prompt the user to enter a UFCD code
        ufcd_code_to_check = input("Please enter the UFCD code to check: ").strip()

        try:
            # Load the CSV files into DataFrames
            listagem_df = pd.read_csv(csv_filename, delimiter=';', encoding='utf-8-sig').rename(str.strip, axis='columns')

            listagem_df['Codigo'] = listagem_df['Codigo'].astype(str)

            # Check if the user's UFCD code is in listagem_df
            if ufcd_code_to_check in listagem_df['Codigo'].values:
                image_name = listagem_df.loc[listagem_df['Codigo'] == ufcd_code_to_check, 'Estado'].iloc[0]
                if image_name == 'certificado.png':
                    print(f'Utente já realizou {ufcd_code_to_check}')
                elif image_name == 'emEstudo.png':
                    print(f'Utente está a realizar {ufcd_code_to_check}')
                #elif listagem_df['Estado'] is None and listagem_df['Codigo'] is not None:
                #    print(f'Utente cursou todo cuso {ufcd_code_to_check}')
                else:
                    print(f'Estado desconhecido para o código {ufcd_code_to_check}')
            else:
                print(f'Utente nunca cursou esse UFCD ({ufcd_code_to_check})')

            print("1: Check another UFCD")
            print("2: Exit")
            input_option = input("Please select an option: ")
            option = int(input_option)
            if option == 1:
                continue
            elif option == 2:
                break
            elif option != 1 and option != 2:
                print("Invalid option. Please try again.")
                continue
            

        except Exception as e:
            y_save_error_excep.handle_exception(e, driver, run_directory)
        finally:
            # Navigate back or to the next step as necessary
            if csv_filename != None and option == 2:
                c_navigation.navigate_to_formandos_e_inscricoes(driver, nif, wt, run_directory)
# ---------------------------------------------------------------

# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    load_and_compare_ufcd()
# -----------------------------------------------------------------------------------

# ---------------------------------------------------------------
# e_compare_info.py end
# ---------------------------------------------------------------

    
    
    