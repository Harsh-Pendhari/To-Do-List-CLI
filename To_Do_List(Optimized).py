from time import sleep
import json
import os
import sys
import tabulate
from json import dump, load
from pathlib import Path as path

import colorama
from colorama import Fore as fore, Style as style

colorama.init(autoreset=True)

red = fore.RED
yellow = fore.YELLOW
green = fore.GREEN
cyan = fore.CYAN
light_magenta = fore.LIGHTMAGENTA_EX
light_cyan = fore.LIGHTCYAN_EX
white = fore.WHITE
light_white = fore.LIGHTWHITE_EX
light_blue = fore.LIGHTBLUE_EX
blue = fore.BLUE

class Functions:
    json_path = "To_Do_List.json"

    def typeWriter(self, toPrint: str, colour):
        s = str(toPrint)
        for ch in s:
            print(colour + style.BRIGHT + ch, end="", flush=True)
            sleep(0.02)

    def header_section(self, username, list_name=None, task_name=None):
        self.typeWriter(f"User : {username}\n", yellow)
        if list_name is not None:
            self.typeWriter(f"Selected List : {list_name}\n", blue)
        if task_name is not None:
            self.typeWriter(f"Selected Task : {task_name}\n", green)
        print()

    def yes_no_checker(self, response):
        r = str(response).strip().lower()
        if r in ("yes", "y"):
            return True
        if r in ("no", "n"):
            return False
        self.typeWriter("Invalid Option! Please Try Again", red)
        return None

    def tabulate_data(self, data):
        rows = [[white + style.BRIGHT + str(t), white + style.BRIGHT + str(d)] for t, d in data]
        header = [light_cyan + style.BRIGHT + "Tasks", light_cyan + style.BRIGHT + "Deadlines"]
        table = tabulate.tabulate(rows, headers=header, tablefmt="grid", stralign="left", disable_numparse=True)
        print(table + style.RESET_ALL)

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def json_read(self):
        with open(self.json_path, 'r') as file:
            data = load(file)
        return data

    def json_dumper(self, data):
        with open(self.json_path, 'w') as file:
            dump(data, file, indent=4)

    def json_write_user_name(self, write_data: any):
        uName = {
            "User_Names": [write_data],
            write_data: {
                "lists": [],
                "list_tasks": {}
            }
        }
        with open(self.json_path, 'w') as file:
            dump(uName, file, indent=4)

    def json_write_list(self, user, to_do_list_name: any):
        data = self.json_read()
        data[user]["lists"].append(to_do_list_name)
        data[user]["list_tasks"][to_do_list_name] = {}
        with open(self.json_path, 'w') as file:
            dump(data, file, indent=4)

    def json_write_list_tasks(self, user, task_to_add: any, list_name, deadline="None"):
        data = self.json_read()
        data[user]["list_tasks"][list_name][task_to_add] = deadline
        with open(self.json_path, 'w') as file:
            dump(data, file, indent=4)

    def json_write_new_user_name(self, new_user_name):
        data = self.json_read()
        data["User_Names"].append(new_user_name)
        data[new_user_name] = {
            "lists": [],
            "list_tasks": {}
        }
        with open(self.json_path, 'w') as file:
            dump(data, file, indent=4)

    def json_delete_user(self, username):
        data = self.json_read()
        del data[username]
        data["User_Names"].remove(username)
        self.json_dumper(data)

    def json_delete_list(self, username, listname):
        data = self.json_read()
        data[username]["lists"].remove(listname)
        del data[username]["list_tasks"][listname]
        self.json_dumper(data)

    def json_delete_list_tasks(self, username, listname, taskname):
        data = self.json_read()
        del data[username]["list_tasks"][listname][taskname]
        self.json_dumper(data)

class To_Do_List:
    def __init__(self):
        if path("To_Do_List.json").exists():
            try:
                userNames = Functions().json_read()
            except Exception:
                Functions().typeWriter("Data file is corrupted. Creating a new one.\n", red)
                self.first_time_setup()
                return
            if len(userNames.get("User_Names", [])) > 1:
                self.select_User()
            else:
                try:
                    uName = Functions().json_read()
                    UName_list = uName.get("User_Names", [])
                    if not UName_list:
                        self.first_time_setup()
                        return
                    UName = UName_list[0]
                    Functions().header_section(UName)
                    Functions().typeWriter(f"======== Welcome {UName} ========\n\n", cyan)
                    self.welcome_menu_screen(UName)
                except Exception as e:
                    Functions().typeWriter(str(e), red)
        else:
            self.first_time_setup()

    def first_time_setup(self):
        Functions().typeWriter("======== WELCOME TO THE TO-DO LIST CLI ========\n\n", cyan)
        Functions().typeWriter("Please Enter Your Name : ", light_cyan)
        userName = input()
        try:
            Functions().json_write_user_name(userName)
        except Exception as e:
            print(str(e))
        else:
            Functions().clear_screen()
            Functions().header_section(userName)
            self.welcome_menu_screen(userName)

    def select_User(self):
        data = Functions().json_read()
        user_count = len(data['User_Names'])
        while True:
            Functions().clear_screen()
            count = 1
            for users in data['User_Names']:
                Functions().typeWriter(f"[{count}] {users}\n", white)
                count += 1
            Functions().typeWriter("\nSelect User to View/Switch : ", light_cyan)
            try:
                pick = input().strip()
                if pick.lower() == 'm':
                    Functions().clear_screen()
                    selected = data['User_Names'][0]
                    Functions().header_section(selected)
                    self.welcome_menu_screen(selected)
                    return
                user = int(pick)
                if user <= 0 or user > user_count:
                    Functions().typeWriter("Please Enter a Valid Option", red)
                    sleep(1.0)
                    continue
                selected_user = data["User_Names"][user - 1]
                Functions().clear_screen()
                Functions().header_section(selected_user)
                Functions().typeWriter(f"======== Welcome {selected_user} ========\n\n", cyan)
                self.welcome_menu_screen(selected_user)
                return
            except ValueError:
                Functions().typeWriter("Please Enter a Valid Option", red)
                sleep(1.0)
                continue

    def welcome_menu_screen(self, selected_user):
        while True:
            Functions().typeWriter("[1] Create New List\n[2] Create New User\n[3] Edit List(s)\n[4] View List(s)\n[5] View/Switch User\n[6] Delete List(s)\n[7] Delete User\n[8] Exit\n\n", white)
            Functions().typeWriter("Enter Your Choice : ", light_cyan)
            try:
                pick = input().strip()
                selected_option = int(pick)
                if selected_option <= 0 or selected_option > 8:
                    Functions().typeWriter("Please Enter a Valid Option", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
                if selected_option == 1:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.create_new_list(selected_user)
                    return
                elif selected_option == 2:
                    Functions().clear_screen()
                    self.create_new_user(selected_user)
                    return
                elif selected_option == 3:
                    Functions().clear_screen()
                    self.edit_list(selected_user)
                    return
                elif selected_option == 4:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.view_list(selected_user)
                    return
                elif selected_option == 5:
                    Functions().clear_screen()
                    self.select_User()
                    return
                elif selected_option == 6:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.delete_list(selected_user)
                    return
                elif selected_option == 7:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.delete_user(selected_user)
                    return
                elif selected_option == 8:
                    sys.exit()
            except ValueError:
                Functions().typeWriter("Please Enter a Valid Option", red)
                sleep(1.0)
                Functions().clear_screen()
                Functions().header_section(selected_user)
                continue

    def create_new_list(self, user_name):
        while True:
            Functions().typeWriter("(Enter '0' to go back)\n\n", yellow)
            Functions().typeWriter("Enter New List's Name : ", light_cyan)
            data = Functions().json_read()
            try:
                list_name = str(input())
                if list_name == '0':
                    Functions().clear_screen()
                    Functions().header_section(user_name)
                    self.welcome_menu_screen(user_name)
                    return
                if list_name.strip() == "":
                    Functions().typeWriter("\nList Name Cannot be Blank!", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(user_name)
                    continue
                if list_name in data[user_name]["lists"]:
                    Functions().typeWriter("\nList Name Already Exists.", red)
                    Functions().typeWriter(f" Do you want to edit the existing list '{list_name}'? [y/n] : ", light_cyan)
                    yes_no = input().lower()
                    yes_no_respo = Functions().yes_no_checker(yes_no)
                    if yes_no_respo:
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        self.edit_list(user_name)
                        return
                    elif yes_no_respo is False:
                        Functions().clear_screen()
                        Functions().header_section(user_name)
                        continue
                    else:
                        sleep(1.0)
                        Functions().clear_screen()
                        Functions().header_section(user_name)
                        continue
                Functions().json_write_list(user_name, list_name)
                Functions().clear_screen()
                Functions().header_section(user_name, list_name)
                while True:
                    Functions().typeWriter(f"List '{list_name}' Created Successfully !\n\n", green)
                    Functions().typeWriter("Do you want to continue with adding Tasks to the List? [y/n] : ", light_cyan)
                    try:
                        yes_no = str(input()).lower()
                        yes_no_respo = Functions().yes_no_checker(yes_no)
                        if yes_no_respo:
                            Functions().clear_screen()
                            Functions().header_section(user_name, list_name)
                            self.add_tasks(user_name, list_name)
                            return
                        elif yes_no_respo is False:
                            Functions().clear_screen()
                            Functions().header_section(user_name)
                            self.welcome_menu_screen(user_name)
                            return
                        else:
                            sleep(1.0)
                            Functions().clear_screen()
                            Functions().header_section(user_name, list_name)
                            continue
                    except Exception as e:
                        Functions().typeWriter(str(e), red)
            except Exception as e:
                Functions().typeWriter(str(e), red)

    def add_tasks(self, user_name, list_name):
        while True:
            data = Functions().json_read()
            Functions().typeWriter("(Enter '0' to go back)\n\n", yellow)
            Functions().typeWriter("Enter Task : ", light_cyan)
            task_name = input()
            keys = list((data[user_name]["list_tasks"][list_name]).keys())
            if task_name.strip() == "":
                Functions().typeWriter("Task Name Cannot be Blank!", red)
                sleep(1.0)
                Functions().clear_screen()
                Functions().header_section(user_name, list_name)
                continue
            if task_name == "0":
                Functions().clear_screen()
                Functions().header_section(user_name)
                self.welcome_menu_screen(user_name)
                return
            if task_name in keys:
                Functions().typeWriter("\n\nTask Already Added. ", red)
                Functions().typeWriter("Do you want to edit task? [y/n] : ", light_cyan)
                try:
                    yes_no = input().lower()
                    yes_no_response = Functions().yes_no_checker(yes_no)
                    if yes_no_response:
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name, task_name)
                        self.edit_tasks(user_name, list_name)
                        return
                    elif yes_no_response is False:
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        continue
                    else:
                        sleep(1.0)
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        continue
                except Exception as e:
                    Functions().typeWriter(str(e), red)
                    continue
            while True:
                Functions().clear_screen()
                Functions().header_section(user_name, list_name, task_name)
                Functions().typeWriter("(Enter '0' to go back)\n", yellow)
                Functions().typeWriter(f"Do You Want to Add Deadline For the Task '{task_name}'? [y/n] : ", light_cyan)
                try:
                    yes_no = input().lower()
                    if yes_no == "0":
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        break
                    yes_no_respo = Functions().yes_no_checker(yes_no)
                    if yes_no_respo:
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name, task_name)
                        Functions().typeWriter("Enter Deadline : ", light_cyan)
                        deadline = input()
                        if deadline.strip() == "":
                            Functions().typeWriter("Deadline Cannot be Blank!", red)
                            continue
                        Functions().json_write_list_tasks(user_name, task_name, list_name, deadline)
                        Functions().typeWriter("Task Added Successfully!", green)
                        sleep(1.0)
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        break
                    elif yes_no_respo is False:
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        Functions().json_write_list_tasks(user_name, task_name, list_name)
                        Functions().typeWriter("Task Added Successfully!", green)
                        sleep(1.0)
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        break
                    else:
                        sleep(1.0)
                        Functions().clear_screen()
                        Functions().header_section(user_name, list_name)
                        continue
                except Exception as e:
                    Functions().typeWriter(str(e), red)

    def edit_tasks(self, user_name, list_name):
        while True:
            data = Functions().json_read()
            tasks = list((data[user_name]['list_tasks'][list_name]).keys())
            deadlines = list((data[user_name]['list_tasks'][list_name]).values())
            if not tasks:
                Functions().typeWriter("No tasks yet.\n", yellow)
                sleep(0.7)
                Functions().clear_screen()
                Functions().header_section(user_name, list_name)
                self.add_tasks(user_name, list_name)
                return
            for task, deadline, count in zip(tasks, deadlines, (range(1, len(tasks) + 1))):
                Functions().typeWriter(f"[{count}] {task} : {deadline}\n", white)
            Functions().typeWriter("(Enter '0' to go back or 'm' for main menu)\n\n", yellow)
            Functions().typeWriter("Select Task You Want to Edit : ", light_cyan)
            try:
                pick = input().strip()
                if pick.lower() == 'm':
                    Functions().clear_screen()
                    Functions().header_section(user_name)
                    self.welcome_menu_screen(user_name)
                    return
                selection = int(pick)
                if selection == 0:
                    Functions().clear_screen()
                    Functions().header_section(user_name, list_name)
                    self.add_tasks(user_name, list_name)
                    return
                if selection > len(tasks) or selection < 0:
                    Functions().typeWriter("\nPlease Choose a Valid Option!", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(user_name, list_name)
                    continue
                while True:
                    task_to_edit = tasks[selection - 1]
                    Functions().clear_screen()
                    Functions().header_section(user_name, list_name, task_to_edit)
                    Functions().typeWriter(f"\n[1] Edit/ Remove Deadline\n[2] Change Task Name\n[3] Delete Task\n[4] Back to Main Menu\n\n", white)
                    Functions().typeWriter(f"Enter Your choice : ", light_cyan)
                    try:
                        pick2 = input().strip()
                        if pick2.lower() == 'm':
                            Functions().clear_screen()
                            Functions().header_section(user_name)
                            self.welcome_menu_screen(user_name)
                            return
                        edit_option = int(pick2)
                        if edit_option == 1:
                            Functions().typeWriter("Enter New Deadline (Leave Blank to remove Deadline) : ", light_cyan)
                            deadline = input()
                            if deadline.strip() == "":
                                data = Functions().json_read()
                                data[user_name]["list_tasks"][list_name][task_to_edit] = "None"
                                with open('To_Do_List.json', 'w') as file:
                                    json.dump(data, file, indent=4)
                                Functions().typeWriter("\n\nTask Edited Successfully!", green)
                                sleep(1.0)
                                Functions().clear_screen()
                                Functions().header_section(user_name, list_name)
                                self.add_tasks(user_name, list_name)
                                return
                            else:
                                data = Functions().json_read()
                                data[user_name]["list_tasks"][list_name][task_to_edit] = deadline
                                with open('To_Do_List.json', 'w') as file:
                                    json.dump(data, file, indent=4)
                                Functions().typeWriter("\n\nTask Edited Successfully!", green)
                                sleep(1.0)
                                Functions().clear_screen()
                                Functions().header_section(user_name, list_name)
                                self.add_tasks(user_name, list_name)
                                return
                        elif edit_option == 2:
                            while True:
                                task_to_edit = tasks[selection - 1]
                                Functions().typeWriter("\n(Enter '0' to go back)\n", yellow)
                                Functions().typeWriter(f"\nEnter New Name for the task '{task_to_edit}' : ", light_cyan)
                                new_name_for_task = input()
                                if new_name_for_task == "0":
                                    Functions().clear_screen()
                                    Functions().header_section(user_name, list_name, task_to_edit)
                                    break
                                if new_name_for_task.strip() == "":
                                    Functions().typeWriter("Task Name cannot be blank!", red)
                                    sleep(1.0)
                                    Functions().clear_screen()
                                    Functions().header_section(user_name, list_name, task_to_edit)
                                    continue
                                data = Functions().json_read()
                                old_key_value = (data[user_name]["list_tasks"][list_name][task_to_edit])
                                Functions().json_delete_list_tasks(user_name, list_name, task_to_edit)
                                Functions().json_write_list_tasks(user_name, new_name_for_task, list_name, old_key_value)
                                Functions().typeWriter(f"Task name changed successfully from {task_to_edit} -> {new_name_for_task}", green)
                                sleep(1.0)
                                Functions().clear_screen()
                                Functions().header_section(user_name, list_name)
                                self.add_tasks(user_name, list_name)
                                return
                        elif edit_option == 3:
                            Functions().typeWriter(f"Are You Sure You Want to Delete the task '{task_to_edit}'? [y/n] : ", red)
                            yes_no = input()
                            if yes_no.strip().lower() in ("y", "yes"):
                                Functions().json_delete_list_tasks(user_name, list_name, task_to_edit)
                                Functions().typeWriter(f"Task '{task_to_edit}' Deleted Successfully!", green)
                                Functions().clear_screen()
                                Functions().header_section(user_name, list_name)
                                self.add_tasks(user_name, list_name)
                                return
                            elif yes_no.strip().lower() in ("n", "no"):
                                continue
                            else:
                                Functions().typeWriter("Invalid Option! Please Try Again", red)
                                sleep(1.0)
                                Functions().clear_screen()
                                Functions().header_section(user_name, list_name)
                                continue
                        elif edit_option == 4:
                            Functions().clear_screen()
                            Functions().header_section(user_name)
                            self.welcome_menu_screen(user_name)
                            return
                        else:
                            Functions().typeWriter("Please Choose a Valid Option!", red)
                            sleep(1.0)
                            Functions().clear_screen()
                            Functions().header_section(user_name, list_name)
                            continue
                    except Exception as e:
                        Functions().typeWriter(str(e), red)
            except Exception as e:
                Functions().typeWriter(str(e), red)

    def create_new_user(self, selected_user):
        while True:
            Functions().typeWriter("(Enter '0' to go back or 'm' for main menu)\n\n", yellow)
            Functions().typeWriter("Enter Username to create new User: ", light_cyan)
            new_username = input().strip()
            if new_username.lower() == 'm':
                Functions().clear_screen()
                Functions().header_section(selected_user)
                self.welcome_menu_screen(selected_user)
                return
            data = Functions().json_read()
            user_names = data["User_Names"]
            if new_username == '0':
                Functions().clear_screen()
                Functions().header_section(selected_user)
                self.welcome_menu_screen(selected_user)
                return
            if new_username.strip() == "":
                Functions().typeWriter("\nUsername Cannot be blank", red)
                Functions().clear_screen()
                Functions().header_section(selected_user)
                continue
            if new_username in user_names:
                Functions().typeWriter(f"User with name '{new_username}' already exists!\nDo you want to continue with this existing user? [y/n] : ", light_magenta)
                yes_no = input()
                yes_no_response = Functions().yes_no_checker(yes_no)
                if yes_no_response:
                    Functions().clear_screen()
                    Functions().header_section(new_username)
                    Functions().typeWriter(f"======== Welcome {new_username} ========\n\n", cyan)
                    self.welcome_menu_screen(new_username)
                    return
                elif yes_no_response is False:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
                else:
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
            Functions().json_write_new_user_name(new_username)
            Functions().clear_screen()
            Functions().header_section(new_username)
            Functions().typeWriter(f"New User '{new_username}' Created Successfully!", green)
            sleep(1.0)
            Functions().clear_screen()
            Functions().header_section(new_username)
            self.welcome_menu_screen(new_username)
            return

    def edit_list(self, username):
        while True:
            data = Functions().json_read()
            list_names = data[username]["lists"]
            if not list_names:
                Functions().typeWriter("No lists yet.\n", yellow)
                sleep(0.7)
                Functions().clear_screen()
                Functions().header_section(username)
                self.welcome_menu_screen(username)
                return
            count = 1
            for list_name in list_names:
                Functions().typeWriter(f"[{count}] {list_name}\n", white)
                count += 1
            Functions().typeWriter(f"(Enter '0' to go back or 'm' for main menu)\n\n", yellow)
            Functions().typeWriter(f"Select the List You want to edit : ", light_cyan)
            try:
                pick = input().strip()
                if pick.lower() == 'm':
                    Functions().clear_screen()
                    Functions().header_section(username)
                    self.welcome_menu_screen(username)
                    return
                user_selection = int(pick)
                if user_selection == 0:
                    Functions().clear_screen()
                    Functions().header_section(username)
                    self.welcome_menu_screen(username)
                    return
                if user_selection < 0 or user_selection > (len(list_names)):
                    Functions().typeWriter("Invalid Option! Please Try Again", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(username)
                    continue
                while True:
                    selected_list = data[username]["lists"][user_selection - 1]
                    Functions().clear_screen()
                    Functions().header_section(username, selected_list)
                    Functions().typeWriter("[1] Change List Name\n[2] Add Tasks to the selected List\n[3] Edit Tasks in the Selected List\n[4] Delete List\n\n", white)
                    Functions().typeWriter("(Enter '0' to go back or 'm' for main menu)\n", yellow)
                    Functions().typeWriter("Enter Your Choice : ", light_cyan)
                    try:
                        pick2 = input().strip()
                        if pick2.lower() == 'm':
                            Functions().clear_screen()
                            Functions().header_section(username)
                            self.welcome_menu_screen(username)
                            return
                        if pick2 == '':
                            Functions().typeWriter("\n\nInvalid Selection ", red)
                            sleep(1.0)
                            Functions().clear_screen()
                            Functions().header_section(username, selected_list)
                            continue
                        selected_option = int(pick2)
                        if selected_option == 0:
                            Functions().clear_screen()
                            Functions().header_section(username)
                            break
                        if selected_option > 4 or selected_option < 0:
                            Functions().typeWriter("Invalid Option! Please Try Again", red)
                            sleep(1.0)
                            continue
                        if selected_option == 1:
                            while True:
                                Functions().clear_screen()
                                Functions().header_section(username, selected_list)
                                Functions().typeWriter("(Enter '0' to go back or 'm' for main menu)\n", yellow)
                                Functions().typeWriter(f"Enter New Name For the List '{selected_list}' : ", light_cyan)
                                new_name = input()
                                if new_name.lower() == 'm':
                                    Functions().clear_screen()
                                    Functions().header_section(username)
                                    self.welcome_menu_screen(username)
                                    return
                                if new_name.strip() == '':
                                    Functions().typeWriter("\n\nList Name Cannot be empty! ", red)
                                    Functions().typeWriter("Please Try Again.", light_cyan)
                                    sleep(1.0)
                                    continue
                                if new_name == "0":
                                    Functions().clear_screen()
                                    break
                                old_list_name = data[username]["lists"][user_selection - 1]
                                old_list_data = dict(data[username]["list_tasks"].get(old_list_name, {}))
                                Functions().json_delete_list(username, old_list_name)
                                Functions().json_write_list(username, new_name)
                                data = Functions().json_read()
                                data[username]["list_tasks"][new_name] = old_list_data
                                Functions().json_dumper(data)
                                Functions().typeWriter("\n\nList Name Updated Successfully!", green)
                                sleep(1.0)
                                Functions().clear_screen()
                                Functions().header_section(username, new_name)
                                self.edit_list(username)
                                return
                        elif selected_option == 2:
                            Functions().clear_screen()
                            Functions().header_section(username, selected_list)
                            self.add_tasks(username, selected_list)
                            return
                        elif selected_option == 3:
                            Functions().clear_screen()
                            Functions().header_section(username, selected_list)
                            self.edit_tasks(username, selected_list)
                            return
                        elif selected_option == 4:
                            Functions().clear_screen()
                            Functions().typeWriter(f"Are you sure you want to delete the list '{selected_list}'? [y/n] : ", red)
                            yes_no = input().lower()
                            yes_no_respo = Functions().yes_no_checker(yes_no)
                            if yes_no_respo:
                                Functions().json_delete_list(username, selected_list)
                                Functions().typeWriter(f"\nList '{selected_list}' Deleted Successfully!", green)
                                sleep(1.0)
                                Functions().clear_screen()
                                self.edit_list(username)
                                return
                            elif yes_no_respo is False:
                                Functions().clear_screen()
                                continue
                            else:
                                sleep(1.0)
                                continue
                    except Exception as e:
                        Functions().typeWriter(str(e), red)
            except Exception as e:
                Functions().typeWriter(str(e), red)

    def view_list(self, selected_user):
        while True:
            data = Functions().json_read()
            list_names = data[selected_user]["lists"]
            if not list_names:
                Functions().typeWriter("No lists yet.\n", yellow)
                sleep(0.7)
                Functions().clear_screen()
                Functions().header_section(selected_user)
                self.welcome_menu_screen(selected_user)
                return
            count = 1
            for list_name in list_names:
                Functions().typeWriter(f"[{count}] {list_name}\n", white)
                count += 1
            Functions().typeWriter(f"(Enter '0' to go back)\n\n", yellow)
            Functions().typeWriter(f"Select the List You want to View : ", light_cyan)
            try:
                user_selection = int(input())
                if user_selection == 0:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.welcome_menu_screen(selected_user)
                    return
                if user_selection < 0 or user_selection > (len(list_names)):
                    Functions().typeWriter("Invalid Option! Please Try Again", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
                while True:
                    list_task_name = data[selected_user]["lists"][user_selection - 1]
                    Functions().clear_screen()
                    Functions().header_section(selected_user, list_task_name)
                    table_data = list((data[selected_user]["list_tasks"][list_task_name]).items())
                    Functions().typeWriter(f"{list_task_name} :-\n\n", blue)
                    if table_data:
                        Functions().tabulate_data(table_data)
                    else:
                        Functions().typeWriter("No tasks yet.\n", yellow)
                    print()
                    Functions().typeWriter("Enter '0' to go back or 'e' to edit tasks : ", yellow)
                    try:
                        check_for_back = input().strip()
                        if check_for_back == "0":
                            Functions().clear_screen()
                            Functions().header_section(selected_user)
                            break
                        elif check_for_back.lower() == "e":
                            Functions().clear_screen()
                            Functions().header_section(selected_user, list_task_name)
                            self.edit_tasks(selected_user, list_task_name)
                            return
                        else:
                            Functions().typeWriter("Invalid Option. Please Try Again!", red)
                            sleep(0.5)
                            continue
                    except Exception as e:
                        Functions().typeWriter(str(e), red)
            except Exception as e:
                Functions().typeWriter(str(e), red)

    def delete_list(self, username):
        while True:
            data = Functions().json_read()
            list_names = data[username]["lists"]
            if not list_names:
                Functions().typeWriter("No lists to delete.\n", yellow)
                sleep(0.7)
                Functions().clear_screen()
                Functions().header_section(username)
                self.welcome_menu_screen(username)
                return
            count = 1
            for list_name in list_names:
                Functions().typeWriter(f"[{count}] {list_name}\n", white)
                count += 1
            Functions().typeWriter(f"(Enter '0' to go back)\n\n", yellow)
            Functions().typeWriter(f"Select the List You want to Delete : ", light_cyan)
            try:
                pick = input().strip()
                user_selection = int(pick)
                if user_selection == 0:
                    Functions().clear_screen()
                    Functions().header_section(username)
                    self.welcome_menu_screen(username)
                    return
                if user_selection < 0 or user_selection > (len(list_names)):
                    Functions().typeWriter("Invalid Option! Please Try Again", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(username)
                    continue
                list_name_to_delete = list_names[user_selection - 1]
                Functions().clear_screen()
                Functions().header_section(username)
                Functions().typeWriter(f"Are You Sure You Want to Delete '{list_name_to_delete}'? [y/n] : ", red)
                yes_no = input()
                yes_no_respo = Functions().yes_no_checker(yes_no)
                if yes_no_respo:
                    Functions().json_delete_list(username, list_name_to_delete)
                    Functions().clear_screen()
                    Functions().header_section(username)
                    Functions().typeWriter(f"List '{list_name_to_delete}' Deleted Successfully!", green)
                    sleep(0.7)
                    Functions().clear_screen()
                    Functions().header_section(username)
                    continue
                elif yes_no_respo is False:
                    Functions().clear_screen()
                    Functions().header_section(username)
                    continue
                else:
                    sleep(0.5)
                    Functions().clear_screen()
                    Functions().header_section(username)
                    continue
            except Exception as e:
                Functions().typeWriter(str(e), red)

    def delete_user(self, selected_user):
        while True:
            data = Functions().json_read()
            user_count = len(data['User_Names'])
            count = 1
            for users in data['User_Names']:
                Functions().typeWriter(f"[{count}] {users}\n", white)
                count += 1
            Functions().typeWriter("(Press '0' to go back or 'm' for main menu)\n", yellow)
            Functions().typeWriter("\nSelect User to Delete : ", light_cyan)
            try:
                pick = input().strip()
                if pick.lower() == 'm':
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.welcome_menu_screen(selected_user)
                    return
                user = int(pick)
                if user == 0:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    self.welcome_menu_screen(selected_user)
                    return
                if user < 0 or user > user_count:
                    Functions().typeWriter("Please Enter a Valid Option", red)
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
                Functions().clear_screen()
                username_to_delete = data["User_Names"][user - 1]
                Functions().typeWriter(f"Are you sure you want to Delete the User '{username_to_delete}'? [y/n] : ", red)
                yes_no = input()
                yes_no_respo = Functions().yes_no_checker(yes_no)
                if yes_no_respo:
                    Functions().json_delete_user(username_to_delete)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    Functions().typeWriter(f"User '{username_to_delete}' Deleted Successfully!", green)
                    sleep(0.7)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
                elif yes_no_respo is False:
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
                else:
                    sleep(1.0)
                    Functions().clear_screen()
                    Functions().header_section(selected_user)
                    continue
            except ValueError:
                Functions().typeWriter("Please Enter a Valid Option", red)
                sleep(1.0)
                Functions().clear_screen()
                Functions().header_section(selected_user)
                continue

if __name__ == "__main__":
    To_Do_List()
