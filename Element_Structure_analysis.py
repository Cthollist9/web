#用于分析密码元素与结构
import json
import re

def analysis_element_structure(args):
    with open(args.datafile) as file:
        data = json.load(file)
    password_count = len(data)

    EN_count = 0
    number_count = 0
    symbol_count = 0
    total_count = 0
    symbol_dict = {}
    structure_dict = {}
    elements_dict = {}
    for password in data:
        if password != "":
            elements = ""
            structure = ""
            temp = ""
            UPPER_letters = re.sub(r'[^A-Z]', '', password)
            LOWER_letters = re.sub(r'[^a-z]', '', password)
            numbers = re.sub(r'[^0-9]','',password)
            symbols = re.sub(r'[0-9a-zA-Z]','',password)
            EN_len = len(UPPER_letters) + len(LOWER_letters)
            number_len = len(numbers)
            symbol_len = len(symbols)
            if number_len != 0:
                elements += "|D|"
            if UPPER_letters != "":
                elements += "|UL|"
            if LOWER_letters != "":
                elements += "|LL|"
            if symbol_len != 0:
                elements += "|S|"
            if elements not in elements_dict:
                elements_dict[elements] = 1
            elif elements in elements_dict:
                elements_dict[elements] += 1
            for i in range(0, len(password)):
                if password[i].isdigit():
                    temp += "D"
                elif password[i].isalpha():
                    temp += "L"
                else:
                    temp += "S"
                    if password[i] not in symbol_dict:
                        symbol_dict[password[i]] = 1
                    else:
                        symbol_dict[password[i]] += 1
            structure += temp[0]
            count = 1
            for i in range(1, len(temp)):
                if temp[i] == temp[i-1]:
                    count += 1
                elif temp[i] != temp[i-1]:
                    structure += f"{count}"
                    structure += temp[i]
                    count = 1
                if i == len(temp) - 1:
                    structure += f"{count}"
                
            if structure not in structure_dict:
                structure_dict[structure] = 1
            else:
                structure_dict[structure] += 1

            EN_count += EN_len
            number_count += number_len
            symbol_count += symbol_len
            total_count += len(password)

    sorted_symbols = sorted(symbol_dict, key=lambda key:symbol_dict[key], reverse=True)
    sorted_structures = sorted(structure_dict, key=lambda key:structure_dict[key], reverse=True)
    sorted_elements = sorted(elements_dict, key=lambda key:elements_dict[key], reverse=True)
    print(f"字母元素在所有口令中占比为:{EN_count/total_count * 100}%\n")
    print(f"数字元素在所有口令中占比为:{number_count/total_count * 100}%\n")
    print(f"符号元素在所有口令中占比为:{symbol_count/total_count * 100}%\n")
    print(f"TOP10 symbols:\n{sorted_symbols[0]}:{ (symbol_dict[sorted_symbols[0]]/symbol_count) *100 }%\n\
    {sorted_symbols[1]}:{ (symbol_dict[sorted_symbols[1]]/symbol_count) *100 }%\n\
    {sorted_symbols[2]}:{ (symbol_dict[sorted_symbols[2]]/symbol_count) *100 }%\n\
    {sorted_symbols[3]}:{ (symbol_dict[sorted_symbols[3]]/symbol_count) *100 }%\n\
    {sorted_symbols[4]}:{ (symbol_dict[sorted_symbols[4]]/symbol_count) *100 }%\n\
    {sorted_symbols[5]}:{ (symbol_dict[sorted_symbols[5]]/symbol_count) *100 }%\n\
    {sorted_symbols[6]}:{ (symbol_dict[sorted_symbols[6]]/symbol_count) *100 }%\n\
    {sorted_symbols[7]}:{ (symbol_dict[sorted_symbols[7]]/symbol_count) *100 }%\n\
    {sorted_symbols[8]}:{ (symbol_dict[sorted_symbols[8]]/symbol_count) *100 }%\n\
    {sorted_symbols[9]}:{ (symbol_dict[sorted_symbols[9]]/symbol_count) *100 }%\n")
    print(f"Structures:\n{sorted_structures[0]}:{ (structure_dict[sorted_structures[0]]/password_count) *100 }%\n\
    {sorted_structures[1]}:{ (structure_dict[sorted_structures[1]]/password_count) *100 }%\n\
    {sorted_structures[2]}:{ (structure_dict[sorted_structures[2]]/password_count) *100 }%\n\
    {sorted_structures[3]}:{ (structure_dict[sorted_structures[3]]/password_count) *100 }%\n\
    {sorted_structures[4]}:{ (structure_dict[sorted_structures[4]]/password_count) *100 }%\n\
    {sorted_structures[5]}:{ (structure_dict[sorted_structures[5]]/password_count) *100 }%\n\
    {sorted_structures[6]}:{ (structure_dict[sorted_structures[6]]/password_count) *100 }%\n\
    {sorted_structures[7]}:{ (structure_dict[sorted_structures[7]]/password_count) *100 }%\n\
    {sorted_structures[8]}:{ (structure_dict[sorted_structures[8]]/password_count) *100 }%\n\
    {sorted_structures[9]}:{ (structure_dict[sorted_structures[9]]/password_count) *100 }%\n")
    print(f"Elements:\n{sorted_elements[0]}:{ (elements_dict[sorted_elements[0]]/password_count) *100 }%\n\
    {sorted_elements[1]}:{ (elements_dict[sorted_elements[1]]/password_count) *100 }%\n\
    {sorted_elements[2]}:{ (elements_dict[sorted_elements[2]]/password_count) *100 }%\n\
    {sorted_elements[3]}:{ (elements_dict[sorted_elements[3]]/password_count) *100 }%\n\
    {sorted_elements[4]}:{ (elements_dict[sorted_elements[4]]/password_count) *100 }%\n\
    {sorted_elements[5]}:{ (elements_dict[sorted_elements[5]]/password_count) *100 }%\n\
    {sorted_elements[6]}:{ (elements_dict[sorted_elements[6]]/password_count) *100 }%\n\
    {sorted_elements[7]}:{ (elements_dict[sorted_elements[7]]/password_count) *100 }%\n\
    {sorted_elements[8]}:{ (elements_dict[sorted_elements[8]]/password_count) *100 }%\n\
    {sorted_elements[9]}:{ (elements_dict[sorted_elements[9]]/password_count) *100 }%\n")
