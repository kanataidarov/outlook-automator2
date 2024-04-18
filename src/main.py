import os
import sys

from src.config.args_parser import ArgsParser
from src.handler.outlook_automator import OutlookAutomator


def main():
    args = ArgsParser.parse_args()
    oa = OutlookAutomator(args)

    command = args["command"]
    if not command:
        command = input()

    if args["debug"]:
        debug_mode(oa, command)
    else:
        oa.create_reminder(command)


def debug_mode(oa, command):
    selected_mails = oa.select_mails(command)

    oa.mark_read(selected_mails)
    oa.delete(selected_mails)


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # fixes unknown bug with debugging
    main()
