
# Tools for building a command line interface.
# Instanciate to use.

import re


class CliTools:

    # Clear terminal window
    def clear(self):
        print(
            'If you can see this without scrolling up your terminal does not support ANSI.')
        print('\033[2J')

    # Prints a block of characters of width xlen and height of length ylen
    def separator(self, xlen=30, ylen=1, char='=') -> str:
        print((f"{char * xlen}\n") * ylen)

    # Bool selection (yes or no)
    def yes_no(self, q, new_line=True) -> bool:
        y_pattern = '(?:y$|Y$|^$)'
        n_pattern = '(?:n$|N$)'
        while True:
            response = input('\n' * new_line + f'{q} [y/n]: ')
            if re.match(y_pattern, response):
                return True
            elif re.match(n_pattern, response):
                return False

    def quiestion(self, q: str) -> str:
        while True:
            help_text = 'Please enter number designated to certain menu or\n"-h" to see help\n"-q" to exit'
            a = input(q)
            if a == '-h':
                print(help_text)
                continue
            elif a == '-q':
                return -1

            return a

    # Prints numbered list

    def list_print(self, items: list, index: list = None) -> None:
        # Preprocessing
        max_option_len = 0
        max_index_len = 0
        for i in range(len(items)):
            if len(items[i]) > max_option_len:
                max_option_len = len(items[i])
            if index != None and len(index[i]) > max_index_len:
                max_index_len = len(index[i])

        # Print
        for i in range(len(items)):
            sel = str(i) if index == None else index[i]
            print(
                '\033[100m' * (i % 2 == 0 and len(items) > 2) +
                sel +
                ': ' + ' ' * (max_index_len - len(sel)) +
                items[i] +
                ' ' * (max_option_len - len(items[i])) +
                '\033[0m'
            )

    # Prints menu and returns index of selection
    # Does not print options (on start) if quiet is True
    # Returns -1 on quit if -q is entered
    def menu(self, title, options: list, index: list = None, quiet=False) -> int:
        help_text = 'Please enter number designated to certain menu or\n"-h" to see help\n"-q" to exit menu\n"-m" to see menu options\n"-c" to clear window\n'

        print('\n' + title)

        if not quiet:
            self.list_print(options, index)

        while True:
            try:
                response = input(
                    'Select option' + f' [0-{len(options)-1}]' * (index == None) + ': ')
                if response == '-h':
                    print(help_text)
                    continue
                elif response == '-q':
                    return -1
                elif response == '-m':
                    return self.menu(title, options, index)
                elif response == '-c':
                    self.clear()
                    return self.menu(title, options, index, quiet)

                if index == None:
                    response = int(response)
                    if response >= len(options) and response < 0:
                        raise ValueError
                else:
                    if response not in index:
                        raise ValueError
            except ValueError:
                print('Invalid input.\n' + help_text)
                continue

            return response
