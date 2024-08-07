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
        Parser configuration
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
        parser.add_argument('-C', '--context', action='store', type=int, nargs=2,
                        help='count line before and after finding')
        # -exclude=GLOB
        # --include=GLOB

        return parser

    def search_pattern_in_line(self, pattern:str, line:str):
        """
        search pattern in line
        """
        if self.__arguments.ignore_case:
            pattern = pattern.lower()
            line = line.lower()

        return re.search(pattern, line)

    def print_result(self, line:str, idx: int):
        """
        print result
        """
        if self.__arguments.line_number:
            print(f'{idx}: {line}')
        else:
            print(f'{line}')

    def process_file(self, file:Path, pattern:str):
        """
        process one file
        """
        count = 0

        lines = file.open(encoding="utf-8").readlines()
        for idx, line in enumerate(lines):
            match = self.search_pattern_in_line(pattern, line)
            if match:
                count +=1
                self.print_result(line, idx)

        if self.__arguments.count:
            print(f'Number of lines found in file: {count}')

        return count

    def execute(self):
        """
        Main execution method
        """

        pattern = self.__arguments.pattern
        print(f'{pattern}')

        path = self.__arguments.path
        print(path)

        # print(self.__arguments.after_context)
        # print(self.__arguments.before_context)
        # print(self.__arguments.context)

        if not path.exists():
            raise MyExceptionError('No any path in command line')

        lines_count = 0

        if self.__arguments.recursive:
            for file in path.glob('*.txt'):
                if not file.is_dir():
                    lines_count += self.process_file(file, pattern)
        else:
            if not path.is_dir():
                lines_count += self.process_file(path, pattern)
            else:
                raise MyExceptionError(f'{path}' + ': Is a directory')

        if self.__arguments.count:
            print(f'Total number of lines found: {lines_count}')

def main():
    """
    Main implementation
    """
    my_grep = GrepImpl()
    my_grep.execute()


if __name__ == "__main__":
    main()
