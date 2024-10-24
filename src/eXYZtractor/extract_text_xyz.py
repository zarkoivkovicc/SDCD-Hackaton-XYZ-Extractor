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

def determine_filename(relevant_lines, detected_text, num_xyzs, prefix):
    """
    This function determines the filename based on the last three preceding lines.
    """
    if prefix is not None:
        return f'{prefix}_{num_xyzs}.xyz'
    else:
        xyz_length = len(detected_text)
        for i in range(len(relevant_lines)-1, -1, -1):
            print(relevant_lines[i])
            line = relevant_lines[i].strip()
            words = line.split()
            skip_line = False
            for word in words:
                try:
                    num_value = float(word)
                    if num_value != int(num_value) or int(num_value) == xyz_length:
                        skip_line = True
                        break

                except ValueError:
                    continue
        
            if not skip_line:
                line = line.replace(' ', '_').replace('.', '')
                filename = f"{line}.xyz"
                return filename
    
    return f'Coordinates_{num_xyzs}.xyz'


def get_xyz_from_pdf(path, prefix=None):

    #pattern_match = r'\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)' #original
    #pattern_match = r'^\s*\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)' #no whitespaces, fucks with page-break
    pattern_match = r'(?<![\d.])\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)'
    reader = PdfReader(path)

    text_ongoing = False
    detected_text = []
    preceding_lines = []
    num_xyzs = 0

    for page_num in range(len(reader.pages)):

        page = reader.pages[page_num]
        text = page.extract_text()
        text = combine_strings(text)

        for line in text:
            found, matching_part = check_and_extract_matching_part(line, pattern_match)
            if found:
                if len(detected_text) == 0:  # Start of new XYZ block
                    if len(preceding_lines) >= 3:
                        comment_lines = preceding_lines[-3:]
                    else:
                        comment_lines = preceding_lines[:]
                text_ongoing = True
                detected_text.append(matching_part)
            else:
                text_ongoing = False

            if len(preceding_lines) >= 3:
                preceding_lines.pop(0)
            preceding_lines.append(line)

            if text_ongoing == False and len(detected_text) > 0:
                output_fname = determine_filename(comment_lines, detected_text, num_xyzs, prefix)
                write_text_to_xyz(fname=output_fname, text=detected_text)
                detected_text = []
                num_xyzs += 1

    if len(detected_text) > 0:
        output_fname = determine_filename(comment_lines, detected_text, num_xyzs, prefix)
        write_text_to_xyz(fname=output_fname, text=detected_text)
        num_xyzs += 1

    print("Extraction complete")