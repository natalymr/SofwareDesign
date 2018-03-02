import io


class input_stream:

    def __init__(self, input=None):
        self.__io_str = io.StringIO()
        if input:
            self.__io_str.write(input)

    def get_input(self):
        return self.__io_str.getvalue()


class output_stream:

    def __init__(self):
        self.__io_str = io.StringIO()

    def write_to_stream(self, str):
        self.__io_str.write(str)

    def convert_to_input(self):
        return input_stream(self.__io_str.getvalue())
