def show_commands():
        for i in commands_desc:
            print(i)

action_commands = ["help", "add_record", "del_record", "edit_record", "show_birthdays", "add_note", "del_note", "edit_note_text", \
    "find_note", "show_note", "add_tag", "del_tag", "change_tag", "show_note_by_tag", "find_note_by_tag", "sort_files"]
exit_commands = ["good_bye", "close", "exit"]
commands_description = ["Returns the list of available CLI commands", "Adding the Record to the AddressBook", \
    "Deleting the Record", "Editing the Record", "Returns the list of Records with the birthdays within the requested period", \
        "Adding the Note to the Notebook", "Deleting the Note", "Editing the text of the Note", "Search for the Note", \
    "Displays the Note", "Adding the Tag to the Note", "Deleting the Tag", "Changing the Tag", "Returns the list of Notes by Tag", \
        "Searching the Note by Tag", "Sorting the files in a specified directory" , "Exits the program"]
commands_desc = [f"<<{cmd}>> - {desc}" for cmd, desc in zip(action_commands + [', '.join(exit_commands)], commands_description)]


show_commands()