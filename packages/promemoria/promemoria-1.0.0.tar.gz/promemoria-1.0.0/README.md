![GitHub](https://img.shields.io/github/license/diantonioandrea/promemoria)

![PyPI](https://img.shields.io/pypi/v/promemoria?label=promemoria%20on%20pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/promemoria)
![PyPI - Downloads](https://img.shields.io/pypi/dm/promemoria)

![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/diantonioandrea/promemoria)
![GitHub last commit](https://img.shields.io/github/last-commit/diantonioandrea/promemoria)
![GitHub Release Date](https://img.shields.io/github/release-date/diantonioandrea/promemoria)

![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/diantonioandrea/promemoria/latest)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# [promemoria]

Intuitive Python based tool to create reminders in the shell.

**promemoria** is a Python based tool to help you stay organized and on top of your tasks! Quickly *create reminders in the shell* with the ability to *set a title, description, priority and date* to make sure you never forget anything.

## Installation

**promemoria** can be installed from [PyPI](https://pypi.org) by:

```
python3 -m pip install --upgrade promemoria
```

## Usage

### Show the list of reminders

By simply calling `promemoria`[^1] you'll have:

[^1]: Shouldn't this work, you can call **promemoria** by `python3 -m promemoria`.

```
[promemoria]

You have 1 reminder(s).
-----------------------

◯ [1] New reminder !!
      Empty reminder for test purposes.
      Due: 2023-07-10

------------
0 completed.
```

### Create a new reminder

The command for creating a new reminder is the following:

```
promemoria new -t "TITLE" -de "DESCRIPTION" -da "DATE" -p PRIORITY
```

and an example would be:

```
promemoria new -t "Christmas" -de "It's Christmas!" -da "2023-12-25" -p 3
```

which would result in

```
[promemoria]

Reminder created succesfully!

◯ Christmas !!!
  It's Christmas!
  Due: 2023-12-25
```

### Delete every reminder

By

```
promemoria clear
```

you'll delete every reminder.

```
[promemoria]

Your reminders have been deleted.
```

### Delete a specific reminder

By 

```
promemoria delete -i INDEX
```

you'll be able to delete the i-th reminder in your list.

### Toggle a reminder

By 

```
promemoria toggle -i INDEX
```

you'll be able to toggle the i-th reminder in your list.

By calling `promemoria toggle -i 1` on the *Christmas* reminder created before:

```
[promemoria]

● ̶C̶h̶r̶i̶s̶t̶m̶a̶s !!!
  It's Christmas!
  Due: 2023-12-25
```

the reminder gets toggled and its title gets striked.