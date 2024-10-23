"""
This class helps with the calculation of the taxes (IVA / ISR)

1. The calculation of the IVA tax is very simple, is 16%.
2. The calculation of the ISR is the complex part, it depends on the amount
of the income...

This class has to define the total of taxes to pay, how much the app has whitheld from me and
how much I still owe to pay...
"""

# TODO: change all the prints...

from pathlib import Path
from fpdf import FPDF
from datetime import datetime
import os
import csv

class TaxesCalculator:
    _instace = None # class variable to storage the only instance...

    def __new__(cls, *args, **kwargs):
        if not cls._instace: # if there is any instance, create one...
            cls._instace = super(TaxesCalculator, cls).__new__(cls)
        # returns the same instace always...
        return cls._instace

    def __init__(self, card_deposits, cash_deposits, invoices_amount):
        self.card = card_deposits
        self.cash = cash_deposits
        self.acreditable_iva = invoices_amount
        self.iva = 0.16
        # route to the folder where it is stored
        self.reports_dir = Path(Path.home() / "desktop/my_finances/reportes_taxes")
        self.csv_files_path = Path(Path.home() / "desktop/did_finace_manager/csv")
        # these lists contain the necessary data for the calculation of
        # income tax...
        self.isr_data_weekly = []
        self.isr_data_monthly = []
        self.isr_data_annul = []

    """
    Lists all CSV files in a the csv folder
    """
    def _listDir(self):
        csv_files = []

        # check if the folder exists...
        if not os.path.exists(self.csv_files_path):
            print(f"La carpeta no existe: {self.csv_files_path}")
            return csv_files

        # browse the folder and filter out those that are csv...
        for file in os.listdir(self.csv_files_path):
            if file.endswith(".csv"):
                csv_files.append(os.path.join(self.csv_files_path, file))

        return csv_files

    """
    reads a csv file and stores it in an array (list of lists). Each row of the CSV will be a sublist.
    """
    def _readAndStorage(self, csv_file):
        matriz = []

        #check if the csv file exists...
        if not os.path.exists(csv_file):
            print(f"El archivo {csv_file} no existe.")
            return matriz

        # read the csv file
        try:
            with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)

                # iterate over the row of the csv file...
                for index, row in enumerate(csv_reader, start=1):
                    if index > 2: # the information we need is from line 4 onwards...
                        matriz.append(row) # add each row into the array as a lists

            print(f"Archivo {csv_file} leído correctamente.")
        except Exception as e:
            print(f"Ocurrio un error al leer el archivo {csv_file}: {e}")

        return matriz

    """
    Processes all CSV files in the given folder, reading their contents and storing them in arrays..
    """
    def processCsvFiles(self):
        csv_files = self._listDir()

        # itera over each csv file found...
        for csv_file in csv_files:
            print(f"Leyendo archivo: {csv_file}")
            matriz = self._readAndStorage(csv_file)

            if "anual" in csv_file.lower():
                self.isr_data_annul = matriz
            elif "semanal" in csv_file.lower():
                self.isr_data_weekly = matriz
            elif "mensual" in csv_file.lower():
                self.isr_data_monthly = matriz

        print("Datos ISR anual:", self.isr_data_weekly)

    """
    This method helps with the calculation of the iva that I probably have to pay

    calculates, taxes already withheld (card), and taxes still to be paid(cash)
    """
    def _getIva(self, amount):
        # this function makes the iva calculation...
        def iva_calculation(amount, iva_rate):
            # this is the iva without deduction...
            return (amount / (1 + iva_rate)) * iva_rate
        # paid iva...
        iva = iva_calculation(amount, self.iva)

        # acreditable iva...
        acreditable_iva = iva_calculation(self.acreditable_iva, self.iva)
        # iva payable...
        iva_payable = iva - acreditable_iva

        return {
            "without_deduction": round(iva, 2),
            "with_deduction": round(iva_payable, 2)
        }

    """
    This method helps me to determine the ISR payable...
    """
    def getIsr(self, amount, period):
        # function to search the range...
        def searchRange(list, amount):
            # iterate each lists (row)
            for row in list:
                lower_limit = float(row[0]) # lower limit is in index 0
                upper_limit = float(row[1]) # upper limit is in indesx 1
                # check if the amount is between the lower and upper limit...
                if amount >= lower_limit and amount <= upper_limit:
                    return row

        # first determine which period to calculate (weekly, monthly or annual)...
        if period == "weekly":
            matriz = self.isr_data_weekly
        elif period == "monthly":
            matriz = self.isr_data_monthly
        elif period == "annual":
            matriz = self.isr_data_annul
        else:
            return 0 # this means, wrong period...

        # get the correct row of the table...
        row = searchRange(matriz, amount)

        # calculate ISR...
        surplus = amount - row[0]
        isr_surplus = surplus * row[3]
        isr_total = row[2] + isr_surplus

        # return the calculated ISR...
        return isr_total