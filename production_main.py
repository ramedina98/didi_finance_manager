# This file is just meanwhile production...
from taxes_calculation.classes_taxes.WebScraping_isr import IsrScraping
from taxes_calculation.classes_taxes.TaxesCalculator import TaxesCalculator

scraping = IsrScraping()
taxes = TaxesCalculator(3000, 2000, 3000)

taxes.processCsvFiles()

print(f"ISR: {taxes.getIsr(17600, "monthly")}")