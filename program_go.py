import os

from tree_sitter import Language, Parser

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'vendor/tree-sitter-go'
  ]
)
GO_LANGUAGE = Language('build/my-languages.so', 'go')

output1 = []
output2 = []
inner_list = []
inner_list_2 = []

import re
import enchant

regex_for_snake_case = "^[a-z](?!.*?[^a-z_]).*?[a-z]$"
regex_for_consecutive_capitals = ".*[A-Z]{2,}.*"
regex_for_capitals = "[A-Z]+"
regex_for_underscore = "_.*_$"
extern_under_snake_regex = "_[a-z]+_"
regex_for_underscores_side = ".*__.*$"
regex_for_camel_case = "([A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$)))"
regex_for_snake_words = "([a-z](?:[a-z]+|[A-Z]*(?=[A-Z]|$)))"
regex_for_first_camelcase = "^[a-z].*?(?=[A-Z])"
regex_for_short_words = "[a-z]+$"
dictionary = enchant.Dict("en_US")

anomalies = ["Capitalisation Anomaly", "Consecutive Underscores", "Dictionary Words",
             "Excessive Words", "External Underscores", "Identifier Encoding", "Long Identifier Name",
             "Naming Convention Anomaly", "Numeric Identifier Name", "Short Identifier Name"]

numbers_in_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
                    'thirteen', 'fourteen',
                    'fifteen', 'sixteen', 'seventeen', 'eighteen',
                    'nineteen', 'twenty', 'thirty', 'forty',
                    'fifty', 'sixty', 'seventy', 'eighty',
                    'ninety', 'zero', 'hundred']


def validation_characters(input_string, output_list):
    if len(input_string) > 20:
        if anomalies[6] not in output_list:
            output_list.append(anomalies[6])
            return False
    else:
        return True


def validation_short_names(input_string, output_list, valid_short_identifiers):
    if input_string in valid_short_identifiers:
        return True
    elif len(input_string) < 8:
        if anomalies[9] not in output_list:
            output_list.append(anomalies[9])
            return False
    else:
        return True


def validation_identifier_numbers(input_string, output_list):
    if input_string.find("_") != -1:
        count = 0
        result = input_string.split('_')

        for i in result:
            if i.lower() in numbers_in_words:
                count += 1
        if count == len(result):
            if anomalies[8] not in output_list:
                output_list.append(anomalies[8])
                return False

    if input_string in numbers_in_words:
        if anomalies[8] not in output_list:
            output_list.append(anomalies[8])
            return False

    result = any(c.isupper() for c in input_string)
    if result:
        count = 0
        words_camel_case = re.findall(regex_for_camel_case, input_string)
        # print("Yover camel cases  = ")
        # print(words_camel_case)
        for i in words_camel_case:
            count += len(i)

        if len(input_string) == count:
            count = 0
            for j in words_camel_case:
                if j.lower() in numbers_in_words:
                    count += 1
            if count == len(words_camel_case):
                if anomalies[8] not in output_list:
                    output_list.append(anomalies[8])
                    return False
    else:
        return True


def validation_snake_case(input_string, output_list):
    if input_string.find("_") != -1:
        # print("bool result is..", re.match(regex_for_snake_case, input_string))
        # print("bool result is..", re.match(extern_under_snake_regex, input_string))

        if re.match(regex_for_snake_case, input_string) is not None:
            # print("Snake case found")
            if re.match(regex_for_underscores_side, input_string) is not None:
                if anomalies[1] not in output_list:
                    output_list.append(anomalies[1])
                    return False
            else:
                return True
        else:
            if input_string[0] == '_' or input_string[-1] == '_':
                if anomalies[4] not in output_list:
                    output_list.append(anomalies[4])
                    return False
            elif re.match(regex_for_consecutive_capitals, input_string) is not None:
                if anomalies[0] not in output_list:
                    output_list.append(anomalies[0])
                    return False
            else:
                if anomalies[7] not in output_list:
                    output_list.append(anomalies[7])
                    # print("error string is", output_list)
                    return False

    else:
        return True


def validation_capitals(input_string, output_list):
    if input_string.find("_") != -1:
        return validation_snake_case(input_string, output_list)
    result = any(c.isupper() for c in input_string)
    if result:
        if re.match(regex_for_consecutive_capitals, input_string) is not None:
            if anomalies[0] not in output_list:
                output_list.append(anomalies[0])
                return False
    if re.match(regex_for_capitals, input_string) is not None:
        capital_words = re.findall(regex_for_capitals, input_string)
        if len(capital_words) == 1:
            return True
    else:
        return True


def validation_words_count(input_string, output_list):
    result = any(c.isupper() for c in input_string)
    # print("result is", result)
    if result:
        if input_string[0].lower() == input_string[0]:
            if len(re.findall(regex_for_capitals, input_string)) > 3:
                if anomalies[3] not in output_list:
                    output_list.append(anomalies[3])
                    return False
        if len(re.findall(regex_for_capitals, input_string)) > 4:
            if anomalies[3] not in output_list:
                output_list.append(anomalies[3])
                return False
    else:
        return True


def validation_camelcase(input_string, output_list):
    result = any(c.isupper() for c in input_string)
    if result:
        if input_string[0] == '_' or input_string[-1] == '_':
            return False

        if input_string[0].lower() == input_string[0]:
            if len(re.findall(regex_for_first_camelcase, input_string)) > 0:
                word = re.findall(regex_for_first_camelcase, input_string)[0]
                word_dict = dictionary.check(word)
                if not word_dict:
                    if anomalies[2] not in output_list:
                        output_list.append(anomalies[2])
                        return False
    else:
        return True


def snake_case_dict_check(input_string, output_list):
    if input_string.find("_") != -1:
        result = any(c.islower() for c in input_string)
        if result:
            words_snake_case = re.findall(regex_for_snake_words, input_string)
            # print("snake strings", words_snake_case)
            count = 0
            for i in words_snake_case:
                if dictionary.check(i.lower()):
                    count += 1
            if count == len(words_snake_case):
                return True
            else:
                if anomalies[2] not in output_list:
                    output_list.append(anomalies[2])
                    return False
    else:
        return True


def capitalization_anomaly(input_string, output_list):
    if re.match(regex_for_short_words, input_string):
        if not dictionary.check(input_string):
            if anomalies[2] not in output_list:
                output_list.append(anomalies[2])
                return False
    else:
        return True


def main_tests(input_string):
    output_list = []
    valid_short_identifiers = ['c', 'd', 'g', 'e', 'i', 'in', 'inOut', 'j', 'k', 'm', 'n', 'o', 'out', 't', 'x', 'y',
                               'z']
    validation_snake_case(input_string, output_list)
    validation_capitals(input_string, output_list)
    validation_characters(input_string, output_list)
    validation_short_names(input_string, output_list, valid_short_identifiers)
    validation_words_count(input_string, output_list)
    validation_camelcase(input_string, output_list)
    snake_case_dict_check(input_string, output_list)
    capitalization_anomaly(input_string, output_list)
    validation_identifier_numbers(input_string, output_list)
    return output_list


for root, dirs, files in os.walk(r'clone_files'):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.go'):
            # print(os.path.join(root, file))
            file1 = open(os.path.join(root, file), 'r', encoding='UTF8')

            data = file1.read()
            file1.close()
            code = data
            code_list = code.split('\n')
            parser = Parser()
            parser.set_language(GO_LANGUAGE)
            tree = parser.parse(bytes(code, "utf8"))

            l = [0]
            list = []


            def parser(root):
                if len(root.children) == 0:
                    return
                else:
                    for i in root.children:
                        if i.type == 'identifier':
                            list.append(i)
                            l[-1] += 1
                        parser(i)


            root1 = tree.root_node
            parser(root1)
            # print(list)

            for i in range(len(list)):
                line = list[i].start_point[0]
                start = list[i].start_point[1]
                end = list[i].end_point[1]
                inner_list.append(f'Identifier: {code_list[line][start:end]}')
                inner_list.append(f'Start point: {list[i].start_point}')
                inner_list.append(f'End point: {list[i].end_point}')
                output1.append(inner_list)
                inner_list = []

            textfile = open("output1.txt", "w")
            for element in output1:
                # print("element = ",element)
                textfile.write(str(element) + "\n")

            textfile.close()

            for i in range(len(list)):
                line = list[i].start_point[0]
                start = list[i].start_point[1]
                end = list[i].end_point[1]
                # print("string is..", code_list[line][start:end])
                result = main_tests(code_list[line][start:end])
                # print("result is", result)
                if len(result) == 0:
                    continue
                else:
                    inner_list_2.append(f'Identifier: {code_list[line][start:end]}')
                    inner_list_2.append(f'Start point: {list[i].start_point}')
                    inner_list_2.append(f'End point: {list[i].end_point}')
                    inner_list_2.append(result)
                    output2.append(inner_list_2)
                    inner_list_2 = []

            textfile = open("output2.txt", "w")
            for element in output2:
                # print("element = ",element)
                textfile.write(str(element) + "\n")

            textfile.close()

