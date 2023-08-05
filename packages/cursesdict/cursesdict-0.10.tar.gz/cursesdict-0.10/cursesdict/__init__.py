import curses
import operator
import re
import sys
from functools import reduce
from threading import Thread
from time import sleep
from flatten_everything import flatten_everything

menu_config = sys.modules[__name__]
menu_config.menulen = 40
menu_config.add_spaces_right = 5
menu_config.add_spaces_left = 2
menu_config.menulen_highlighted = 40
menu_config.add_spaces_right_highlighted = 10
menu_config.add_spaces_left_highlighted = 4
menu_config.use_rjust = True
menu_config.refresh_sleep = 0.001
menu_config.quit_keys = [""]
menu_config.enter_keys = ["PADENTER"]
menu_config.key_up_keys = ["KEY_UP"]
menu_config.key_down_keys = ["KEY_DOWN"]
menu_config.menudict = {}


# https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses


def start_menu(
    menudict: dict,
    menu_len: int = 40,
    n_spaces_right: int = 5,
    n_spaces_left: int = 2,
    menu_len_selected: int = 40,
    n_spaces_right_selected: int = 10,
    n_spaces_left_selected: int = 4,
    rjust: bool = True,
    refresh_time: float = 0.001,
    quit_keys: tuple | list = ("",),
    enter_keys: tuple | list = ("PADENTER",),
    key_up_keys: tuple | list = ("KEY_UP",),
    key_down_keys: tuple | list = ("KEY_DOWN",),
) -> None:
    r"""
        Displays a menu using the curses library and allows the user to navigate and interact with the menu options.
        Download the Windows version of curses: https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses

        Args:
            menudict (dict): Dictionary containing the menu structure and options.
            menu_len (int, optional): Length of the menu items. Defaults to 40.
            n_spaces_right (int, optional): Number of spaces to add to the right of each menu item. Defaults to 5.
            n_spaces_left (int, optional): Number of spaces to add to the left of each menu item. Defaults to 2.
            menu_len_selected (int, optional): Length of the highlighted (selected) menu items. Defaults to 40.
            n_spaces_right_selected (int, optional): Number of spaces to add to the right of each highlighted menu item. Defaults to 10.
            n_spaces_left_selected (int, optional): Number of spaces to add to the left of each highlighted menu item. Defaults to 4.
            rjust (bool, optional): If True, right-justifies the menu items. If False, left-justifies the menu items. Defaults to True.
            refresh_time (float, optional): Refresh time for the menu display, in seconds. Defaults to 0.001.
            quit_keys (tuple or list, optional): Keys to quit the menu. Defaults to ("",).
            enter_keys (tuple or list, optional): Keys to select/enter a menu option. Defaults to ("PADENTER",).
            key_up_keys (tuple or list, optional): Keys to navigate up in the menu. Defaults to ("KEY_UP",).
            key_down_keys (tuple or list, optional): Keys to navigate down in the menu. Defaults to ("KEY_DOWN",).

        Returns:
            None

        Example:
    import subprocess
    from cursesdict import start_menu

    def fufu1(key):
        filetest = "c:\\testestestest.txt"
        with open(filetest, mode="w", encoding="utf-8") as f:
            f.write(str(key))
            f.write("\n")
        subprocess.Popen(f"notepad.exe {filetest}", shell=True)


    stama = {
        "main": {
            "menu_header": "Imaginary School - Main Menu",
            "option_0": {
                "Exercises": lambda: fufu1("Imaginary School - Main Menu - Exercises")
            },
            "option_1": {"Review": lambda: fufu1("Imaginary School - Main Menu - Review")},
            "option_2": {
                "Talk to a teacher": lambda: fufu1(
                    "Imaginary School - Main Menu - Talk to a teacher"
                )
            },
            "option_3": {
                "Blackboard": lambda: fufu1("Imaginary School - Main Menu - Blackboard")
            },
            "option_4": {
                "Vocabulary Training": {
                    "menu_header": "Welcome to the Vocabulary Training section:",
                    "option_0": {
                        "A1": lambda: fufu1(
                            "Imaginary School - Main Menu - Vocabulary Training - A1"
                        )
                    },
                    "option_1": {
                        "A2": lambda: fufu1(
                            "Imaginary School - Main Menu - Vocabulary Training - A2"
                        )
                    },
                    "option_2": {
                        "B1-B2": lambda: fufu1(
                            "Imaginary School - Main Menu - Vocabulary Training - B1-B2"
                        )
                    },
                    "option_3": {
                        "C1-C2": lambda: fufu1(
                            "Imaginary School - Main Menu - Vocabulary Training - C1-C2"
                        )
                    },
                    "option_4": {
                        "Training for Tests": {
                            "menu_header": "Specific Test Training",
                            "option_0": {
                                "Sub Option 0": lambda: fufu1(
                                    "Imaginary School - Main Menu - Vocabulary Training - Suboption 0"
                                )
                            },
                            "option_1": {
                                "Sub Option 1": lambda: fufu1(
                                    "Imaginary School - Main Menu - Vocabulary Training - Suboption 1"
                                )
                            },
                            "option_2": {
                                "Sub Option 2": lambda: fufu1(
                                    "Imaginary School - Main Menu - Vocabulary Training - SubOption 2"
                                )
                            },
                            "option_3": {
                                "Sub Option 3": lambda: fufu1(
                                    "Imaginary School - Main Menu - Vocabulary Training - Suboption 3"
                                )
                            },
                            "option_4": {
                                "Sub Option 4": lambda: fufu1(
                                    "Imaginary School - Main Menu - Vocabulary Training - Suboption 4"
                                )
                            },
                            "option_5": {
                                "Go back": ("main", "option_4", "Vocabulary Training")
                            },
                        },
                    },
                    "option_5": {"Go back": ("main",)},
                },
            },
        }
    }
    start_menu(stama)

    """
    menu_config.menulen = menu_len
    menu_config.add_spaces_right = n_spaces_right
    menu_config.add_spaces_left = n_spaces_left
    menu_config.menulen_highlighted = menu_len_selected
    menu_config.add_spaces_right_highlighted = n_spaces_right_selected
    menu_config.add_spaces_left_highlighted = n_spaces_left_selected
    menu_config.use_rjust = rjust
    menu_config.refresh_sleep = refresh_time
    menu_config.quit_keys = quit_keys
    menu_config.enter_keys = enter_keys
    menu_config.key_up_keys = key_up_keys
    menu_config.key_down_keys = key_down_keys

    menu_config.menudict = menudict
    curses.wrapper(main)


def init_screen(stdscr):
    curses.initscr()
    stdscr.clear()
    curses.curs_set(0)
    curses.noecho()
    stdscr.keypad(True)
    stdscr.refresh()


def main(stdscr):
    init_screen(stdscr)

    def rjust(s, active=False):
        if not active:
            return (
                str(
                    (menu_config.add_spaces_left * " ")
                    + str(s)
                    + (menu_config.add_spaces_right * " ")
                ).rjust(menu_config.menulen)
                + "\n"
            )
        return (
            str(
                (menu_config.add_spaces_left_highlighted * " ")
                + str(s)
                + (menu_config.add_spaces_right_highlighted * " ")
            ).rjust(menu_config.menulen_highlighted)
            + "\n"
        )

    def ljust(s, active=False):
        if not active:
            return (
                str(
                    (menu_config.add_spaces_left * " ")
                    + str(s)
                    + (menu_config.add_spaces_right * " ")
                ).ljust(menu_config.menulen)
                + "\n"
            )
        return (
            str(
                (menu_config.add_spaces_left_highlighted * " ")
                + str(s)
                + (menu_config.add_spaces_right_highlighted * " ")
            ).ljust(menu_config.menulen_highlighted)
            + "\n"
        )

    def break_window():
        nonlocal refresh_window
        refresh_window = False
        sleep(menu_config.refresh_sleep * 10)

    def refresh_thread():
        while refresh_window:
            stdscr.refresh()
            sleep(menu_config.refresh_sleep)

    def print_menu(header, all_menu_choices):
        stdscr.clear()
        stdscr.addstr(f"{header}\n")
        for i, choice in enumerate(all_menu_choices):
            if i == current_choice:
                stdscr.addstr(juststring(choice, True), curses.A_REVERSE)
            else:
                stdscr.addstr(juststring(choice))

    def get_active_dict(midi, keys):
        return reduce(operator.getitem, keys, midi)

    def get_active_menu_items(di):
        return list(
            flatten_everything(
                [
                    (list(di[keyx]))
                    for keyx, itemx in di.items()
                    if re.match(r"option_\d+", keyx)
                ]
            )
        )

    current_choice = 0

    # Get user input until 'q' is pressed
    t = Thread(target=refresh_thread)
    refresh_window = True
    t.start()
    juststring = rjust if menu_config.use_rjust else ljust
    active_choices = get_active_dict(menu_config.menudict, ["main"])
    active_menu_choices = get_active_menu_items(active_choices)
    print_menu(
        header=active_choices["menu_header"], all_menu_choices=active_menu_choices
    )

    while True:
        print_menu(
            header=active_choices["menu_header"], all_menu_choices=active_menu_choices
        )

        key = stdscr.getkey()

        if key in menu_config.quit_keys:
            break_window()
            break
        elif key in menu_config.enter_keys:
            o = active_choices[f"option_{current_choice}"]
            first_key_o = list(o.keys())[0]
            if callable(fu := o[first_key_o]):
                fu()
            elif isinstance(fu, dict):
                active_choices = fu
                active_menu_choices = get_active_menu_items(active_choices)
                current_choice = 0
            elif isinstance(fu, tuple):
                active_choices = get_active_dict(menu_config.menudict, fu)
                active_menu_choices = get_active_menu_items(active_choices)
                current_choice = 0
        if key in menu_config.key_down_keys:
            current_choice = (current_choice + 1) % len(active_menu_choices)
        elif key == menu_config.key_up_keys:
            current_choice = (current_choice - 1) % len(active_menu_choices)
    curses.endwin()
