import pickle
import sys

from colorama import Fore, Style, init

from .help import help
from .files import getReminders, saveReminders
from .reminders import reminder
from .utilities import parser

# Colorama's initialization.
init()


# Defines promemoria's main function.
# This makes possible calling promemoria as a script.
def main() -> None:
    # Obtains instructions and options.
    instructions, sdOpts, ddOpts = parser(sys.argv)
    index: int = -1

    # Gets reminders.
    reminders: list[reminder] = getReminders()

    # Get reminder index, if present.
    if "i" in sdOpts:
        try:
            assert isinstance(sdOpts["i"], int)
            assert 0 < sdOpts["i"] <= len(reminders)

            index = sdOpts["i"] - 1

        except AssertionError:
            pass

    # Application name.
    print(Style.BRIGHT + "[promemoria]" + Style.RESET_ALL + "\n")

    # Helper.
    if "help" in instructions:
        print(help())

    # Creates a new reminder.
    elif "new" in instructions:
        newReminder = reminder(sys.argv)

        if newReminder.confirmation:
            reminders.append(newReminder)

            print("\n" + str(newReminder))

    # Delete all reminders.
    elif "clear" in instructions:
        reminders = []

        print("Your reminders have been deleted.")

    # Delete a reminder.
    elif "delete" in instructions:
        if index < 0:
            print(Fore.RED + "Syntax error." + Style.RESET_ALL)
            return -1

        message = "You have deleted a reminder."

        print(message)
        print("-" * len(message))

        print("\n" + str(reminders.pop(index)))

    # Toggle a reminder.
    elif "toggle" in instructions:
        if index < 0:
            print(Fore.RED + "Syntax error." + Style.RESET_ALL)
            return -1

        message = "You toggled a reminder."

        print(message)
        print("-" * len(message))

        reminders[index].toggle()
        print("\n" + str(reminders[index]))

    # No reminders.
    elif not len(reminders):
        hint = Style.BRIGHT + "promemoria new -t 'TITLE' ..." + Style.RESET_ALL

        print("You have no reminders.")
        print("Try creating one using " + hint)

    # Shows reminders by default.
    else:
        # Get printable reminders.
        if "all" not in ddOpts:
            printable = [rem for rem in reminders if not rem.dismissed]

        else:
            printable = reminders.copy()

        # Print reminders, if any.
        if len(printable):
            message: str = "You have {} reminder(s).".format(len(printable))

            print(message)
            print("-" * len(message))

            # Prints the list of reminders.
            for rem in printable:
                pIndex = reminders.index(rem)
                print("\n" + rem.__str__(pIndex + 1))

        else:
            print("Nothing to show.")

        if "all" in ddOpts:
            # Prints the number of completed reminders.
            completed: int = [rem.dismissed for rem in reminders].count(True)
            message: str = "{} completed.".format(completed)

            print("\n" + "-" * len(message))
            print(message)

    # Saves reminders.
    saveReminders(reminders)
