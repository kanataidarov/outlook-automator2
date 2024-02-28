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

OUTLOOK_ROOT = "Корневой уровень хранилища"
