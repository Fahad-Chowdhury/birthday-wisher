import datetime as dt
import os
import random
import smtplib
import pandas
import config


class BirthdayWisher():

    def __init__(self):
        self.data = None
        self.birthday_msg = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def _generate_birthday_letter(self, name):
        """ Generate a birthday letter by selecting a file in 'letters' variable in config file,
        reading the file and setting birthday letter by replacing [NAME] with given name. """
        letter = random.choice(config.letters)
        letter_file_path = os.path.join(self.current_dir, "letter_templates", letter)
        with open(letter_file_path, "r") as file:
            msg = file.read()
            self.birthday_msg = msg.replace('[NAME]', name)

    def _send_birthday_email(self, name, email):
        """ Send an e-mail with generated birthday letter to the person with given name and email. """
        print(f"Sending Birthday Wish to {name} (e-mail: {email}.)")
        self._generate_birthday_letter(name)
        with smtplib.SMTP(config.SMTP_SERVER, port=config.SMTP_PORT) as connection:
            connection.starttls()
            connection.login(user=config.SENDER, password=config.PASSWORD)
            email_msg = f"Subject:Happy Birthday!\n\n{self.birthday_msg}"
            connection.sendmail(from_addr=config.SENDER, to_addrs=email, msg=email_msg)

    def send_birthday_wishes(self):
        """ Read birthday data from 'birthdays.csv' file, and if today is a person's birthday,
        then send an e-mail with birthday wishes. """
        data_file_path = os.path.join(self.current_dir, "birthdays.csv")
        self.data = pandas.read_csv(data_file_path)
        now = dt.datetime.now()
        for (_, row) in self.data.iterrows():
            if now.day == row["day"] and now.month == row["month"]:
                self._send_birthday_email(row["name"], row["email"])


def main():
    """ Main method to send birthday wishes. """
    wisher = BirthdayWisher()
    wisher.send_birthday_wishes()


if __name__ == "__main__":
    main()
