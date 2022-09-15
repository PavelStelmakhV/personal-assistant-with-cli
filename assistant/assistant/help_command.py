def show_commands():
        for i in commands_desc:
            print(i)

action_commands = ["help", "hello", "contact add", "contact del", "contact edit", "contact find", "contact show", "contact birthday", "note add", \
    "note del", "note edit", "note find", "note show", "note edit tag", "note show by tag", "note find by tag",  "sort file"]
exit_commands = ["good_bye", "close", "exit", "."]
commands_description = ["Returns the list of available CLI commands", "Welcoming the user", "Adding the Record to the AddressBook", \
    "Deleting the Record", "Editing the Record", "Searching for the Record", "Returns the Records in Addressbook", \
        "Returns the list of Records with the birthdays within the requested period",
        "Adding the Note to the Notebook", "Deleting the Note", "Editing the text of the Note", "Search for the Note", \
    "Displays the Note", "Changing the Note's Tag", "Returns the list of Notes by Tag", \
        "Searching the Note by Tag", "Sorting the files in a specified directory" , "Exits the program"]
commands_desc = [f"<<{cmd}>> - {desc}" for cmd, desc in zip(action_commands + [', '.join(exit_commands)], commands_description)]
