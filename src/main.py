import os
import sys

from args_parser import ArgsParser
from outlook_automator import OutlookAutomator


def main():
    args = ArgsParser.parse_args()
    oa = OutlookAutomator(args)

    if args["debug"]:
        debug_mode(oa, args)
    else:
        pass


def debug_mode(oa, args):
    command = args["command"]
    if not command:
        command = input()
    oa.create_reminder(command)
    # folder_name = "RSS-подписки"
    # selected_mails = oaut.select_mails(folder_name, 9)
    # print(selected_mails)


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # fixes unknown bug with debugging
    main()
