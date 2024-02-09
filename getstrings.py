import re
import json

# temp codes, would change later

def ReadFile(path):
    record_match = r'^ *// *Record *#\d*$'
    return_list = []
    record_list = []
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            # make a list of indexes of all lines that match the record_match
            record_index_list = [0]
            for index,line in enumerate(lines):
                if re.match(record_match, line):
                    record_list.extend(re.findall(r'\d+', line))
                    record_index_list.append(index)
                    strings = []
                    for line in lines[record_index_list[-2]:record_index_list[-1]]:
                        # 分割每一行，取"//"之前的部分，并去除两端的空白
                        part = line.split('//')[0].strip()
                        # 只有当part不是空字符串时，才将其添加到strings中
                        if part != '':
                            strings.append(part)
                    return_list.append(strings)
            # append all lines between the record indexes to the return list
                

        return return_list, record_list
    
    except FileNotFoundError:
        print("File not found")
        return None
    
def MatchStrings(list):
    optional_info_match = r'optional_info'
    error_message_match = r'error_message *<.*default.*> *'
    strings_match = r'strings *<.*default.*> *'
    report_list = []
    for i in range(len(list)):
        if re.match(optional_info_match, list[i][0]) or re.match(strings_match, list[i][0]) or re.match(error_message_match, list[i][0]):
            report_list.append(i)
    print(report_list)
    return report_list



def WriteFile(path, data):
    try:
        with open(path, 'w') as file:
            file.write(data)
    except FileNotFoundError:
        print("File not found")
        return None


def main():
    path = 'sprites/jptrains.yagl'
    list, records = ReadFile(path)
    # print(list)
    # MatchStrings(list)
    strings = ''
    record_align = max(len(str(record)) for record in records)
    strings += f"{'Rc':<{record_align}}|String\n"
    for i in MatchStrings(list):
        for j in list[i]:
            j = j.strip()
            if j != '' and ('"' in j or 'optional_info' in j or 'error_message' in j or 'strings' in j):
                strings += f"{records[i]:<{record_align}}|{j}\n"
    WriteFile('text.txt', strings)

if __name__ == "__main__":
    main()