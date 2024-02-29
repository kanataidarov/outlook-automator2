from argparse import ArgumentParser
from const import Optionals, Positionals
from custom_argparse import CustomArgparseFormatter
from global_utils import to_bool


class ArgsParser:
    """Parses Command Line arguments and replaces optional ones with default settings.
    """

    @staticmethod
    def parse_args():
        arg_parser = ArgumentParser(description=description(), formatter_class=CustomArgparseFormatter)

        # positional arguments
        arg_parser.add_argument(Positionals.EMAIL["name"], help=Positionals.EMAIL["help"])
        arg_parser.add_argument(Positionals.PASWD["name"], help=Positionals.PASWD["help"])
        arg_parser.add_argument(Positionals.DEBUG["name"], help=Positionals.DEBUG["help"])

        # optional arguments
        arg_parser.add_argument(Optionals.EWS_URL["name"], default=Optionals.EWS_URL["default"],
                                type=str, help=Optionals.EWS_URL["help"])
        arg_parser.add_argument(Optionals.AUTH_TYPE["name"], default=Optionals.AUTH_TYPE["default"],
                                type=str, help=Optionals.AUTH_TYPE["help"])
        arg_parser.add_argument(Optionals.OUTLOOK_ROOT["name"], default=Optionals.OUTLOOK_ROOT["default"],
                                type=str, help=Optionals.OUTLOOK_ROOT["help"])
        arg_parser.add_argument(Optionals.EXISTING_TASKS["name"], default=Optionals.EXISTING_TASKS["default"],
                                type=str, help=Optionals.EXISTING_TASKS["help"])

        parsed_args = arg_parser.parse_args()

        args = {"email": parsed_args.email,
                "paswd": parsed_args.paswd,
                "debug": to_bool(parsed_args.debug),
                "ews_url": parsed_args.ews_url,
                "auth_type": parsed_args.auth_type,
                "outlook_root": parsed_args.outlook_root,
                "existing_tasks": parsed_args.existing_tasks}

        return args


def description():
    return "TODO: Description. \
        \n\nWritten by Kanat Aidarov (https://github.com/kanataidarov)"
