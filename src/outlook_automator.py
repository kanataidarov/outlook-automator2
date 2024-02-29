import json
import re
import zoneinfo
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from exchangelib import Credentials, Configuration, Account, DELEGATE
from exchangelib.items import Task

import const


class OutlookAutomator:
    """TODO: Docstring for OutlookAutomator.
    """

    def __init__(self, args):
        self.args = args
        self.account = self.__authenticate()
        self.tz = zoneinfo.ZoneInfo('Asia/Almaty')

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

    def select_mails(self, folder_name, last_n):
        folder = self.acc_root() / self.args["outlook_root"] / folder_name

        return [(item.subject, item.sender, item.datetime_received)
                for item in folder.all().order_by("-datetime_received")[:last_n]]

    def create_reminder(self, in_str):
        lines = in_str.split(const.TASK_SUBJECT_SPLITTER)
        if len(lines) < 2:
            raise ValueError(f"Invalid input: `{in_str}` should contain at least time and subject")

        dt = lines[0].strip()
        if len(dt) == 1 and dt.isdigit():
            existing_tasks = json.loads(self.args["existing_tasks"])
            existing_task = next(task for task in existing_tasks if task["alias"] == dt)

            task = self.account.tasks.filter(subject=existing_task["subject"])[0]
            body = self.__extract_body_text(task.body)
            task.body = self.__add_lines_to_body(body, lines[1:])

            task.reminder_due_by = self.__create_dt(existing_task["dt"])
        else:
            task = Task(folder=self.account.tasks)
            self.__create_subject(task, lines[1:])

            task.reminder_due_by = self.__create_dt(dt)

        task.reminder_is_set = True
        task.save()

    @staticmethod
    def __create_subject(task, lines):
        task.subject = lines[0].strip()
        if len(lines) > 1:
            task.body = "\n".join(lines[1:])

    def __create_dt(self, dt):
        """Parses a time string like "n10:33" into variables and creates datetime object.

            Args:
                dt (str): Date and time string to parse.

            Returns:
                datetime containing parts of parsed dt string.
        """
        day = datetime.now() + timedelta(days=1)
        if not dt[0].isdigit():
            if dt[0] not in {'n', 't', 'a'}:
                raise ValueError("Time prefix should be one of the following: n, t, a")
            elif dt[0] == 'a':
                day += timedelta(days=1)
            elif dt[0] == 'n':
                day -= timedelta(days=1)

            dt = dt[1:]

        try:
            hour, minute = map(int, dt.split(":"))
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
            new_text = "\n" + "\n".join([line.strip() for line in lines])
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
        if not ("<" in html and ">" in html):
            return html

        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        if body:
            text = body.get_text(separator='\n').strip()
            return re.sub(r"\n{2,}", "\n", text)
        else:
            return ""
