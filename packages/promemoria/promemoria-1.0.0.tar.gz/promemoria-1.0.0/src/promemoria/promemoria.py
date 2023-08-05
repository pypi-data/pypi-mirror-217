from __future__ import annotations

from colorama import Fore, Style

from .utilities import strike, parser


class reminder:
    def __init__(self: reminder, prompt: list[str]):
        _, sdOpts, _ = parser(prompt)

        try:
            # Checks title.
            assert "t" in sdOpts
            self.title: str = sdOpts["t"]

            # Checks priority.
            if "p" in sdOpts:
                assert isinstance(sdOpts["p"], int)
                assert 1 <= sdOpts["p"] <= 3

                self.priority: int = sdOpts["p"]

            else:
                self.priority = 0

            # Checks description.
            if "de" in sdOpts:
                assert isinstance(sdOpts["de"], str)

                self.description: str = sdOpts["de"]

            else:
                self.description = ""

            # Checks date.
            if "da" in sdOpts:
                assert isinstance(sdOpts["da"], str)

                # To be formatted.
                self.date: str = sdOpts["da"]

            else:
                self.date = ""

            self.dismissed: bool = False
            self.confirmation: bool = True

            print("Reminder created succesfully!")

        except AssertionError:
            print("Reminder creation failed!\nCheck your prompt.")
            self.confirmation: bool = False

    def __str__(self: reminder, index: int = -1) -> str:
        # Mark.
        mark = "\u25cf " if self.dismissed else "\u25ef "

        if index != -1:
            mark += "[{}] ".format(index)

        # Lenght of 'mark' in spaces.
        spaces = len(mark) * " "

        # Title.
        # Striked on dismissed reminders.
        if self.dismissed:
            title = strike(self.title)

        else:
            title = Style.BRIGHT + self.title + Style.RESET_ALL

        string = mark + title

        # Priority.
        if self.priority:
            priority = " " + Fore.RED + "!" * self.priority + Fore.RESET

            string += priority

        # Description.
        if self.description:
            description = Style.DIM + self.description + Style.RESET_ALL

            string += "\n" + spaces + description

        # Date.
        if self.date:
            date = Fore.CYAN + self.date + Fore.RESET

            string += "\n" + spaces + "Due: " + date

        # Finally returns string.
        return string

    def toggle(self: reminder) -> None:
        """
        Toggles itself.
        """

        self.dismissed = not self.dismissed
