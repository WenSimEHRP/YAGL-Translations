import re
import sys
import time

def OpenFile(path):
    try: 
        with open(path, 'r', encoding = "utf-8") as f:
            # return a list of strings
            return f.readlines()
    except FileNotFoundError:
        print("File not found.\nPlease check the path and try again.")
        sys.exit(1)
    
def SplitRecords(list):
    # split the list by records
    # return a list of lists
    record_match = re.compile(r'^ *// *Record *\d* *$')
    index_list = [0]
    index_list.append([index for line, index in enumerate(list) if re.match(record_match, line)])
    return [list[index_list[i]:index_list[i+1]] for i in range(len(index_list)-1)]

def GetStrings(list):
    # get the strings from the list
    def GetStringsGetOptionalInfo(list):
        optional_info_match = re.compile(r'^ *optional_info *{*$')
        return [index for index, sublist in enumerate(list) if re.match(optional_info_match, sublist[1])]
    
    def GetStringsGetStringsOrError(list):
        string_match = re.compile(r'^ *strings|error_message *<.*> *$')
        return [index for index,sublist in enumerate(list) if re.match(string_match, sublist[1])]
    
    def GetStringsProcessOptionalInfo(list):
        # inputs flattened array
        return [line.split[0].strip() for line in list if '""' in line]
    
    def GetStringsProcessStringsOrError(list):
        # inputs a list of lists
        return [line.strip() for line in list if '""' in line]
    
    optional_info_index = GetStringsGetOptionalInfo(list)
    strings_or_error_index = GetStringsGetStringsOrError(list)

    return [strings for strings in GetStringsGetOptionalInfo(strings for strings in list)], [strings for strings in GetStringsGetStringsOrError(strings for strings in list)]


if __name__ == "__main__":
    # timer
    start_time = time.time()
    path = sys.argv[1]
    # if no path is given, show help message
    if len(sys.argv) < 2:
        print("Usage: python getstrings.py <path>")
        sys.exit(1)
    list = OpenFile(path)
    records = SplitRecords(list)
    GetStrings(records)
    print("--- %s seconds ---" % (time.time() - start_time))
