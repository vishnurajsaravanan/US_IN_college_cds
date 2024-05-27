# import re
# from pdfminer.high_level import extract_text

# def extract_data_from_pdf(file_path):
#     # Extract text from the PDF file
#     text = extract_text(file_path)
#     # Split the text by 'Common Data Set'
#     print(text)
#     try:
#         pattern = r"(C\. FIRST-TIME, FIRST-YEAR* ADMISSION.*?C1.*?C2.*?)(Admission Requirements)"
#     except:
#         pass
#     match = re.search(pattern, text, re.DOTALL)
#     if match:
#         return match.group(1)q
#     else:
#         pattern = r"Common Data Set C: First-­Time, First-­Year (Freshman)* Admission"
#         match = re.search(pattern, text, re.DOTALL)
#         return match.group(1)

import pdfplumber

def extract_numeric_value(text):
        # Extract numeric values from text and remove commas
        numeric_value = ''.join(filter(str.isdigit, text.replace(",", "")))
        return numeric_value

def extract_data_pdf(file_path):

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
    

    with pdfplumber.open('./'+file_path) as pdf:
        for page in pdf.pages:
            text=page.extract_text()
            # print(text)
            for key,value in data.items():
                if key in text:
                    start_index = text.find(key) +len(key)
                    end_index =text.find("\n",start_index)
                    extracted_value = text[start_index:end_index].strip()
  
                    numeric_value = extract_numeric_value(extracted_value)
                    data[key] = numeric_value
    # print(data)
    return data

