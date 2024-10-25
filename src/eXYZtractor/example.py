from eXYZtractor.extract_text_xyz import get_xyz_from_pdf
import os

folder = 'example_pdfs'
#path_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.pdf')]
path_list = ['example_pdfs/header_1.pdf']

for i, path in enumerate(path_list):
    print(f"File {i}: {path}")
    get_xyz_from_pdf(path=path, prefix=f'example_{i}')