from src.const import const
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from exchangelib import Account, Credentials, Configuration, DELEGATE, Message, EWSDateTime
from exchangelib.items import Task
from loguru import logger as log

import json
import re
import zoneinfo


class OutlookAutomator:
    """TODO: Docstring for OutlookAutomator.
    """

    def __init__(self, args):
        self.args = args
        self.account = self.__authenticate()
        self.tz = zoneinfo.ZoneInfo("Asia/Aqtobe")

    def __authenticate(self):
        credentials = Credentials(self.args["email"], self.args["paswd"])

        config = Configuration(
            service_endpoint=self.args["ews_url"],
            credentials=credentials,
            auth_type=self.args["auth_type"],
        )

        account = Account(
            primary_smtp_address=self.args["email"],
            config=config,
            access_type=DELEGATE,
        )

        return account

    def acc_root(self):
        return self.account.root

    def select_mails(self, command):
        invalid_input = (f"Invalid input: `{command}` should contain folder name, search string"
                         f" and number of messages to retrieve")
        lines = self.__validate_command(command, 3, invalid_input)
        folder_name = lines[0].strip()
        folder = self.acc_root() / self.args["outlook_root"] / folder_name
        filter_str = str(lines[1].strip())
        last_n = int(lines[2].strip())

        messages = [item for item in self.__apply_filter(folder, filter_str)[:last_n]]

        log.info(f"Selected {len(messages)} messages in folder `{folder_name}`")

        return messages

    @staticmethod
    def mark_read(messages):
        for idx, item in enumerate(messages):
            if isinstance(item, Message):
                item.is_read = True
                item.save()
                log.info(f"Marked message {idx} - `{item.subject}` as read")
        log.success(f"Marked {len(messages)} messages as read")

    @staticmethod
    def delete(messages):
        count = 0
        for item in messages:
            if isinstance(item, Message) and item.is_read:
                item.delete()
                count += 1
                log.info(f"Deleted message {count} - `{item.subject}`")
        log.success(f"Deleted {count} already read messages")

    def bulk_delete(self, command):
        invalid_input = f"Invalid input: `{command}` should contain folder name and search string"
        lines = self.__validate_command(command, 2, invalid_input)
        folder_name = lines[0].strip()
        folder = self.acc_root() / self.args["outlook_root"] / folder_name

        count = 0
        for i in range(1, len(lines)):
            filter_str = str(lines[i].strip())
            count += len(self.__apply_filter(folder, filter_str).delete(page_size=9999, chunk_size=999))

        log.success(f"Deleted {count} messages in folder `{folder_name}`")

        return count

    def folders(self):
        root = self.acc_root() / self.args["outlook_root"]
        folders = []
        for folder in root.walk():
            folders.append(folder.name)
        log.debug(f"Folders: {folders}")
        return folders

    def create_reminder(self, command):
        invalid_input = f"Invalid input: `{command}` should contain at least time and subject"
        lines = self.__validate_command(command, 2, invalid_input)

        dt = lines[0].strip()
        if len(dt) == 1 and dt.isdigit():
            existing_tasks = json.loads(self.args["existing_tasks"])
            existing_task = next(task for task in existing_tasks if task["alias"] == dt)

            task = self.account.tasks.filter(subject=existing_task["subject"])[0]
            body = self.__extract_body_text(task.body)
            task.body = self.__add_lines_to_body(body, lines[1:])

            task.reminder_due_by = self.__create_dt(existing_task["dt"])
        elif len(dt) == 2 and not dt.isdigit():
            existing_tasks = json.loads(self.args["existing_tasks"])
            existing_task = next(task for task in existing_tasks if task["alias"] == dt[1])

            task = self.account.tasks.filter(subject=existing_task["subject"])[0]
            body = self.__extract_body_text(task.body)
            task.body = self.__add_lines_to_body(body, lines[1:])

            task.reminder_due_by = self.__create_dt(dt[0] + existing_task["dt"])
        else:
            task = Task(folder=self.account.tasks)
            self.__create_subject(task, lines[1:])

            task.reminder_due_by = self.__create_dt(dt)

        task.reminder_is_set = True
        task.save()

        log.success(f"Updated reminder for task `{task.subject}`")

    @staticmethod
    def __create_subject(task, lines):
        task.subject = lines[0].strip()
        if len(lines) > 1:
            task.body = '\n'.join(lines[1:])

    def __create_dt(self, dt):
        """Parses a time string like "n10:33" into variables and creates datetime object.

            Args:
                dt (str): Date and time string to parse.

            Returns:
                datetime containing parts of parsed dt string.
        """
        day = datetime.now() + timedelta(days=1)
        print(dt)
        if not dt[0].isdigit():
            if dt[0] not in {'n', 't', 'a'}:
                raise ValueError("Time prefix should be one of the following: n, t, a")
            elif dt[0] == 'a':
                day += timedelta(days=1)
            elif dt[0] == 'n':
                day -= timedelta(days=1)

            dt = dt[1:]

        try:
            hour, minute = map(int, dt.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError(f"Invalid time format: {dt}")
        except ValueError as e:
            raise ValueError(f"Invalid time format: {dt}") from e

        return datetime(year=day.year, month=day.month, day=day.day, hour=hour, minute=minute, tzinfo=self.tz)

    @staticmethod
    def __add_lines_to_body(text, lines):
        """
        Inserts provided lines into the body of the Task.

        Args:
            text: body property of the Task object.
            lines: Lines to insert into the body.

        Returns:
            Modified body string with lines inserted.
        """
        if len(lines) >= 1:
            new_text = '\n' + '\n'.join([line.strip() for line in lines])
            text += new_text

        return text

    @staticmethod
    def __extract_body_text(html):
        """
        Extracts the text content from the body of an HTML file.

        Args:
            html: The HTML file to extract text data from.

        Returns:
            The text content of the body.
        """
        if not html:
            return ""
        if not ('<' in html and '>' in html):
            return html

        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body")
        if body:
            text = body.get_text(separator='\n').strip()
            return re.sub(r"\n{2,}", '\n', text)
        else:
            return ""

    @staticmethod
    def __validate_command(command, no_lines, err_msg):
        if not command:
            raise ValueError(err_msg)

        lines = command.split(const.TASK_SUBJECT_SPLITTER)
        if len(lines) < no_lines:
            raise ValueError(err_msg)

        return lines

    def __apply_filter(self, folder, filter_str):
        if filter_str.lower().startswith("upto:"):
            return folder.filter(datetime_received__lt=self.__extract_dt(filter_str))
        else:
            return folder.filter(filter_str)

    def __extract_dt(self, filter_str):
        dt = datetime.strptime(filter_str.lower().removeprefix("upto:"), "%Y-%m-%d")
        return EWSDateTime(dt.year, dt.month, dt.day, 0, 0, tzinfo=self.tz)
