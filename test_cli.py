from unittest import TestCase, mock
from unittest.mock import mock_open, Mock, call

from IO_classes import output_stream
from cli import execute_command, pipe_execution


class TestExecuteCommand(TestCase):

    @mock.patch("sys.exit", return_value=None)
    def test_exit_command_calls_for_program_exit(self, exit_mock: Mock):
        execute_command(["exit"], 0, 1)

        exit_mock.assert_called()

    def test_echo_respects_separate_words(self):
        output = execute_command(["echo", "hello", "world"], 0, 3)

        self.assertEqual(stream_to_string(output), "hello world")

    def test_cat_opens_file_and_prints_it_to_output(self):
        output = execute_command(["cat", "helloworld.txt"], 0, 2)

        self.assertEqual(stream_to_string(output), "one two three")

    def test_cat_print_contents_of_passed_output_stream(self):
        prev_command_result = output_stream()
        prev_command_result.write_to_stream("hello world")

        output = execute_command(["cat"], 0, 1, prev_command_result)

        self.assertEqual(stream_to_string(output), "hello world")

    def test_execute_command_executes_only_selected_range(self):
        tokens = ["echo", "echo", "hello"]

        self.assertEqual(
            stream_to_string(execute_command(tokens, 0, 2)),
            "echo"
        )

        self.assertEqual(
            stream_to_string(execute_command(tokens, 0, 3)),
            "echo hello"
        )

        self.assertEqual(
            stream_to_string(execute_command(tokens, 1, 3)),
            "hello"
        )

    @mock.patch("os.getcwd", return_value="/urhere")
    def test_pwd_returns_cur_working_directory(self, pwd_mock : Mock):
        self.assertEqual(
            stream_to_string(execute_command(["pwd"], 0, 1)),
            "/urhere"
        )

        pwd_mock.assert_called_once()

    def test_wc_returns_correct_info_about_file(self):
        output = execute_command(["wc", "helloworld.txt"], 0, 2)

        self.assertEqual(
            stream_to_string(output),
            "1 3 13"
        )

    def test_wc_returns_correct_info_of_passed_output_stream(self):
        prev_command_result = output_stream()
        prev_command_result.write_to_stream("hello world")

        output = execute_command(["wc"], 0, 1, prev_command_result)

        self.assertEqual(
            stream_to_string(output),
            "1 2 11"
        )

    def test_dollar_sign_correct_reveal_and_expounds_vars(self):
        execute_command(["x=ho"], 0, 1)

        output = execute_command(["ec$x", "hello"], 0, 2)

        self.assertEqual(
            stream_to_string(output),
            "hello"
        )


def stream_to_string(stream: output_stream):
    return stream.convert_to_input().get_input()
