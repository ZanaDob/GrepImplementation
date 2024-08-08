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

    def search_pattern_in_line(self, pattern:str, line:str)->bool:
        """
        Search pattern in line. Process '-i', '-E'
        return true if line found
        """
        # Process ignore case '-i'
        if self.__arguments.ignore_case:
            pattern = pattern.lower()
            line = line.lower()

        # Find pattern in line by expression '-E' or by line
        if self.__arguments.extended_regexp:
            match = re.search(pattern, line)
            if match:
                return True
        else:
            if pattern in line:
                return True

        return False

    def print_result(self, line:str, idx: int):
        """
        Print result. Process '-n'
        """
        if self.__arguments.line_number:
            print(f'{idx}: {line}')
        else:
            print(f'{line}')

    def process_file(self, file:Path, pattern:str)->int:
        """
        Process one file. Process '-c' for one file, '-A', '-B', '-C'
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
            after_count = self.__arguments.context[1]

        # Process file and print results
        try:
            lines = file.open(encoding="utf-8").readlines()
        except UnicodeError:
            return count

        processed = False

        for idx, line in enumerate(lines):
            if self.search_pattern_in_line(pattern, line):

                if before_count > 0 and not processed:
                    print(*lines[max(0, idx - before_count) : idx], sep='/n')

                self.print_result(line, idx)
                count +=1
                processed = True
            else:
                if after_count > 0 and processed:
                    print(*lines[idx : min(idx + after_count, len(lines))], sep='/n')

                processed = False

        if self.__arguments.count and count > 0:
            print(f'Number of lines found in file: {count}')

        return count

    def execute(self):
        """
        Main execution method. Process '-r', '-c'
        """

        pattern:str = self.__arguments.pattern
        print(f'{pattern}')

        path:Path = self.__arguments.path
        print(path)

        if not path.exists():
            raise MyExceptionError('No any path in command line')

        lines_count = 0

        # Start serch. Process '-r'
        if self.__arguments.recursive:
            for file in path.glob('*'):
                if not file.is_dir():
                    lines_count += self.process_file(file, pattern)
        else:
            if not path.is_dir():
                lines_count += self.process_file(path, pattern)
            else:
                raise MyExceptionError(f'{path}' + ': Is a directory')

        # Print count. Process '-c'
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
