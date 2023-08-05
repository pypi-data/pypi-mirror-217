def strike(string: str) -> str:
    """
    Returns the strikethrough version of a string.
    """

    return "".join(["\u0336{}".format(c) for c in string])


def strToNum(string: str) -> "int, float, str":
    """
    Optionally converts a string to a number.
    """

    try:
        number = float(string)

        if number == int(number):
            return int(number)

        return number

    except ValueError:
        return string


def parser(prompt: list[str]) -> tuple[list[str], dict[str, str], list[str]]:
    """
    Prompt parser.
    """

    instructions: list[str] = []
    sdOpts: dict[str, str] = {}
    ddOpts: list[str] = []

    assert isinstance(prompt, list)

    # Single dash option skip flag.
    sdSkip: bool = False

    for j in range(len(prompt)):
        if sdSkip:
            sdSkip = False
            continue

        entry = prompt[j]
        assert isinstance(entry, str)

        # Double dash options.
        if len(entry) > 2:
            if entry[0] == entry[1] == "-":
                ddOpts.append(entry.replace("--", ""))

                continue

        # Single dash options.
        if len(entry) > 1:
            if entry[0] == "-":
                # Ignores negative numbers.
                try:
                    _ = float(entry)
                    continue

                except ValueError:
                    pass

                sdOpts[entry.replace("-", "", 1)] = strToNum(prompt[j + 1])
                sdSkip = True

                continue

        # Plain instructions.
        instructions.append(entry)

    if "debug" in ddOpts:
        print("instructions: " + ", ".join(instructions))
        print("sdOpts: " + ", ".join(sdOpts))
        print("ddOpts: " + ", ".join(ddOpts))

    return instructions, sdOpts, ddOpts
