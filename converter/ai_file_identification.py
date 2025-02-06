# converter/ai_file_identification.py
import magic

def identify_file_type(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type