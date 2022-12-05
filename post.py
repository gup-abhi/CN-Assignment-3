import os


def post_data(request):
    # getting file name from the request
    file_name = request.split(' ')[1][1:]
    # file = open(file_name, "w")
    print(f"File Name - {file_name}")
    print(request)
    print(f"request.find('Overwrite') - {request.find('Overwrite')}")

    # checking file exists or not
    file_exist_flag = os.path.isfile(file_name)

    # getting overwrite flag value from the request
    index_of_overwrite = request.find('Overwrite')
    overwrite_flag = request[index_of_overwrite + 11: index_of_overwrite + 15]
    print(f"overwrite_flag - {overwrite_flag}")
    print(f"length of overwrite - {len(overwrite_flag)}")

    print("Checking file opened")
    print(f"os.access(os.getcwd() + f'/{file_name}', os.W_OK) - {os.access(os.getcwd() + f'/{file_name}', os.W_OK)}")

    # checking overwrite flag
    print(f"os.path.exists - {os.path.exists(os.getcwd() + f'/{file_name}')}")
    if overwrite_flag == 'True':
        if (not os.path.exists(os.getcwd() + f"/{file_name}")) or os.access(os.getcwd() + f"/{file_name}", os.W_OK):
            print("W")
            file = open(file_name, "w")
        else:
            return "HTTP/1.0 409 File is being accessed by another client."
    else:
        print("O")
        if (not os.path.exists(os.getcwd() + f"/{file_name}")) or os.access(os.getcwd() + f"/{file_name}", os.W_OK):
            file = open(file_name, "a")
        else:
            return "HTTP/1.0 409 File is being accessed by another client."

    # getting data from the request
    index_of_body = request.find('Body:')
    data = request[index_of_body + 6:]
    print(f"Data - {data}")

    # writing in the file
    file.write(data)

    print(f"os.path.isfile(file_name) - {os.path.isfile(file_name)}")

    # sending response
    if file_exist_flag:
        return "HTTP/1.0 200 Successfully Updated"
    else:
        return "HTTP/1.0 201 Successfully Created"
