

# Daniel T. K. W.
# github.com/danieltkw
# danielkopolo95@gmail.com
# ---- Importando bibliotecas necessárias ----


# -----------------------------------------------------------------------------------
# Scrappy code
# -----------------------------------------------------------------------------------

# ---- Imports ----


# -----------------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------------


def order():
    # Placeholder function for ordering data.
    
    # Load the HTML content into BeautifulSoup
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Assuming we have the right div or table class or id
    # This will change based on the actual HTML structure, which isn't fully shown in the snippets
    courses_table = soup.find('div', {'id': 'relevant_div_or_table_id'})

    # Store the extracted data
    extracted_data = []

    # Iterate over each row of the table within the tbody section
    for row in courses_table.find_all('tr'):
        # Find the columns (these classes will depend on the actual HTML structure)
        code_col = row.find('td', {'class': 'class_for_code_column'})
        status_col = row.find('td', {'class': 'class_for_status_column'})

        # Extract the text or alt text for images
        code = code_col.text.strip() if code_col else None
        status_image = status_col.find('img')
        status = status_image['alt'].strip() if status_image else None

        # Store the extracted data
        if code and status:
            extracted_data.append({'code': code, 'status': status})

    # Now `extracted_data` contains all the codes and statuses
    # You can process this list as needed, e.g., save to a file, database, etc.
    
    # For demonstration, let's just print the extracted data
    for data in extracted_data:
        print(data)
    pass



# -----------------------------------------------------------------------------------
# g_order_data
# -----------------------------------------------------------------------------------

    
    
    