import os
import pathlib
import shlex
import webbrowser
from dataclasses import dataclass
from typing import List

import requests

from fileparseerror import FileParseError
from sites import Sites

SOURCE = "sites2.txt"


# todo what about sites that need authentication?

def valid_url(url: str) -> bool:
    print('Validate Url:', url)
    try:
        requests.get(url)
    except requests.ConnectionError as exception:
        return False
    except requests.exceptions.MissingSchema as exception:
        return False
    return True


def parse_sites_file(file: str) -> Sites:
    print("Loading...")
    has_internet_connection = False
    # Check that the program has an internet connection
    try:
        # requests.get("http://www.google.com/")
        # requests.get("http://www.github.com/")
        has_internet_connection = False  # todo update after debugging
    except requests.ConnectionError as exception:
        pass

    with open(file) as f:
        file_path = f'"{os.path.join(pathlib.Path(__file__).parent.resolve(), file)}"'
        inside_braces, has_open_paren = False, False
        category = None
        open_paren_line_number = 0
        sites_data = Sites()
        # address duplicates
        # empty nicknames
        for line_num, line in enumerate(f.readlines(), 1):
            if line.startswith("#"):
                continue
            elif line.startswith("Category:") and not has_open_paren:
                _, *category = line.strip('\n').split(':')
                category = ":".join([i.strip() for i in category])
                continue
            elif line.startswith("Category:") and has_open_paren:
                raise FileParseError(file, file_path, '{', open_paren_line_number, "was never closed")

            match line.strip('\n').strip():
                case '':
                    continue
                case '{' if has_open_paren:
                    raise FileParseError(file, file_path, '{', open_paren_line_number, "was never closed")
                case '{':
                    inside_braces, has_open_paren = True, True
                    open_paren_line_number = line_num
                    data_sites = []
                case '}' if not has_open_paren:
                    print('here is the error that was thrown')
                    raise FileParseError(file, file_path, '}', line_num, "was never opened")
                case '}' if has_open_paren:
                    if category is None:
                        print(f"Warning: line {open_paren_line_number + 1} to line {line_num - 1}, Category is None")
                    else:
                        print("Category:", category)
                    if any(data_sites):
                        sites_data.append_sites(category, data_sites)
                    inside_braces, has_open_paren = False, False
                case other if inside_braces:
                    match other.count(","):
                        case 2:
                            title, nickname, url = other.split(',')
                            data_sites.append((title.strip(), nickname.strip(), url.strip()))
                        case 1:
                            title, url = other.split(',')
                            data_sites.append((title.strip(), None, url.strip()))
                        case 0:
                            msg = f"has zero commas, minimum of 1, in Category: {category}"
                            raise FileParseError(file, file_path, other, line_num, msg)
                        case _:
                            msg = f"has too many commas, maximum of 2, in Category: {category}"
                            raise FileParseError(file, file_path, other, line_num, msg)

                    if has_internet_connection and not valid_url(url):
                        raise FileParseError(file, file_path, url, line_num, "is not a valid url")

                case other:
                    print(f"Please remove the unused text '{other}' on line {line_num} in {file}")
        sites_data.display_sites()
        return sites_data


def get_command():
    return shlex.split(input(">>>"))


@dataclass
class Command:
    """Class that represents a command."""
    command: str
    arguments: List[str]


def run_command(command: Command):
    match command:
        case _:
            print(f"Unknown command: {command!r}")


def main(*args, **kwargs):
    print('Open Default 2.0.0 (tags//v3.10.0:b494f59, Oct 5 2021, 20:27:44 -0400)')
    print('Type "help" or "copyright" for more information.')
    # open many different types of websites
    # call websites by number, name, or nickname

    while True:
        command, *arguments = get_command()
        run_command(Command(command, arguments))


if __name__ == '__main__':
    parse_sites_file(SOURCE)
    #
    os.system('cls')
