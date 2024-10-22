"""
this class is for web scraping the official ISR web page, to extract the data
from the weekly and monthly ISR table, process the data and make use of it...
"""
# TODO: chance all the prints...
import requests
import os
import csv
from bs4 import BeautifulSoup
from pathlib import Path
from taxes_calculation.utils_taxes.csvFileName import csvFileName

class IsrScraping:
    _instance = None # class variable to storage the only instance...

    def __new__(cls, *args, **kwargs):
        if not cls._instance: # if there is any instance, create one...
            cls._instance = super(IsrScraping, cls).__new__(cls)
        # returns the same instance always...
        return cls._instance

    def __init__(self):
        #check if it has already been initialized...
        if not hasattr(self, 'initialized'):
            self.url = "https://www.elcontribuyente.mx/2023/12/tablas-isr-2024/"
            self.base_dir = Path.home() / "desktop" / "did_finace_manager" / "csv"
            self.h3 = ["reteperiodicas2", "reteperiodicas5", "reteperiodicas6"]
            self.initialized = True # this is a falg to avoid multiple inicializations...
            # ensure if the folder csv exists...
            if not os.path.exists(self.base_dir):
                os.makedirs(self.base_dir, exist_ok=True)

    """
    this method helps me to process the data in the tables found after the h3 tags...
    """
    def _process_table_and_save_csv(self, table, text):
        # process the name of the csv file...
        file_name_csv = csvFileName(text)

        # create the CSV file path based...
        csv_file_path = Path(self.base_dir / f"{file_name_csv}.csv")

        try:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)

                # process the rows of the tables...
                rows = table.find_all('tr')

                for row in rows:
                    # get all cells in the row (both <th> and <td>)
                    cells = row.find_all(['th', 'td'])
                    cell_data = [cell.get_text(strip=True) for cell in cells]

                    # write the row to the csv file
                    csv_writer.writerow(cell_data)

            print(f"Data successfully saved to {csv_file_path}")
        except OSError as e:
            print(f"An error ocurred while saving the file: {e}")

    """
    this method helps me to make the scraping of the web provided...
    """
    def _scraping(self):
        # make the requests...
        response = requests.get(self.url)

        # check if the response was sucessfully...
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # loop through the h3 tags and find the ones with matching id from self.h3 list
            h3s = [soup.find('h3', id=h3_id) for h3_id in self.h3]

            # filter out any None value (if no h3 was found with the given id)
            h3s = [h3 for h3 in h3s if h3 is not None]

            if h3s:
                for h3 in h3s:
                    print(f"Found <3>: {h3.text.strip()}") # this prints the content of the h3...
                    # look for the table immediately following the <h3> element
                    table = h3.find_next('table')

                    # check if a table was found after the <h3>
                    if table:
                        print(f"Found a table under <h3> with text: {h3.text.strip()}")
                        # process the table data...
                        self._process_table_and_save_csv(table, h3.text.strip())
                    else:
                        print(f"No table found under <h3> with text: {h3.text.strip()}")
            else:
                print("No matching h3 elements found.")
        else:
            print(f"Failed to retrieve the webpages. Status code: {response.status_code}")