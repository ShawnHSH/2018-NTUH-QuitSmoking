import os
from urllib import request, error
import time


def bytes_to_string(input_bytes):
    input_bytes = input_bytes.decode('UTF-8', 'ignore').replace('\n', '').replace('\r', '.').encode('ascii', 'ignore')  # remove chinese
    input_string = input_bytes.decode('ascii')
    return input_string


def all_post(BioConcept):
    directory = './patients/utf8/'
    for subdirectory in ['class_1', 'class_4']:
        for file_name in os.listdir(os.path.join(directory, subdirectory)):
            try:
                os.mkdir(os.path.join(directory, subdirectory, 'post'))
            except:
                pass
            if os.path.splitext(file_name)[-1] == '.txt':
                full_directory = os.path.join(directory, subdirectory, file_name)
                with open(full_directory, 'rb') as input_file:
                    print(full_directory)

                    input_bytes = input_file.read()
                    input_string = bytes_to_string(input_bytes)

                tagged_bytes = post_to_pubtator(input_string, BioConcept)
                if type(tagged_bytes) is bytes and len(tagged_bytes) != 0:
                    dir_name, file_name = os.path.split(full_directory)
                    with open(os.path.join(dir_name, 'post', file_name), 'wb') as output_file:
                        output_file.write(tagged_bytes)


def post_to_pubtator(input_string, BioConcept):
    json_string = '{"text":"%s"}' % input_string
    # print(json_string)
    json_bytes = json_string.encode('ascii')

    # start_time = time.time()
    session_number_file = request.urlopen('https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/%s/Submit/' % BioConcept, json_bytes)
    session_number = session_number_file.read()
    session_number_file.close()
    session_number = session_number.decode('utf-8')
    print(session_number)

    code = 404
    tagged_file = ''
    receive_url = 'https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/%s/Receive/' % session_number

    # empty = False
    while code == 404 or code == 501:
        time.sleep(5)
        try:
            tagged_file = request.urlopen(receive_url)
            tagged_bytes = tagged_file.read()
            # print(tagged_bytes.decode('utf-8'))
            tagged_file.close()

            return tagged_bytes

        except error.HTTPError as e:
            code = e.code
        except error.URLError as e:
            code = e.code
        else:
            code = tagged_file.getcode()

    # end_time = time.time()
    # print(end_time - start_time)


all_post('DNorm')
