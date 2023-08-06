# Excel Splitter

This is a package which will allow you to quickly split a single Excel sheet into either separate tabs of the same report or into different Excel reports.

IMPORTANT: Your sheet must contain a header row to function properly!

Once installed, you can call the split_sheet() function which contains the following parameters: 

split_sheet(split_type, input_report_path, column_number_to_split_by)

ACCEPTED PARAMETER VALUES:

split_type = "separate_files" or "split_tabs"
input_report_path = the path to the report to be split
column_number_to_split_by = the # of the Excel column to split by (A = 1, B = 2, C =3, etc.)

EXAMPLE OF SPLITTING AN EXCEL SHEET BY UNIQUE VALUES IN COLUMN B INTO DIFFERENT REPORTS

split_sheet(split_type='separate_files, input_report_path='PATH_TO_REPORT.xlsx', column_number_to_split_by=2)

KNOWN ISSUE: 

The current version of this script does not support transfer of formulas!!