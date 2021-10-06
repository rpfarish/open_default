class FileParseError(Exception):
    def __init__(self, file, file_path, line, line_num, message=None):
        if line.endswith('\n'):
            self.line = line[:-1]
        else:
            self.line = line
        self.file_path = file_path
        self.file = file
        self.line_num = line_num
        msg = "\nThe file was unable to load because it was not formatted correctly"
        self.message = message if message is not None else msg
        super(FileParseError, self).__init__(self.message)

    def __str__(self):
        msg = f"\n  File {self.file_path}, line {self.line_num}, in {self.file}" \
              f"\n{self.__class__.__name__}: '{self.line}' {self.message}"
        return msg
