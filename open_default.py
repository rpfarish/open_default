import os
import shlex
from dataclasses import dataclass
from typing import List
import webbrowser
from parsefile import parse_sites_file

SOURCE = "sites2.txt"


# todo what about sites that need authentication?


def get_command():
    return shlex.split(input(">>>"))


@dataclass
class Command:
    """Class that represents a command."""
    command: str
    arguments: List[str]


def get_help(arguments, sites_data):
    match arguments:
        case ['all', *rest]:
            print('Opens all links')
        case ['copyright', *rest]:
            print('Prints the copyright')
        case ['help', *rest]:
            print('Display information about builtin commands.')
        case ['restart', *rest]:
            print('re-parse the source file and reload it')
            sites_data.display_sites()
        case ['type', *rest]:
            print('Shows the category of all available types')
        case ['quit', *rest]:
            print("help: no help topics match 'quit'.")
        case []:
            print('all\t\t       Opens all links')
            print('copyright\t   Prints the copyright')
            print('help\t\t   Gives info based on current context')
            print('restart\t\t   Restarts the program and reloads from the file')
            print('type\t\t   Changes current type name')
            print('types\t\t   Shows all available types')
            print('quit\t\t   Exits the program')
        case other:
            print(f'Get-Help : Get-Help could not find "{"".join(other)}" in a help file in this session.')


def open_feline():
    i = 'iuuqt;00xxx/zpvuvcf/dpn0xbudi@w>WtgsV7Z[YuN'
    webbrowser.open(''.join([str(chr(ord(j)-1)) for j in i]))


def main(*args, **kwargs):
    source, *_ = args
    print('Open Default 2.0.0 (tags//v3.10.0:b494f59, Oct 5 2021, 20:27:44 -0400)')
    print('Type "help" or "copyright" for more information.')
    # open many different types of websites
    # call websites by number, name, or nickname

    sites_data = parse_sites_file(source)
    print("Ready")
    while True:
        reply = input(">>>").strip()
        if not reply:
            continue

        command, *arguments = shlex.split(reply)
        command = Command(command, arguments)

        match command:
            case Command(command="help", arguments=[*rest]):
                get_help(rest, sites_data)
                print("hi, hope this was helpful")

            case Command(command="restart", arguments=["--force" | "-f", *rest]):
                print('-' * 20, 'RESTART', '-' * 20)
                sites_data = parse_sites_file(source, force_load=True)
            case Command(command="restart", arguments=["--validate" | "-v", *rest]):
                print('-' * 20, 'RESTART', '-' * 20)
                sites_data = parse_sites_file(source, force_validate=False)
            case Command(command="restart"):
                print('-' * 20, 'RESTART', '-' * 20)
                sites_data = parse_sites_file(source)

            case Command(command="cls", arguments=[*rest]):
                os.system('cls')

            case Command(command="ls" | "dir", arguments=["--category" | "-c", *rest]):
                sites_data.display_sites_by_category(rest)
            case Command(command="ls" | "dir", arguments=["--nickname" | "-n", *rest]):
                sites_data.display_sites_by_nickname(rest)
            case Command(command="ls" | "dir", arguments=[*rest]) if not any(rest):
                sites_data.display_sites()
            case Command(command="ls" | "dir", arguments=[*rest]):
                sites_data.display_sites_by_sub_categories(rest)

            case Command(command="cats", arguments=[*rest]):
                print("meow")
                sites_data.display_categories()
            case Command(command="meow", arguments=[*none]):
                open_feline()

            case Command(command="all", arguments=["--category" | "-c", *rest]):
                # todo double check categories exist
                # todo have sub-categories also be explicitly callable
                sites_data.open_by_category(rest)
            case Command(command="all", arguments=["-n" | "--nickname", *rest]):
                sites_data.open_by_nickname(rest)
            case Command(command="all", arguments=[*rest]) if not any(rest):
                sites_data.call_all()

            case Command(command="load", arguments=[filename]):
                print(f"Loading file: {filename}")
            case Command(command="save", arguments=[filename]):
                print(f"Saving file: {filename}")
            case Command(command="quit" | "exit" | "bye", arguments=["--force" | "-f", *rest]):
                print("Sending SIGTERM to all processes and quitting the program")
                quit()
            case Command(command="quit" | "exit" | "bye", arguments=[*rest]):
                print("Quitting the program")
                quit()
            case _:
                print(f"Unknown command: {command!r}")


if __name__ == '__main__':
    main(SOURCE)

    os.system('cls')
