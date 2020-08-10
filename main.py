import webbrowser

source = "sites.txt"


class Dbtype:
    types = []

    def __init__(self, name, desc, sites):
        Dbtype.types.append(self)
        self.name = name
        self.desc = desc
        self.sites = sites

    @classmethod
    def get_all_of_type(cls, type_name=None):
        if type_name is None:
            return [n for n in cls.types]

    @classmethod
    def get_sites_by_type(cls, type_name=None):
        if type_name is None:
            return [n.sites for n in cls.types]

    @classmethod
    def get_desc_by_type(cls, type_name=None):
        if type_name is None:
            return [n.desc for n in cls.types]

    @classmethod
    def get_sites_by_name(cls, name):
        for i in Dbtype.types:
            if i.name == name:
                return i.sites
        else:
            return -1

    @classmethod
    def get_all_sites(cls):
        for obj in cls.types:
            print(obj.name)
            print(obj.desc)
            print(obj.sites)

    def __repr__(self):
        return f'Type: {self.name}, Description: {self.desc} \nSites: {self.sites}'


class FileParseError(Exception):
    def __init__(self, line, line_num, message="The file was unable to load because it was not formatted correctly"):
        if line[-1:] == '\n':
            self.line = line[:-1]
        else:
            self.line = line
        self.line_num = line_num
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} on line {self.line_num}: '{self.line}'"


def setup(file):
    type_obj = []

    with open(file) as f:
        for line_num, line in enumerate(f.readlines()):
            if line == '\n':
                continue
            elif '{' in line:
                about = []
                link = []
                title = line[0:-2]

            elif '}' in line:
                type_obj.append(Dbtype(title, about, link))
            elif ',' in line:

                line = line.split(',')
                about.append(line[0])
                link.append(line[1])
            else:
                raise FileParseError(line, line_num + 1)

    # for i in type_obj:
    #     print(i)
    # Dbtype.get_all_sites()
    return type_obj


def call_all(all_sites):
    print('Opening all...')
    if isinstance(all_sites[0], list):

        for sites in all_sites:
            for site in sites:
                webbrowser.open(site)
    elif isinstance(all_sites[0], int):
        for site in all_sites:
            webbrowser.open(site)
    else:
        print("I don't understand the question.")


def call_some(num, sites):
    # TODO print actual name of what is being opened
    print(f"Opening {num}...")
    for site in num:
        webbrowser.open(sites[site])


def call_some_none(num, sites):
    print(f"Opening {[sites[i][0] for i in num]}...")
    for site in num:
        webbrowser.open(sites[site][1])

def site_help(desc, sites):
    for num, _site in enumerate(zip(desc, sites)):
        print(f"\t{num}: {_site}")


def is_empty(arg):
    for a in arg:
        if a.isspace():
            pass
        else:
            return False
    return True


def data_in_range(nums, data):
    for i in nums:
        if int(i) >= len(data):
            return False

    return True


def validate_data(nums, data):
    if data == -1 or nums.startswith(','):
        return -1
    # Data is Num/convert to cleaned num str
    new = []
    for i in nums.split(','):
        next_char = ''
        for j in i:
            if j.isspace():
                continue
            elif not j.isnumeric():
                return -1
            else:
                next_char += j
        else:
            new.append(next_char)

    # check if cleaned data is in range
    if data_in_range(new, data):
        return [int(str_arg) for str_arg in new]
    return -1


def call_error(arg, msg=None, pre_msg=None):
    msg = 'is not a internal or external command,\noperable program or batch file.' if msg is None else msg
    pre_msg = '' if pre_msg is None else pre_msg
    print(f"{pre_msg}'{arg}' {msg}")


def parse_type_call(args):
    # chck if arg for type is valid (from DBtype class)
    if len(args) >= 4:
        if args == 'type':
            return True

        if args.startswith('type'):
            args = args.split(' ')
            return args[1:]


def parse_help_call(args):
    # chck if arg for type is valid (from DBtype class)
    if args == 'help':
        return 'help'
    if len(args) >= 4:
        if args.startswith('help'):
            args = args.split(' ')
            args = args[1:]
            return args


def none_type_open(objs):
    num = 0
    sites_li = []
    for n, i in enumerate(objs):
        # print("Type:", i.name)
        for _, s in enumerate(zip(i.desc, i.sites)):
            sites_li.append(s)
            # print('\t', num, ' , '.join(s))
            num += 1
    return sites_li



# add functionality to search some sites
# have help and all, take args for type and other things

def main_loop(objs):
    run = True
    prompt = ">>>"
    curr_type = None
    while run:

        arg = input(prompt).lower()

        if is_empty(arg):
            continue
        if arg == 'restart':
            print('-' * 20, 'RESTART', '-' * 20)
        if arg == 'types':
            print('All available types:')
            print('\t', ', '.join(i.name for i in Dbtype.types))
            continue
        if type_call := parse_help_call(arg):
            if 'all' in type_call:
                print('opens all of the specified type')
                continue
            elif 'copyright' in type_call:
                print('Prints the copyright')
                continue
            elif 'help' in type_call and type(type_call) == list:
                print("Calling help 'thing' prints help for the object 'thing'.")
                continue
            elif 'restart' in type_call:
                print("Prints a long line.")
                continue
            elif 'quit' in type_call:
                print("Exits the program.")
                continue
            elif 'type' in type_call:
                print('type in name of the catagory you want to switch to.')
                print("If you want to go back to no type enter 'type none'")
                continue

            elif 'types' in type_call:
                print('Shows all available types')
                continue
            if curr_type is None:
                num = 0
                for n, i in enumerate(objs):
                    print("Type:", i.name)
                    for _, s in enumerate(zip(i.desc, i.sites)):
                        print('\t', num, ', '.join(s))
                        num += 1
            else:
                for n, i in enumerate(objs):
                    if i.name == curr_type:
                        print("Type:", i.name)
                        for num, s in enumerate(zip(i.desc, i.sites)):
                            print('\t', num, ', '.join(s))
            print('all\t\t   Opens all links')
            print('copyright\t   Prints the copyright')
            print('help\t\t   Gives info based on current context')
            print('restart\t\t   Restarts the program and reloads from the file')
            print('type\t\t   Changes current type name')
            print('types\t\t   Shows all available types')
            print('quit\t\t   Exits the program')

            print()
            continue
        elif arg == 'all':
            print(Dbtype.get_sites_by_type())
            call_all(Dbtype.get_sites_by_type())
            continue
        elif type_call := parse_type_call(arg):
            # validate

            if type_call is True:
                print('Builtin type function\ntype "help type" for more')
                continue
            curr_type = type_call[0]
            if curr_type == 'none':
                curr_type = None
                prompt = ">>>"

            else:
                prompt = f"({curr_type}) >>>"
            continue
        elif arg == 'copyright':
            print('Copyright (c)', 2020, 'Ryan Farish Software Foundation.')
            print('All Rights Reserved.')
            continue
        elif arg == 'quit':
            quit()
        # can use code as a kwarg for quit to have a exit code and a red error msg

        elif (open_sites := validate_data(arg, (site_li := none_type_open(objs)))) and curr_type is None:
            if open_sites == -1:
                call_error(arg, ' was not given in the correct syntax or the correct range ', "The command ")
            else:
                call_some_none(open_sites, site_li)
            continue
        # clean and check data
        elif open_sites := validate_data(arg, Dbtype.get_sites_by_name(curr_type)):
            if open_sites == -1:
                call_error(arg, ' was not given in the correct syntax or the correct range ', "The command ")

            else:
                call_some(open_sites, Dbtype.get_sites_by_name(curr_type))

        else:
            call_error(arg)

    input()


if __name__ == '__main__':
    print('Open Default 1.5.2 (tags/v2.1:6f8c832, Jul 27 2020, 20:27:44 -0400)')
    print('Type "help" or "copyright" for more information.')
    obj = setup(source)
    main_loop(obj)
