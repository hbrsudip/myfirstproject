# Load the workbook
path = 'test.xlsx'
import xlwings as xw

# Connect to an existing Excel instance or create a new one
app = xw.App(visible=False)

# Open the workbook
wb = app.books.open(path)

# Access the active sheet
sheet = wb.sheets['Review Protocol Cover Sheet']
sheet['F12'].value = "Hi"

# Save changes and close the workbook
try:
    wb.save('C:/Users/z0050604/OneDrive - ZF Friedrichshafen AG/Apps/My tools/RCR Test Automation/rough/test3.xlsx')
except Exception as e:
    print(e)
wb.close()

# Quit Excel
app.quit()
