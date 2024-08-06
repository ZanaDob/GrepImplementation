import argparse
from pathlib import Path
import re

class GrepImpl:
    """
    Grep method implementation
    """

    def __init__(self) -> None:
        self.__parser = self.configure_parser()
        self.__arguments = self.__parser.parse_args()


    def regular_expressions(self, path: Path, pattern: str):
        """
        To grep with regular expressions
        """

        print("Start regularExpressions implementation: " + f'{pattern} {path}')

        if path.is_dir():
            print(f'{path}' + ": Is a directory")
            return

        with open(path, encoding="utf-8") as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    print(f'{match.group()}: {line}')

    def configure_parser(self):
        """
        Parser configuration
        """
        parser = argparse.ArgumentParser(description='Grep command line')

        #parser.add_argument('pattern', type=str, required=True, help='the pattern to find')
        parser.add_argument('pattern', type=str, help='the pattern to find')
        parser.add_argument('path', type=Path, help='the pattern to find')
        #parser.add_argument('file', metavar='FILE', nargs='*', default=['-'],
        #                    help='the files to search')
        parser.add_argument('-E', '--extended-regexp', action='store_true',
                        help='expressions matches')
        parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='')
        parser.add_argument('-c', '--count', action='store_true',
                        help='')
        parser.add_argument('-n', '--line-number', action='store_true',
                        help='')
        parser.add_argument('-r', '--recursive', action='store_true',
                        help='')

        # -A NUM, --after-context=NUM
        # -B NUM, --before-context=NUM
        # -C NUM, -NUM, --context=NUM
        # -exclude=GLOB
        # --include=GLOB

        return parser

    def execute(self):
        """
        Main execution method
        """

        pattern = self.__arguments.pattern
        print(f'{pattern}')

        path = self.__arguments.path
        print(path)

        if self.__arguments.extended_regexp:
            self.regular_expressions(path, pattern)

def main():
    """
    Main implementation
    """
    my_grep = GrepImpl()
    my_grep.execute()


if __name__ == "__main__":
    main()
