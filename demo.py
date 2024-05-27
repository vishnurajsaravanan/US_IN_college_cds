# import pandas as pd

# da = pd.read_excel('./downloaded_files/Biola University CDS 2022-2023.xlsx', sheet_name='FT-FY ADMISSION')
# # there are many sheets find the one with 'CDS-C'
# print(da.columns)
# print(da)
#  # filter out rows where C1 is null
#     # return the first 5 rows
# d = {
#     'Index': da[da['Unnamed: 1'].notnull()]['C. FIRST-TIME, FIRST-YEAR (FRESHMAN) ADMISSION'].values,
#     'Contents': da[da['Unnamed: 1'].notnull()]['Unnamed: 1'].values,
#     'Values': da[da['Unnamed: 1'].notnull()]['Unnamed: 2'].values
# }
# column = 'C. FIRST-TIME, FIRST-YEAR (FRESHMAN) ADMISSION'
# start = (da[column] == 'C1').idxmax()
# end = (da[column] == 'C3').idxmax()
# data = da.loc[start:end]
# df = pd.DataFrame(data=d)
# print(df.fillna(''))

# # print(data[data['Unnamed: 1'].notnull()]['Unnamed: 1'].values, data[data['Unnamed: 1'].notnull()]['Unnamed: 2'].values)
# # print(data['C. FIRST-TIME, FIRST-YEAR ADMISSION'],data[data['Unnamed: 1'].notnull()])

import pandas as pd
# from extract_data_from_excel import extract_data_excel

# Path to your Excel file
excel_path = "./downloaded_files/albion college_2022-2023.xlsx"


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
    print(excel_data)

    for sheet_name, df in excel_data.items():
        for index, row in df.iterrows():
            for key in data:
                if any(key in str(cell) for cell in row):
                    column_index = next(index for index, cell in enumerate(row) if key in str(cell))
                    value = extract_numeric_value(row.iloc[column_index + 3])
                    data[key] = value
                    break

    return data

data = extract_data_excel(excel_path)
# Print the extracted data
for key, value in data.items():
    print(f"{key}: {value}")