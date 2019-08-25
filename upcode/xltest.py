from openpyxl import Workbook
from openpyxl import load_workbook


fname='temp1.xlsm'


wb=load_workbook(filename='temp.xlsm', read_only=False, keep_vba=True)
wb2=wb

wb2.save(filename=fname)