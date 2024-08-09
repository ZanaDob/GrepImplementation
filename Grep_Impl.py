"""
@file: Grep method implementation
Usage: grep [OPTION]... PATTERN [FILE]...
"""
from pathlib import Path
import argparse
import re

class MyExceptionError(Exception):
    """
    My Exception
    """

class GrepImpl:
    """
    Grep method implementation
    """

    def __init__(self) -> None:
        self.__parser = self.configure_parser()
        self.__arguments = self.__parser.parse_args()

    def configure_parser(self):
        """
        Parser configuration. Return parser.
        """
        parser = argparse.ArgumentParser(description='Grep command line')

        parser.add_argument('pattern', type=str, help='the pattern to find')
        parser.add_argument('path', type=Path, help='the pattern to find')

        parser.add_argument('-E', '--extended-regexp', action='store_true',
                        help='expressions matches')
        parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='ignore case in finding')
        parser.add_argument('-c', '--count', action='store_true',
                        help='print count of lines')
        parser.add_argument('-n', '--line-number', action='store_true',
                        help='print line number')
        parser.add_argument('-r', '--recursive', action='store_true',
                        help='recursive finding')
        parser.add_argument('-A', '--after-context', action='store', type=int, nargs=1,
                        help='count line after finding')
        parser.add_argument('-B', '--before-context', action='store', type=int, nargs=1,
                        help='count line before finding')
        parser.add_argument('-C', '--context', action='store', type=int, nargs=1,
                        help='count line before and after finding')
        parser.add_argument('--exclude', '--exclude', action='store', type=Path, nargs='?',
                        help='exclude file type')
        parser.add_argument('--include', '--include', action='store', type=str, nargs='?',
                        help='include file type')

        return parser

    def print_line(self, file_name:str, line:str, idx: int):
        """
        Process '-n' and print one line
        """
        if self.__arguments.line_number:
            print(f'{file_name} : {idx} : {line}')
        else:
            print(f'{file_name} : {line}')

    def print_range(self, file_name:str, lines:list, rbegin:int, rend:int):
        """
        Print lines range
        """
        for i in range(rbegin, rend):
            self.print_line(file_name, lines[i], i)

    def print_count(self, file_name:str, count:int):
        """
        Process '-c' and print lines count
        """
        if self.__arguments.count:
            print(f'Number of lines found in {file_name}: {count}')

    def search_pattern_in_line(self, pattern:str, line:str)->bool:
        """
        Process '-i', '-E' and search pattern in the line. Return True if line was found
        """
        # Process ignore case '-i'
        if self.__arguments.ignore_case:
            pattern = pattern.lower()
            line = line.lower()

        # Find pattern in line by expression '-E' or by line. Return True if pattern in the line
        if self.__arguments.extended_regexp:
            match = re.search(pattern, line)
            if match:
                return True
        else:
            if pattern in line:
                return True

        return False

    def process_file(self, file:Path, pattern:str)->int:
        """
        Process one file. Process '-A', '-B', '-C'. Return count of processed lines
        """
        count = 0
        before_count = 0
        after_count = 0

        # Process '-A', '-B', '-C'
        if self.__arguments.before_context:
            before_count = self.__arguments.before_context[0]

        if self.__arguments.after_context:
            after_count = self.__arguments.after_context[0]

        if self.__arguments.context:
            before_count = self.__arguments.context[0]
            after_count = self.__arguments.context[0]

        # Process file and print results
        try:
            lines = file.open(encoding="utf-8").readlines()
        except UnicodeError:
            self.print_count(file.name, 0)
            return count

        processed = False

        for idx, line in enumerate(lines):
            if self.search_pattern_in_line(pattern, line):

                if before_count > 0 and not processed:
                    print('------')
                    self.print_range(file.name, lines, max(0, idx - before_count), idx)

                self.print_line(file.name, line, idx)
                count +=1
                processed = True
            else:
                if after_count > 0 and processed:
                    self.print_range(file.name, lines, idx, min(idx + after_count, len(lines)))
                    print('------')
                processed = False

        self.print_count(file.name, count)

        return count

    def is_file_included(self, file:Path)->bool:
        """
        Process '--exclude' command. Return True if file sall be processed
        """
        if self.__arguments.exclude:
            return not file.match(str(self.__arguments.exclude))
        else:
            return True


    def get_mask(self)->str:
        """
        Process '--include' command. Return mask
        """
        if self.__arguments.include:
            return self.__arguments.include
        else:
            return '*'

    def execute(self):
        """
        Main execution method. Process '-r'
        """

        pattern:str = self.__arguments.pattern
        print(f'pattern: {pattern}')

        path:Path = self.__arguments.path
        print(f'path: {path}')

        if not path.exists():
            raise MyExceptionError('No any path in command line')

        lines_count = 0

        if path.is_file():
            # process only one file
            if self.is_file_included(path):
                lines_count += self.process_file(path, pattern)
            else:
                print('No file to process')
        else:
            # Process dirrectory
            if self.__arguments.recursive:
                # Process '-r'
                for file in path.rglob(self.get_mask()):
                    if file.is_file() and self.is_file_included(file):
                        lines_count += self.process_file(file, pattern)
            else:
                raise MyExceptionError(f'{path}' + ': Is a directory')

        self.print_count('total', lines_count)

def main():
    """
    Main implementation
    """
    my_grep = GrepImpl()
    my_grep.execute()

if __name__ == "__main__":
    main()
