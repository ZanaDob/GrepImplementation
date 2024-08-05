import argparse
import re

class GrepImpl:
    """
    Grep method implementation
    """

    def regular_expressions(self):
        """
        To grep with regular expressions
        """
        print("regularExpressions")

    def configure_parser(self):
        """
        Parser configuration
        """
        parser = argparse.ArgumentParser(description='Grep command line')

        parser.add_argument('pattern', type=str, help='the pattern to find')
        parser.add_argument('file', metavar='FILES', nargs='*', default=['-'],
                            help='the files to search')
        parser.add_argument('-E', '--extended-regexp', action='store_true',
                        help='expressions matches')

        return parser


    def execute(self):
        """
        Main execution method
        """
        parser = self.configure_parser()
        arguments = parser.parse_args()

        pattern = arguments.pattern
        print(pattern)

        file_list = arguments.file
        print(len(file_list))

def main():
    """
    Main implementation
    """
    my_grep = GrepImpl()
    my_grep.execute()


if __name__ == "__main__":
    main()
