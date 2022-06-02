import os
import json
import pandas as pd


class BotAnalyzer_A360:
    """
    Once bots and dependencies are exported we proceed to analyze
    """

    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf8") as f:
            self._bot = json.load(f)

    def get_count_total_lines(self):
        # This one also is counting disabled lines! (for support it might be neccesary to understand these too,
        # so I keep counting)
        return len(self._get_ids(self._bot["nodes"]))

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
                ids.append(obj.get('uid'))
                children = obj.get('children', None)
                branches = obj.get('branches', None)
                if children:
                    ids.extend(self._get_ids(children))
                if branches:
                    ids.extend(self._get_ids(branches))
            elif isinstance(obj, list):
                ids.extend(self._get_ids(obj))
        return ids
