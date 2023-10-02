# parser.py
import re
from dateutil.parser import parse

def parse_keywords(text_content):
    # Define a list of keywords to search for
    keywords = ['Assignment', 'Exam', 'Test', 'Quiz', 'Final', 'Midterm', 'Project']

    # Initialize a list to store occurrences of keywords
    keyword_occurrences = []
    keyword_dict = {}

    # Search for and extract occurrences of keywords in the text content
    for keyword in keywords:
        occurrences = re.findall(r'\b{}\b'.format(re.escape(keyword)), text_content, re.IGNORECASE)
        keyword_occurrences.extend(occurrences)
        keyword_dict[keyword] = len(keyword_occurrences)  
    return keyword_dict

def parse_tables(table):
    date_pattern = r'\b\d{1,2}(st|nd|rd|th)\b'  # Matches "1st," "12th," etc. (with mandatory st, nd, rd, or th)
    month_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b'
    week_pattern = r'\bweek\b'
    weight_pattern = r'\bweight\b'
    due_pattern = r'\bdue\b'
    percent_pattern = r'\b\d+\s?%\b'  # Matches percentages like "50%" or "50 %"
    grade_pattern = r'\bgrade\b|\bgrades\b'

    for row in table:
        if row is not None:
            # Check each cell in the row
            for cell in row:
                if cell is not None:
                    cell_text = str(cell).lower()

                # Check for the presence of the specified patterns
                    if (
                        re.search(date_pattern, cell_text)
                        or re.search(month_pattern, cell_text)
                        or re.search(week_pattern, cell_text)
                        or re.search(weight_pattern, cell_text)
                        or re.search(due_pattern, cell_text)
                        or re.search(percent_pattern, cell_text)
                        or re.search(grade_pattern, cell_text)
                        ):
                        return True  # Table contains all the specified patterns

    return False

def parse_schedule(text_content):
    # Define a regular expression pattern to match the week titles and content
    pattern = r"(Week \d+ - .*?)(?=Week \d+ - |$)"

    # Use re.findall to find all matching week titles and content
    matches = re.findall(pattern, text_content, re.DOTALL)

    # Extract week titles and content separately
    weekly_topics = [match.strip() for match in matches]

    return weekly_topics

def extract_grade_breakdown(text_content):
    # Define a regular expression pattern to match the "Grades" section
    pattern = r"Grades(.+?)(?=(Accommodations|Inclusion and Respect|Intellectual Honesty|Late Work Policy|Professionalism Policy|\Z))"
    
    # Use re.search to find the "Grades" section
    match = re.search(pattern, text_content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    
    if match:
        grades_section = match.group(1).strip()
        print(type(grades_section))
        return grades_section
    else:
        return None





