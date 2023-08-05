# creates an interactive menu system for your application or program, providing an intuitive and user-friendly interface for users to navigate and perform various actions

## pip install ffmpegdevices

#### Tested against Windows 10 / Python 3.10 / Anaconda 
#### curses from https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses


### Simplifies menu creation: 

The start_menu function abstracts away the complexities of handling user input and managing the menu structure. It provides a convenient way to define menus and associate actions with menu options.

### Customizable appearance: 

The module allows you to customize various aspects of the menu, such as the length of menu items, spacing, justification, and refresh time. This flexibility enables you to adapt the menu to your specific needs.

### Keyboard shortcuts: 

The module supports configurable keyboard shortcuts for actions like quitting the menu, selecting options, and navigating through the menu. This allows for efficient and intuitive menu navigation.

### Nested menus: 

The module supports nested menus, allowing you to create a hierarchical menu structure. This is useful for organizing and categorizing menu options in a logical manner.

### Flexibility and extensibility: 

The module is designed to be flexible and easily extensible. You can modify the menu structure, add new options, and define custom actions according to your requirements.



```python


start_menu(
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

	
```

## copy and paste example


The provided example demonstrates how to use the start_menu function to create a menu system for an imaginary school. Each menu option is associated with a specific action, such as opening a file or performing a task. Here's a breakdown of the example:

The fufu1 function is defined, which writes the given key to a file and opens it in Notepad using subprocess.Popen. This function represents the action to be performed when a menu option is selected.

The stama dictionary defines the menu structure and options. It includes nested dictionaries to create submenus and associated actions.

The start_menu function is called with the stama dictionary as the argument. This will display the menu and allow the user to navigate and interact with the options.

	
	
```python
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

```