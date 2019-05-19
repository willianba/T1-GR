from settings import font


def only_numbers(char):
    return char.isdigit()


def set_container_padding(container):
    container["padx"] = 20
    container["pady"] = 5


def set_entry_configuration(entry):
    set_entry_width(entry)
    set_entry_font(entry)


def set_entry_width(entry):
    entry["width"] = 25


def set_entry_font(entry):
    entry["font"] = font
