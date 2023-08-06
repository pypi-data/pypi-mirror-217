# ResFeci for Excel

In it's current state, this package will allow you to quickly split a single Excel sheet into either separate tabs within the same report or into different Excel reports.  For example, if Column 'B' of your Excel report contains "Names" and "Jack" appears in 3 rows and "Jill" appears in 2, then, this will split the report into 2 separate reports (one for only Jack's rows and another for only Jill's)---or, this will create a new report tabs entitled "Jack" and "Jill".

**IMPORTANT: Your sheet must contain a header row to function properly!**


## EXAMPLE OF SPLITTING AN EXCEL SHEET BY UNIQUE VALUES IN COLUMN B INTO DIFFERENT REPORTS

from resfeci import excel_split

excel_split.split_sheet(split_type= 'separate_files' , input_report_path= 'PATH_TO_REPORT.xlsx' , column_number_to_split_by=2)


## EXAMPLE OF SPLITTING AN EXCEL SHEET BY UNIQUE VALUES IN COLUMN B INTO DIFFERENT TABS OF THE SAME REPORT

from resfeci import excel_split

excel_split.split_sheet(split_type= 'split_tabs' , input_report_path= 'PATH_TO_REPORT.xlsx' , column_number_to_split_by=2)


**PARAMETER DESCRIPTIONS**

split_type = must be either "separate_files" or "split_tabs"

input_report_path = the path to the report to be split

column_number_to_split_by = the NUMBER of the Excel column to split by (A = 1, B = 2, C =3, etc.)

**DEPENDENCIES**
Openpyxl
Pandas

**KNOWN ISSUE** 
The current version of this script does not support transfer of formulas!!