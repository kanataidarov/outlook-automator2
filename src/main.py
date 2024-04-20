import os
import sys

from src.config.args_parser import ArgsParser
from src.debug.debug import debug_mode
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


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # fixes unknown bug with debugging
    main()
