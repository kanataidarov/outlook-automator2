class Positionals:
    EMAIL = {"name": "email", "help": "Email address of Exchange Account"}
    PASWD = {"name": "paswd", "help": "Password of Exchange Account"}
    DEBUG = {"name": "debug", "help": "Boolean value enabling other non-default functionality of given Project"}


class Optionals:
    AUTH_TYPE = {"name": "--auth_type",
                 "default": 'NTLM',
                 "help": "EWS Authentication type"}
    EWS_URL = {"name": "--ews_url",
               "default": 'https://outlook.office365.com/ews/exchange.asmx',
               "help": "URL of EWS"}
    OUTLOOK_ROOT = {"name": "--outlook_root",
                    "default": "Корневой уровень хранилища",
                    "help": "Outlook root directory"}
    EXISTING_TASKS = {"name": "--existing_tasks",
                    "default": '[{"alias": "1", "subject": "вопросы к team_1", "dt": "12:03"},'
                               '{"alias": "2", "subject": "вопросы к team_2", "dt": "09:33"},'
                               '{"alias": "3", "subject": "вопросы к team_3", "dt": "10:03"}]',
                    "help": "Existing task configurations to update"}


TASK_SUBJECT_SPLITTER = "/"
