"""
@file: Grep method implementation
Usage: grep [OPTION]... PATTERN [FILE]...
"""
from pathlib import Path
from threading import Thread
from dataclasses import dataclass
from typing import List
import argparse
import re
import queue
# import time

class MyExceptionError(Exception):
    """
    My Exception
    """
@dataclass
class SearchResult:
    """
    The search result
    """
    file:Path
    line_num: int
    matched_line: str
    before_context: List[str]
    after_context: List[str]

class GrepImpl:
    """
    Grep method implementation
    """

    def __init__(self) -> None:
        self.__parser = self.configure_parser()
        self.__arguments = self.__parser.parse_args()
        self.__lines_queue = queue.Queue(maxsize=5000)

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
        parser.add_argument('-c', '--count', action='store_true', help='print count of lines')
        parser.add_argument('-n', '--line-number', action='store_true', help='print line number')
        parser.add_argument('-r', '--recursive', action='store_true', help='recursive finding')
        parser.add_argument('-A', '--after-context', type=int, help='count line after finding')
        parser.add_argument('-B', '--before-context', type=int, help='count line before finding')
        parser.add_argument('-C', '--context', type=int, help='count line before and after finding')
        parser.add_argument('--exclude', type=Path, help='exclude file type')
        parser.add_argument('--include', type=str, help='include file type')

        return parser

    def queue_line(self, file_name:str, line:str, idx: int):
        """
        Process '-n' and print one line
        """
        if self.__arguments.line_number:
            self.__lines_queue.put(f'{file_name} : {idx} : {line}')
        else:
            self.__lines_queue.put(f'{file_name} : {line}')

    def queue_range(self, file_name:str, lines:list, rbegin:int, rend:int):
        """
        Print lines range
        """
        for i in range(rbegin, rend):
            self.queue_line(file_name, lines[i], i)

    def queue_count(self, file_name:str, count:int):
        """
        Process '-c' and print lines count
        """
        if self.__arguments.count:
            self.__lines_queue.put(f'Number of lines found in {file_name}: {count}')

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
            return re.search(pattern, line) is not None

        return pattern in line

    def process_file(self, file:Path, pattern:str):
        """
        Process one file. Process '-A', '-B', '-C'. Return count of processed lines
        """
        count = 0
        before_count = 0
        after_count = 0

        # Process '-A', '-B', '-C'
        if self.__arguments.before_context:
            before_count = self.__arguments.before_context

        if self.__arguments.after_context:
            after_count = self.__arguments.after_context

        if self.__arguments.context:
            before_count = self.__arguments.context
            after_count = self.__arguments.context

        # Process file and print results
        try:
            lines = file.read_text(encoding="utf-8").splitlines()
        except UnicodeError:
            self.queue_count(file, 0)
            return

        is_line_found = False

        for idx, line in enumerate(lines):
            if self.search_pattern_in_line(pattern, line):
                if before_count > 0 and not is_line_found:
                    self.__lines_queue.put('------')
                    self.queue_range(file, lines, max(0, idx - before_count), idx)

                is_line_found = True
                count +=1
                self.queue_line(file, line, idx)

            else:
                if after_count > 0 and is_line_found:
                    self.queue_range(file, lines, idx, min(idx + after_count, len(lines)))
                    self.__lines_queue.put('------')

                is_line_found = False

        self.queue_count(file, count)

    def process_file_list(self, files:Path, pattern:str):
        """
        Process file list. The method for thred run
        """
        for file in files:
            if file.is_file() and self.is_file_included(file):
                self.process_file(file, pattern)

    def is_file_included(self, file:Path)->bool:
        """
        Process '--exclude' command. Return True if file sall be processed
        """
        if self.__arguments.exclude:
            return not file.match(str(self.__arguments.exclude))

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

        threads:list[Thread] = []

        if path.is_file():
            # process only one file
            if not self.is_file_included(path):
                print('No file to process')
                return

            thread = Thread(target=self.process_file, args=(path, pattern))
            thread.start()
            threads.append(thread)
        else:
            # Process dirrectory
            if not self.__arguments.recursive:
                raise MyExceptionError(f'{path}' + ': Is a directory')

            # Process '-r'
            files = list(path.rglob(self.get_mask()))

            num_thread = 4
            files_per_thread = len(files) // num_thread
            for n in range(files_per_thread):
                files_count = min((n + 1) * files_per_thread, len(files))
                thr_files = files[n * files_per_thread: files_count]
                thread = Thread(target=self.process_file_list, args=(thr_files, pattern))
                thread.start()
                threads.append(thread)

        for th in threads:
            th.join()

        while not self.__lines_queue.empty():
            print(self.__lines_queue.get())
            self.__lines_queue.task_done()

def main():
    """
    Main implementation
    """
    my_grep = GrepImpl()
    my_grep.execute()

if __name__ == "__main__":
    main()
