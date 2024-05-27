# import pandas as pd

# def extract_data_from_excel(file_path):
#     xls = pd.ExcelFile(file_path) 
#     # Define a dictionary that maps sheet names to column names
#     sheets_columns = {
#         'CDS-C': 'C. FIRST-TIME, FIRST-YEAR ADMISSION',
#         'FT-FY ADMISSION': 'C. FIRST-TIME, FIRST-YEAR (FRESHMAN) ADMISSION'
#     }
#     # Iterate over the dictionary and read the first sheet that exists in the Excel file
#     for sheet, column in sheets_columns.items():
#         if sheet in xls.sheet_names:
#             da = pd.read_excel(xls, sheet_name=sheet)
#             break
        
#     start = (da[column] == 'C1').idxmax()
#     end = (da[column] == 'C3').idxmax()
#     data = da.loc[start:end]
#     d = {
#     'Index': data[data['Unnamed: 1'].notnull()][column].values,
#     'Contents': data[data['Unnamed: 1'].notnull()]['Unnamed: 1'].values,
#     # 'Values': data[data['Unnamed: 1'].notnull()]['Unnamed: 2'].values
#     }
#     df = pd.DataFrame(data=d)
#     df = df.fillna('')
#     return df.values

# import pandas as pd

# def extract_data_from_excel(excel_path):
#     data = {
#         "Total first-time, first-year men who applied": None,
#         "Total first-time, first-year women who applied": None,
#         "Total first-time, first-year of another gender who applied": None,
#         "Total first-time, first-year men who were admitted": None,
#         "Total first-time, first-year women who were admitted": None,
#         "Total first-time, first-year of another gender who were admitted": None,
#         "Total full-time, first-time, first-year men who enrolled": None,
#         "Total part-time, first-time, first-year men who enrolled": None,
#         "Total full-time, first-time, first-year women who enrolled": None,
#         "Total part-time, first-time, first-year women who enrolled": None,
#         "Total full-time, first-time, first-year of another gender who enrolled": None,
#         "Total part-time, first-time, first-year of another gender who enrolled": None,
#         "Total first-time, first-year (degree-seeking) who applied": None,
#         "Total first-time, first-year (degree-seeking) who were admitted": None,
#         "Total first-time, first-year (degree-seeking) enrolled": None,
#         "Number of qualified applicants offered a place on waiting list": None,
#         "Number accepting a place on the waiting list": None,
#         "Number of wait-listed students admitted": None
#     }    

#     def extract_numeric_value(cell_value):
#         numeric_value = ''.join(filter(str.isdigit, str(cell_value)))
#         return numeric_value

#     excel_data = pd.read_excel(excel_path, sheet_name=None)

#     for sheet_name, df in excel_data.items():
#         for index, row in df.iterrows():
#             for key in data:
#                 if any(key in str(cell) for cell in row):
#                     column_index = next(index for index, cell in enumerate(row) if key in str(cell))
#                     value = extract_numeric_value(row.iloc[column_index + 3])
#                     data[key] = value
#                     break

#     return data

import pandas as pd

def extract_numeric_value(cell_value):
        numeric_value = ''.join(filter(str.isdigit, str(cell_value)))
        return numeric_value

def extract_data_excel(file_path):

    data = {
        "Total first-time, first-year men who applied": None,
        "Total first-time, first-year women who applied": None,
        "Total first-time, first-year of another gender who applied": None,
        "Total first-time, first-year men who were admitted": None,
        "Total first-time, first-year women who were admitted": None,
        "Total first-time, first-year of another gender who were admitted": None,
        "Total full-time, first-time, first-year men who enrolled": None,
        "Total part-time, first-time, first-year men who enrolled": None,
        "Total full-time, first-time, first-year women who enrolled": None,
        "Total part-time, first-time, first-year women who enrolled": None,
        "Total full-time, first-time, first-year of another gender who enrolled": None,
        "Total part-time, first-time, first-year of another gender who enrolled": None,
        "Total first-time, first-year (degree-seeking) who applied": None,
        "Total first-time, first-year (degree-seeking) who were admitted": None,
        "Total first-time, first-year (degree-seeking) enrolled": None,
        "Number of qualified applicants offered a place on waiting list": None,
        "Number accepting a place on the waiting list": None,
        "Number of wait-listed students admitted": None
    }    

    
    excel_data = pd.read_excel(file_path, sheet_name=None)

    for sheet_name, df in excel_data.items():
        for index, row in df.iterrows():
            for key in data:
                if any(key in str(cell) for cell in row):
                    column_index = next(index for index, cell in enumerate(row) if key in str(cell))
                    value = extract_numeric_value(row.iloc[column_index + 3])
                    data[key] = value
                    break

    return data

