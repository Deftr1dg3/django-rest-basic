
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError


def valiodate_file_size(file: UploadedFile) -> None:
    max_size_kb = 5000 
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files can not be larger than {max_size_kb} KB.')
    


