from PyPDF2 import PdfReader
import re

def combine_strings(char_list):
    result = ''.join(char_list).split('\n')
    return result

def filter_out_page_numbers(strings):

    filtered_list = [
        s for s in strings 
        if not (
            s.strip().isdigit() or  #if string is just a digit
            (s.strip().startswith("S") and s.strip()[1:].isdigit()) or # if string starts with an S and ends with a digit and is only that
            s.strip() == "" # if string is empty
        )
    ]

    return filtered_list

def check_and_extract_matching_part(line, pattern):
    matches = re.findall(pattern, line)
    if matches:
        # Process matches as before
        results = [' '.join(match) if isinstance(match, tuple) else match for match in matches]
        
        # Get start and end positions of the first and last match
        first_match_start = re.search(pattern, line).start()
        last_match_end = re.search(f'{pattern}(?!.*{pattern})', line).end()
        
        # Extract content between the first and last matches
        in_between_content = line[first_match_start:last_match_end]
        
        # Check if there's intermediate non-matching, non-whitespace content and find its end position
        intermediate_content_matches = list(re.finditer(r'\S+', re.sub(pattern, ' ', in_between_content)))
        has_intermediate_content = bool(intermediate_content_matches)
        
        # If intermediate content exists, get the position after the last intermediate match
        after_intermediate_start = intermediate_content_matches[-1].end() if has_intermediate_content else last_match_end
        
        # Get remaining content after the intermediate content (if any) up to the end of the line
        remaining_content = line[after_intermediate_start:]
        
        # Determine if there's extra content after the last match
        has_extra_content = bool(remaining_content.strip())
        
        return True, results, (has_intermediate_content or has_extra_content), remaining_content.strip() if has_extra_content else None
    else:
        return False, None, False, None
    
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
    #pattern_match = r'(?<![\d.])\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)' #first character not part of float
    #pattern_match = r'\s+\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)' #at least one white space before first character
    pattern_match = r'(?<![\w.,;:!?\-\+])\b([A-Z][a-z]?|\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)'
    reader = PdfReader(path)

    text_ongoing = False
    detected_text = []
    preceding_lines = []
    num_xyzs = 0

    # CAN BE PLAYED AROUND WITH FOR HEADER
    #def visitor_body(text, cm, tm, fontDict, fontSize):
    #    y = tm[5]
    #    if y > 50 and y < 720:
    #        parts.append(text)

    for page_num in range(len(reader.pages)):

    #    parts = []

        page = reader.pages[page_num]
     #   text = page.extract_text(visitor_text=visitor_body)
     #   text = "".join(parts)
        text = page.extract_text()
        text = combine_strings(text)
        text = filter_out_page_numbers(text)

        i = 0
        while i < len(text):
            line = text[i]
            found, matching_part, extra_content, trailing_parts = check_and_extract_matching_part(line, pattern_match)
            if found:
                if len(detected_text) == 0:  # Start of new XYZ block
                    if len(preceding_lines) >= 3:
                        comment_lines = preceding_lines[-3:]
                    else:
                        comment_lines = preceding_lines[:]
                detected_text.extend(matching_part)
                if extra_content == True:
                    text_ongoing = False
                else:
                    text_ongoing = True
                if trailing_parts is not None:
                    print("TRAILING PARTS: ", trailing_parts)
                    text[i+1:i+1] = trailing_parts
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
            
            i += 1

    if len(detected_text) > 0:
        output_fname = determine_filename(comment_lines, detected_text, num_xyzs, prefix)
        write_text_to_xyz(fname=output_fname, text=detected_text)
        num_xyzs += 1

    print("Extraction complete")