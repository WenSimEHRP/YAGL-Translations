import re
import sys
import time

def OpenFile(path):
    try: 
        with open(path, 'r', encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
def SplitRecords(input_list):
    record_match = re.compile(r'^ *// *Record #*\d* *$')
    index_list = [0] + [index for index, line in enumerate(input_list) if re.match(record_match, line)] + [len(input_list)]
    return [input_list[index_list[i]:index_list[i+1]] for i in range(len(index_list)-1)]


def GetStrings(input_list, include_other_languages = False, add_curly_brackets = True, language_keep_list=['default', 'en_GB', 'en_US']):
    optional_info_match = re.compile(r'^ *optional_info.*$')
    string_match = re.compile(r'^ *strings|error_message *<.*> *$')

    def GetOptionalInfo(input_list):
        return [index for index, sublist in enumerate(input_list) if re.match(optional_info_match, sublist[1])]
    
    def GetStringsOrError(input_list):
        return [index for index, sublist in enumerate(input_list) if re.match(string_match, sublist[1])]
    
    def ProcessOptionalInfo(input_list):
        lines = [line.split('//')[0].strip() for line in input_list if '"' in line and include_other_languages or any(x in line for x in language_keep_list)]
        return [input_list[1].split('//')[0].strip()] + lines
    
    def ProcessStringsOrError(input_list):
        lines = [line.split('//')[0].strip() for line in input_list if '"' in line]
        if include_other_languages or any(x in input_list[1] for x in language_keep_list):
            return [[('}\n' if add_curly_brackets else '') + input_list[1].split('//')[0].strip() + ('\n{' if add_curly_brackets else '')] + lines]
    
    return (
        [ProcessOptionalInfo(input_list[i]) for i in GetOptionalInfo(input_list)],
        [ProcessStringsOrError(input_list[i]) for i in GetStringsOrError(input_list)]
    )

def WriteFile(path, content, replace_lang = None):
    def WriteNestedList(f, nested_list):
        for element in nested_list:
            if isinstance(element, list):
                WriteNestedList(f, element)
            elif element:
                f.write(f"{element.replace('default', replace_lang) if replace_lang else str(element)}\n")
    
    with open(path, 'w') as f:
        WriteNestedList(f, content)


if __name__ == "__main__":
    start_time = time.time()
    path = sys.argv[1]
    if len(sys.argv) < 2:
        print("Usage: python getstrings.py <path>")
        sys.exit(1)
    input_list = OpenFile(path)

    print('Time taken, Total time taken, Description')
    # 打开文件
    file_open_time = time.time()
    print(f'{file_open_time - start_time:.2f}s, {file_open_time - start_time:.2f}s. Opened file: {path}')

    # 分割记录
    records = SplitRecords(input_list)
    split_time = time.time()
    print(f'{split_time - file_open_time:.2f}s, {split_time - start_time:.2f}s. Split into {len(records)} records')

    # 写入文件
    WriteFile('optional_info.txt', GetStrings(records), 'zh_CN')
    write_time = time.time()
    print(f'{write_time - split_time:.2f}s, {write_time - start_time:.2f}s. Generated optional_info.txt')

    # 输出总用时
    end_time = time.time()
    print(f'---------- finish ----------\nTotal time taken: {end_time - start_time:.2f}s.')