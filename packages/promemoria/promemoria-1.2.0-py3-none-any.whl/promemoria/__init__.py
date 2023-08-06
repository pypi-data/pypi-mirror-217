import sys

from colorama import Fore, Style, init

from .help import help
from .files import getReminders, saveReminders
from .reminders import reminder
from .utilities import parser, msg
from .git import gitContents

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

    # GitHub integration.
    elif "gh" in instructions:
        status, gits = gitContents(sys.argv)

        if status:
            titles = [rem.title for rem in reminders]

            # Try to avoid duplicates.
            gits = [git for git in gits if git.title not in titles]

            reminders += gits

            string: str = "Imported {} {}(s)."
            string = string.format(len(gits), "{}")
            string = string.format("issue" if "pulls" not in ddOpts else "pull")
            msg(string)

            for git in gits:
                print("\n" + str(git))

        else:
            msg("An error occurred during import.", error=True)

    # Delete all reminders.
    elif "clear" in instructions:
        reminders = []

        print("Your reminders have been deleted.")

    # Delete a reminder.
    elif "delete" in instructions:
        if index < 0:
            msg("Missing reminder index.", error=True)
            return -1

        msg("You have deleted a reminder.")
        print("\n" + str(reminders.pop(index)))

    # Toggle a reminder.
    elif "toggle" in instructions:
        if index < 0:
            msg("Missing reminder index.", error=True)
            return -1

        msg("You toggled a reminder.")
        reminders[index].toggle()
        print("\n" + str(reminders[index]))

    # No reminders.
    elif not len(reminders):
        hintNew = Style.BRIGHT + "promemoria new -t 'TITLE' ..." + Style.RESET_ALL
        hintGit = Style.BRIGHT + "promemoria gh -r 'USER/REPO' ..." + Style.RESET_ALL

        print("You have no reminders.\n")
        print("Try creating one using " + hintNew)
        print("or import some using " + hintGit)

    # Shows reminders by default.
    else:
        # Get printable reminders.
        if "all" not in ddOpts:
            printable = [rem for rem in reminders if not rem.dismissed]

        else:
            printable = reminders.copy()

        # Print reminders, if any.
        if len(printable):
            msg("You have {} reminder(s).".format(len(printable)))

            # Prints the list of reminders.
            for rem in printable:
                pIndex = reminders.index(rem)
                print("\n" + rem.__str__(pIndex + 1))

        else:
            msg("Nothing to show.")

        if "all" in ddOpts:
            # Prints the number of completed reminders.
            completed: int = [rem.dismissed for rem in reminders].count(True)

            print()  # Needed space.
            message = "{}/{} completed."
            message = message.format(completed, len(reminders))
            msg(message, reversed=True)

    # Saves reminders.
    saveReminders(reminders)
