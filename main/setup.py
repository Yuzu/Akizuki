# Imports dependencies
import tkinter as tk
# from tkinter import ttk <-- Not used, but might be in the future.
from tkinter import simpledialog
from tkinter import messagebox

import sys
import datetime
import os
import json

class Setup(object):
    """Will walk the user through the setup, asking them for various inputs to get the bot ready to start running."""

    def __init__(self, bot_token, bot_prefix):

        self.window = tk.Tk()
        self.window.withdraw()  # Hides root menu to make it look cleaner.
        self.bot_token = bot_token
        self.bot_prefix = bot_prefix
        self.confirmquestion = ""
        self.userconfirmation = ""
        self.installDependenciesStatus = False
        self.ownerid = ""
        self.wows_api_key = ""

        self.now = datetime.datetime.now()

    def askuser(self):
        """Asks user for their token and prefix."""

        self.bot_token = simpledialog.askstring(
            "Input", "What is the bot token?", parent=self.window)

        if self.bot_token is None:
            messagebox.showerror("Error", "Setup has been cancelled.")
            sys.exit()

        self.bot_prefix = simpledialog.askstring(
            "Input", "What will the bot's prefix be?", parent=self.window)

        if self.bot_prefix is None:
            messagebox.showerror("Error", "Setup has been cancelled.")
            sys.exit()

        self.ownerid = simpledialog.askstring("Input", "What is the bot owner's ID? This is very important!", parent=self.window)

        if self.ownerid is None:
            messagebox.showerror("Error", "Setup has been cancelled.")
            sys.exit()

        self.wows_api_key = simpledialog.askstring("Input", "This part is optional: What is the WOWS API key?", parent=self.window)

        if self.wows_api_key is None:
            messagebox.showerror("Error", "Setup has been cancelled.")
            sys.exit()

    def validitycheck(self):
        """Checks the user's inputs against various conditions that would be problematic for the bot."""

        # Looks for empty inputs and prefixes of purely spaces
        if self.bot_token != "" and self.bot_prefix != "" and not self.bot_prefix.isspace() and self.ownerid != "":
            print("Valid input.")  # Just printing to the console.

        elif self.bot_token == "" or self.bot_prefix == "" or self.bot_prefix.isspace() or self.ownerid == "":
            messagebox.showerror(
                "Warning", "One of your inputs is invalid. The program will run again.")
            main()

    def confirmation(self):
        """Confirms the user's inputs with them."""

        self.userconfirmation = messagebox.askyesno("Confirmation", "So your bot token is: \n{0} \nand your bot prefix is: \n{1} \nand your owner ID is: \n{2} \nand your WOWS API Key is: \n{3}".format(self.bot_token, self.bot_prefix, self.ownerid, self.wows_api_key))

        if self.userconfirmation is True:
            messagebox.showinfo("Information", "Okay, your bot token, prefix, and owner ID and WOWS API Key have been set.")

        elif self.userconfirmation is False:
            messagebox.showinfo("Information", "Okay, running the program again.")
            main()

    def configassign(self):
        """Writes the user's inputs to a text file to store them for the bot."""

        data = {"Bot Token": self.bot_token, "Bot Prefix": self.bot_prefix, "Owner ID": self.ownerid, "WOWS API Key": self.wows_api_key}

        with open("config.json", "w") as my_file:
            json.dump(data, my_file, indent=2)

    def configlogging(self):
        """Will append new changes to log them."""

        with open("confighistory.txt", "w") as my_file:

            my_file.write("Date of update:" + str(self.now) + "\n")
            my_file.write("Bot Token: " + self.bot_token + "\n")
            my_file.write("Bot Prefix: " + self.bot_prefix + "\n")
            my_file.write("Owner ID: " + self.ownerid + "\n")
            my_file.write("WOWS API Key: " + self.wows_api_key + "\n")
            my_file.write("\n")

    def installdependencies(self):
        """Installs dependencies if needed."""

        self.installDependenciesStatus = messagebox.askyesno("Install?", "Would you like to install bot dependencies?")

        if self.installDependenciesStatus is True:
            os.system("pip install -Ur requirements.txt")

        else:
            messagebox.showinfo("Information", "Okay. Exiting setup. You can manually run the dependencies.py file in the main folder if you would like to install it without going through this again.")
            return


def main():
    bot_token = ""
    bot_prefix = ""

    setup_instance = Setup(bot_token, bot_prefix)

    setup_instance.askuser()

    setup_instance.validitycheck()

    setup_instance.confirmation()

    setup_instance.configassign()

    setup_instance.configlogging()

    setup_instance.installdependencies()


if __name__ == "__main__":
    main()
