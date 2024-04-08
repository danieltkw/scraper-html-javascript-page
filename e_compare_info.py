



# ---------------------------------------------------------------
# Daniel T. K. W. - github.com/danieltkw - danielkopolo95@gmail.com
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# e_compare_info.py beggin
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Imports 
import pandas as pd
import y_save_error_excep
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Function to load and compare the UFCD information
def load_and_compare_ufcd(csv_filename, listagem_csv_path, driver, run_directory):
    y_save_error_excep.clear_screen()
    print("4: On load and compare UFCD")

    try:
        listagem_df = pd.read_csv(csv_filename, delimiter=';', encoding='utf-8-sig').rename(str.strip, axis='columns')
        codigo_estados_df = pd.read_csv(listagem_csv_path, delimiter=';', encoding='utf-8-sig').rename(str.strip, axis='columns')

        listagem_df['Completed'] = 'NO'

        # Ensure the 'Código UFCD' column is treated as a string
        listagem_df['Código UFCD'] = listagem_df['Código UFCD'].astype(str)

        for index, row in listagem_df.iterrows():
            # Also ensure that 'ufcd_code' is a string
            ufcd_code = str(row['Código UFCD'])
            image_name = row['Estado']

            # Now we can safely use .str accessor methods
            if image_name == 'certificado.png':
                listagem_df.loc[listagem_df['Código UFCD'].str.strip() == ufcd_code.strip(), 'Completed'] = 'YES'
            elif image_name == 'emEstudo.png':
                listagem_df.loc[listagem_df['Código UFCD'].str.strip() == ufcd_code.strip(), 'Completed'] = 'NO'
    except Exception as e:
        y_save_error_excep.handle_exception(e, driver, run_directory)

    return listagem_df
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# e_compare_info.py end
# ---------------------------------------------------------------

    
    
    