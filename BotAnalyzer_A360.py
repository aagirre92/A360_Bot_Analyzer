import os
import json
from collections import Counter
import pandas as pd


class BotAnalyzer_A360:
    """
    Once bots and dependencies are exported we proceed to analyze
    path: Path of the task bot file
    """

    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf8") as f:
            self._bot = json.load(f)

    def get_count_total_lines(self):
        """
        Only counts actions that are NOT disabled
        :return: Int
        """
        commands = self._get_commands()
        return len(commands)

    def get_if_error_handling(self):
        commands = self._get_commands()
        if "try" in commands:
            return True
        else:
            return False

    def get_number_of_loops(self):
        commands = self._get_commands()
        commands_count = Counter(commands)
        loop_counter = commands_count.get("loop.commands.start")
        if not loop_counter:
            return 0
        else:
            return loop_counter

    def get_if_steps(self):
        commands = self._get_commands()
        if "step" in commands:
            return True
        else:
            return False

    def get_if_comments(self):
        commands = self._get_commands()
        if "Comment" in commands:
            return True
        else:
            return False

    def get_if_scripts(self):
        commands = self._get_commands()
        if any(x in commands for x in
               ["vbscript.commands.openScript", "python.commands.openScript", "javascript.commands.openScript"]):
            return True
        else:
            return False

    def get_if_notification_emails(self):
        commands = self._get_commands()
        if "sendMail" in commands:
            return True
        else:
            return False

    def get_bot_name(self):
        return os.path.basename(self.path)

    def get_number_of_variables(self):
        return len(self._bot["variables"])

    def get_number_of_packages(self):
        return len(self._bot["packages"])

    def variable_df(self):
        variable_name = []
        variable_type = []
        variable_description = []
        variable_input = []
        variable_output = []
        for variable in self._bot["variables"]:
            variable_name.append(variable["name"])
            variable_type.append(variable["type"])
            variable_description.append(variable["description"])
            if variable["input"]:
                variable_input.append("True")
            else:
                variable_input.append("False")
            if variable["output"]:
                variable_output.append("True")
            else:
                variable_output.append("False")

        df_variables = pd.DataFrame(
            {"Name": variable_name, "Type": variable_type, "Description": variable_description, "Input": variable_input,
             "Output": variable_output})

        return df_variables

    def package_df(self):
        package_list = {
            "name": [],
            "version": []
        }
        for package in self._bot["packages"]:
            package_list["name"].append(package["name"])
            package_list["version"].append(package["version"])

        df_packages = pd.DataFrame({"Name": package_list['name'], "Version": package_list['version']})

        return df_packages

    def _get_ids(self, json_array):
        # Recursive function that has the aim to get every line of code
        # https://stackoverflow.com/questions/48394368/how-create-recursive-loop-for-parsing-the-json
        ids = []

        for obj in json_array:
            if isinstance(obj, dict):
                ids.append({'uid': obj.get('uid'), 'command': obj.get('commandName'), 'disabled': obj.get('disabled')})
                children = obj.get('children', None)
                branches = obj.get('branches', None)
                if children:
                    ids.extend(self._get_ids(children))
                if branches:
                    ids.extend(self._get_ids(branches))
            elif isinstance(obj, list):
                ids.extend(self._get_ids(obj))
        return ids

    def _get_commands(self):
        """
        Only return commands that are NOT disabled!!!!!
        :return: List
        """
        ids_dict = self._get_ids(self._bot["nodes"])
        commands = []
        for item in ids_dict:
            if not item['disabled']:
                commands.append(item["command"])
        return commands
