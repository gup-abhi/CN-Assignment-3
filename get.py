from pathlib import Path
import os
import socket


def get_data(request):
    RESPONSE_FORMAT = '''
HTTP/1.0 200
    '''

    extension_to_type = {
        'txt': "text",
        'html': "html"
    }

    extension_to_disposition = {
        "html": "inline",
        "txt": "attachment"
    }

    print(f'Request received in get_data() - {request}')
    file_address = request.split(' ')[1]

    print(f"file address - {file_address}")

    # handle security
    if file_address.find('/..') != -1:
        return "HTTP/1.0 400 Not Allowed"
    else:
        if file_address == '/':
            files = '\n'.join([i.name for i in Path(os.getcwd()).iterdir() if i.is_file()])
            # files = ''
            print(f'Files in working directory')
            # print(f'Files found in main directory - {files}')
            RESPONSE_FORMAT += '''
Body:
Files -
{}
            '''
            print(f"Response sending - {RESPONSE_FORMAT.format(files)}")

            return RESPONSE_FORMAT.format(files)
        else:
            filename = file_address[1:]
            print(f'Filename - {filename}')

            file_extension = filename.split(".")[1]

            # try:
            if os.path.exists(os.getcwd() + f"/{filename}"):
                file_data = open(filename, "r").read()

                RESPONSE_FORMAT += '''
Content-Type: {}
Content-Disposition: {}

Body:
Files Data -
{}
                                    '''
                print(f"Response sending - {RESPONSE_FORMAT.format(extension_to_type[file_extension], extension_to_disposition[file_extension], file_data[:len(file_data)])}")
                return RESPONSE_FORMAT.format(extension_to_type[file_extension], extension_to_disposition[file_extension], file_data[:len(file_data)])
            else:
                print("File not found")
                return "HTTP/1.0 404 Not Found"
