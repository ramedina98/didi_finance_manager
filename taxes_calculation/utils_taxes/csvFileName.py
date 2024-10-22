# the fucntion csv file name helps me creating a name for the file, depending of the
# h3 text above the table, it has to be (semanal, mensual y anual)
import re
from utils.date_time import currentTime, currentYearMonth

def csvFileName(text):
    # key words list...
    key_words = ["semanales", "mensuales", "anual"]

    # create a regular expresion to looking for the required word...
    regex = r'\b(' + '|'.join(key_words) + r')\b'

    # search in the string...
    result = re.search(regex, text)

    # return the name of the file, depends of the found word...
    if result:
        return f"tabla_isr_{result.group(0)}_{currentYearMonth()}_{currentTime()}"
    else:
        return None # any word found...