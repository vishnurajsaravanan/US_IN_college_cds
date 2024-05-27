import re


# Get the name of the college
def clean_college(college):
    college = college.lower()
    return re.sub(r'[^\w\s]', '', college.split(" cds")[0])  # Remove symbols

def year(college):
    match = re.search(r'\b\d{4}-\d{2,4}\b', college)
    if match:
        return match.group(0)
    return None

def get_extension(file_name):
    match = re.search(r'\.\w+$', file_name)
    if match:
        return match.group(0)
    return None