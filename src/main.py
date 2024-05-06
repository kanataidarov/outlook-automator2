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
        process(oa, command)


def process(oa, command):
    cmdName = command[:command.index("/")].strip()
    cmdVal = command[command.index("/") + 1:].strip()
    if cmdName == "select":
        print('\n'.join(mail.subject + " / " + str(mail.datetime_received) for mail in oa.select_mails(cmdVal)))
    elif cmdName == "bulk_del":
        oa.bulk_delete(cmdVal)
    elif cmdName == "remind":
        oa.create_reminder(cmdVal)
    else:
        oa.create_reminder(command)


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # fixes unknown bug with debugging
    main()
