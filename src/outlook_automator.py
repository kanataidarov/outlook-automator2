from exchangelib import Credentials, Configuration, Account, DELEGATE

import const


class OutlookAutomator:
    """TODO: Docstring for OutlookAutomator.
    """

    def __init__(self, args):
        self.args = args
        self.account = self.__authenticate()

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
        folder = self.acc_root() / const.OUTLOOK_ROOT / folder_name

        return [(item.subject, item.sender, item.datetime_received)
                for item in folder.all().order_by("-datetime_received")[:last_n]]
