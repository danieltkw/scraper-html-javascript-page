

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


def extract():
    # Placeholder function for extracting data.
    pass


def read_pdf(file_path):
    # Open and read a PDF file
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            print(page.extract_text())  # For testing, prints text to console
            

def find_pdfs_and_download(driver, base_directory):
    # Example function to find PDF links on the current page and download them
    # This is a placeholder: you'd need to identify how PDFs are linked on your site
    pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
    for link in pdf_links:
        pdf_url = link.get_attribute('href')
        # Logic to download PDF from pdf_url goes here
        # Logic to create directory and save PDF goes here


def download_pdf(driver):
    #"""Find and download the PDF."""
    # Find the PDF link and download it. This is a placeholder and should be replaced with actual logic.
    wait = WebDriverWait(driver, 10)
    pdf_link = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Exportar")))
    pdf_link.click()



def extract_and_save_data(driver, nif=None, name=None, sigo_number=None):
    
    clear_screen()
    
    print("3: On data extraction")
    wait = WebDriverWait(driver, 30)
    data_list = []

    try:
        # Adjusting the XPath to match the element
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='ui-column-title' and contains(text(), 'Componente de formação Profissional/Tecnológica')]")))
        
        # Wait for the table with 'Componente de formação Profissional/Tecnológica' to be visible
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.ui-column-title:contains('Componente de formação Profissional/Tecnológica')")))

        # Find the rows within the data table
        rows = driver.find_elements(By.CSS_SELECTOR, "#color-trs\\:j_idt99\\:j_idt125\\:j_idt126_data tr")
        for row in rows:
            # Extract the 'Código' from the row
            codigo = row.find_element(By.CSS_SELECTOR, "td.xsmall-column").text
            # Extract the 'Estado' based on the image src attribute
            estado_img_src = row.find_element(By.CSS_SELECTOR, "td.exsmall-column img").get_attribute("src")
            estado = "Certificado" if "certificado.png" in estado_img_src else "Em Estudo"

            # Create a dictionary with the extracted data
            data_row = {'Código': codigo, 'Estado': estado}
            if nif:
                data_row['NIF'] = nif
            if name:
                data_row['Name'] = name
            if sigo_number:
                data_row['SIGO Number'] = sigo_number
            
            data_list.append(data_row)

        # Handle pagination if there's a next button
        while True:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".ui-paginator-next.ui-state-default.ui-corner-all")
                if next_button.is_enabled():
                    next_button.click()
                    # Wait for the table to refresh
                    wait.until(EC.staleness_of(rows[0]))
                    rows = driver.find_elements(By.CSS_SELECTOR, "#color-trs\\:j_idt99\\:j_idt125\\:j_idt126_data tr")
                    # Continue extracting data as before
                    # ...
                else:
                    break
            except NoSuchElementException:
                break

        # Write the data to a CSV file
        with open('codigos_estados.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Código', 'Estado', 'NIF', 'Name', 'SIGO Number']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data_row in data_list:
                writer.writerow(data_row)
        
        print(f"Data extracted and saved to 'codigos_estados.csv'. Total {len(data_list)} records found.")

    except Exception as e:
        print(f"An exception occurred: {e}")
        driver.save_screenshot('selenium_exception.png')
        raise e


# -----------------------------------------------------------------------------------
# f_extract_data
# -----------------------------------------------------------------------------------

    
    