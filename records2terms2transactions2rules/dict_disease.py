import os
import json
import csv
import ast

allCount = {}


def bytes_to_string(input_bytes):
    input_bytes = input_bytes.decode('UTF-8', 'ignore').replace('\n', '').replace('\r', '.').encode('ascii', 'ignore')  # remove chinese
    input_string = input_bytes.decode('ascii')
    return input_string


def ProcessData(inputString, dataInput):

    nowCount = {}

    dataInputDict = ast.literal_eval(dataInput)

    for denotations in dataInputDict["denotations"]:

        begin = denotations["span"]["begin"]
        end = denotations["span"]["end"]
        index = denotations["obj"]

        if index not in nowCount.keys():
            nowCount[index] = {}
            nowCount[index]["sentence"] = []

        nowCount[index]["name"] = inputString[begin:end:]

        # if len(nowCount[index]["sentence"]) >= 2: continue

        while begin != 0 and inputString[begin] != '.':
            begin -= 1
        while end != 0 and end != len(inputString) and inputString[end] != '.':
            end += 1
        nowCount[index]["sentence"].append(inputString[begin:end + 1:])

    return nowCount


def CombineData(nowCount):

    for index in nowCount:
        if index not in allCount.keys():
            allCount[index] = {}
            allCount[index]["times"] = 0
            allCount[index]["sentence"] = []

        allCount[index]["name"] = nowCount[index]["name"]
        allCount[index]["times"] += 1

        for sentence in nowCount[index]["sentence"]:
            # if len(allCount[index]["sentence"]) < 2:
            allCount[index]["sentence"].append(sentence)

    transaction_single = nowCount.keys()

    return transaction_single


def save_dict(BioConcept):
    directory = './patients/utf8/'

    for subdirectory in ['class_1', 'class_4']:
        transaction = []
        allCount.clear()

        for file_name in os.listdir(os.path.join(directory, subdirectory)):

            if os.path.splitext(file_name)[-1] == '.txt':
                tagged_file_path = os.path.join(directory, subdirectory, 'post', file_name)
                original_file_path = os.path.join(directory, subdirectory, file_name)

                with open(tagged_file_path, 'r') as tagged_file:
                    tagged_text = tagged_file.read()
                with open(original_file_path, 'rb') as original_file:
                    original_text = bytes_to_string(original_file.read())

                transaction.append(CombineData(ProcessData(original_text, tagged_text)))

        output_file_path = os.path.join(directory, subdirectory, '%s_dict.json' % BioConcept)
        with open(output_file_path, 'w') as output_file:
            json.dump(allCount, output_file)

        transaction_file = open(os.path.join(directory, subdirectory, 'transaction_Disease.csv'), 'w')
        transaction_writer = csv.writer(transaction_file)

        for transaction_single in transaction:
            for i in range(len(transaction_single)):
                transaction_single[i] = allCount[transaction_single[i]]["name"]
            transaction_writer.writerow(transaction_single)

        transaction_file.close()
