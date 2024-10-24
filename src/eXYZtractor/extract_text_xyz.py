from PyPDF2 import PdfReader
import re

def combine_strings(char_list):
    result = ''.join(char_list).split('\n')
    return result

def check_and_extract_matching_part(line, pattern):
    match = re.search(pattern, line)
    if match:
        return True, match.group(0)
    else:
        return False, None
    
def write_text_to_xyz(fname, text):

  with open(fname, 'w') as file:
        file.write(f"{len(text)}\n")
        file.write("\n")
        for line in text:
            file.write(line if line.endswith("\n") else f"{line}\n")

def get_xyz_from_pdf(path, prefix=None):

    pattern_match = r'\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)'
    reader = PdfReader(path)

    text_ongoing = False
    detected_text = []
    num_xyzs = 0

    for page_num in range(len(reader.pages)):

        page = reader.pages[page_num]
        text = page.extract_text()
        text = combine_strings(text)

        for line in text:
            found, matching_part = check_and_extract_matching_part(line, pattern_match)
            if found:
                text_ongoing = True
                detected_text.append(matching_part)
            else:
                text_ongoing = False

            if text_ongoing == False and len(detected_text) > 0:
                write_text_to_xyz(fname=f'Coordinates_{num_xyzs}.xyz' if prefix is None else f'{prefix}_{num_xyzs}.xyz', text=detected_text)
                detected_text = []
                num_xyzs += 1

    print("Extraction complete")