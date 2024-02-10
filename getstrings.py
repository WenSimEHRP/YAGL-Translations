import re
import sys
import time
import argparse

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
        lines = [[line.split('//')[0].strip() if 'http' not in line else line.strip()] for line in input_list
                 if '"' in line and include_other_languages or any(x in line for x in language_keep_list)]
        return [input_list[1].split('//')[0].strip()] + lines
    
    def ProcessStringsOrError(input_list):
        lines = [[line.split('//')[0].strip() if 'http' not in line else line.strip()] for line in input_list if '"' in line]
        if include_other_languages or any(x in input_list[1] for x in language_keep_list):
            return [[('}\n' if add_curly_brackets else '') + input_list[1].split('//')[0].strip() + ('\n{' if add_curly_brackets else '')] + lines]
    
    return (
        [ProcessOptionalInfo(input_list[i]) for i in GetOptionalInfo(input_list)],
        [ProcessStringsOrError(input_list[i]) for i in GetStringsOrError(input_list)]
    )


def WriteFile(path, content, language_keep_list, replace_lang = None):
    def WriteNestedList(f, nested_list):
        for element in nested_list:
            if isinstance(element, list):
                WriteNestedList(f, element)
            elif element:
                if replace_lang is not None:
                    replaced_element = next((element.replace(lang, replace_lang) for lang in language_keep_list if lang in element), element)
                    f.write(f"{replaced_element}\n")
                else:
                    f.write(f"{element}\n")
    
    with open(path, 'w') as f:
        WriteNestedList(f, content)


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='This program is used for extracting strings from a yagl file')
    parser.add_argument('-i', '--input', type=str, required=True, help='The path to the file to be processed')
    parser.add_argument('-o', '--output', type=str, default='optional_info.txt', help='The path to the file to be written')
    parser.add_argument('-l', '--lang', type=str, default=None, help='The language to be written')
    parser.add_argument('-a', '--all', action='store_true', help='Include all languages')
    parser.add_argument('-c', '--curly', action='store_true', help='Add curly brackets')
    parser.add_argument('-k', '--keep', type=str, default='default,en_GB,en_US', help='Keep specific languages')

    args = parser.parse_args()

    print('Time taken, Total time taken, Description')

    input_list = OpenFile(args.input)
    file_open_time = time.time()
    print(f'{file_open_time - start_time:.2f}s, {file_open_time - start_time:.2f}s. Opened file: {args.input}')

    records = SplitRecords(input_list)
    split_time = time.time()
    print(f'{split_time - file_open_time:.2f}s, {split_time - start_time:.2f}s. Split into {len(records)} records')

    WriteFile(args.output, GetStrings(records, args.all, args.curly, args.keep.split(',')), args.keep.split(','), args.lang)
    write_time = time.time()
    print(f'{write_time - split_time:.2f}s, {write_time - start_time:.2f}s. Generated optional_info.txt')

    end_time = time.time()
    print(f'---------- finish ----------\nTotal time taken: {end_time - start_time:.2f}s.')
