import pickle
import sys
from os import makedirs
from os.path import expanduser

from colorama import Style, init

from .promemoria import reminder
from .utilities import parser

# Colorama's initialization.
init()


# Defines promemoria's main function.
# This makes possible calling promemoria as a script.
def main() -> None:
    # Creates or checks reminders' folder.
    path = expanduser("~") + "/.promemoria/"
    makedirs(path, exist_ok=True)

    # Loads reminders.
    try:
        file = open(path + "reminders.pickle", "rb")

        reminders: list[reminder] = pickle.load(file)
        file.close()

        for rem in reminders:
            if not isinstance(rem, reminder):
                # Raises this error to recreate the file.
                raise FileNotFoundError

    except FileNotFoundError:
        reminders: list[reminder] = []

        file = open(path + "reminders.pickle", "wb")
        pickle.dump(reminders, file)
        file.close()

    # Obtains instructions and options.
    instructions, sdOpts, _ = parser(sys.argv)
    index: int = -1

    if "i" in sdOpts:
        try:
            assert isinstance(sdOpts["i"], int)
            assert 0 < sdOpts["i"] <= len(reminders)

            index = sdOpts["i"] - 1

        except AssertionError:
            pass

    # Application name.
    print(Style.BRIGHT + "[promemoria]" + Style.RESET_ALL + "\n")

    # Get some help.
    if "help" in instructions:
        print("List of available commands.")

        print("\nnew: create a new reminder.")
        print("\t-t 'TITLE' [String]")
        print("\t-de 'DESCRIPTION' [String]")
        print("\t-da 'DATE' [String]")
        print("\t-p PRIORITY [Integer, 1-3]")

        print("\nclear: delete every reminder.")

        print("\ndelete: delete a reminder.")
        print("\t-i INDEX [Integer]")

        print("\ntoggle: toggle a reminder.")
        print("\t-i INDEX [Integer]")

    # New reminder.
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
    elif "delete" in instructions and index >= 0:
        message = "You have deleted a reminder."

        print(message)
        print("-" * len(message))

        print("\n" + str(reminders.pop(index)))

    # Toggle a reminder.
    elif "toggle" in instructions and index >= 0:
        reminders[index].toggle()
        print(reminders[index])

    # Shows reminders by default.
    elif not len(reminders):
        help = Style.BRIGHT + "promemoria new -t 'TITLE' ..." + Style.RESET_ALL

        print("You have no reminders.")
        print("Try creating one using " + help)

    else:
        message: str = "You have {} reminder(s).".format(len(reminders))

        print(message)
        print("-" * len(message))

        for j in range(len(reminders)):
            print("\n" + reminders[j].__str__(j + 1))

        completed: int = [rem.dismissed for rem in reminders].count(True)
        message: str = "{} completed.".format(completed)

        print("\n" + "-" * len(message))
        print(message)

    # Saves reminders.
    file = open(path + "reminders.pickle", "wb")
    pickle.dump(reminders, file)
    file.close()
