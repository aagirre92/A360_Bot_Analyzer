import os
import re
import requests
from datetime import datetime
import json
import tempfile
import zipfile
import pandas as pd

from BotAnalyzer_A360 import BotAnalyzer_A360
from functions import complexity_formula


class ReportGenerator:
    """
    This class generates a report taking as input the A360 CR credentials (user+password OR apikey) and the bot id
    """

    def __init__(self, control_room_url, username, password=None, api_key=None):
        assert control_room_url, 'You must provide a valid A360 CR URL'
        assert username, 'You must provide a username'
        assert password or api_key, "You must provide either user's password or api_key"

        if control_room_url[-1] == "/":
            self.control_room_url = control_room_url[:-1]

        self.username = username

        if password:
            self.password = password
        if api_key:
            self.api_key = api_key

        self._token = self._get_token()

    # PUBLIC METHODS
    def get_bot_full_reports(self, bot_id):

        uri = f"{self.control_room_url}/v2/blm/export"

        headers = {
            "X-Authorization": self._token,
            "Content-Type": "application/json"
        }

        payload = {
            "name": f"Bot_Analyzer_Export_{datetime.now().strftime('%d-%b-%Y_%H_%M_%S')}",
            "fileIds": [
                bot_id
            ],
            "includePackages": False
        }

        r = requests.post(url=uri, data=json.dumps(payload), headers=headers, verify=False)

        r.raise_for_status()

        export_id = r.json()["requestId"]

        status = self._check_bot_export_status(export_id)

        while status != "COMPLETED":
            status = self._check_bot_export_status(export_id)

        reports_dict = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            self._download_file(export_id, temp_dir)

            task_bot_paths = ReportGenerator.get_task_bot_paths(os.path.join(temp_dir, "manifest.json"))  # list

            other_dependencies_paths = ReportGenerator.get_file_dependency_paths(
                os.path.join(temp_dir, "manifest.json"))  # dict

            df_bots_overall_report = self._generate_overall_report(task_bot_paths)  # ONLY TASK BOTS

            reports_dict["bots"] = df_bots_overall_report

            df_dependencies_report = self._generate_file_dependency_report(other_dependencies_paths)  # EVERY FILE
            # BUT TASK BOTS

            reports_dict["other_dependencies"] = df_dependencies_report

            df_variables_report = self._generate_variable_report(task_bot_paths)

            reports_dict["variable_list"] = df_variables_report

            df_packages_report = self._generate_packages_report(task_bot_paths)

            reports_dict["packages"] = df_packages_report

            return reports_dict

    # PRIVATE METHODS

    def _get_token(self):

        uri = f"{self.control_room_url}/v1/authentication"

        headers = {
            "Content-Type": "application/json"
        }

        if hasattr(self, 'api_key'):
            payload = {
                "username": self.username,
                "apiKey": self.api_key
            }

        if hasattr(self, 'password'):
            payload = {
                "username": self.username,
                "password": self.password
            }

        r = requests.post(uri, data=json.dumps(payload), headers=headers, verify=False)

        r.raise_for_status()

        return r.json()["token"]

    def _check_bot_export_status(self, export_id):

        uri = f"{self.control_room_url}/v2/blm/status/{export_id}"

        headers = {
            "X-Authorization": self._token
        }

        r = requests.get(url=uri, headers=headers, verify=False)

        r.raise_for_status()

        if r.json()["errorMessage"]:

            raise Exception(
                f"Export was NOT successful for export id {export_id}, message: {r.json()['errorMessage']} ")
        else:
            return r.json()["status"]

    def _download_file(self, export_id, path):
        uri = f"{self.control_room_url}/v2/blm/download/{export_id}"
        headers = {
            "X-Authorization": self._token
        }

        r = requests.get(url=uri, headers=headers, verify=False)

        r.raise_for_status()

        zip_path = os.path.join(path, "response.zip")

        with open(zip_path, "wb+") as f:
            f.write(r.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(path)

        # print(f"File downloaded and saved in {path}")

    def _generate_overall_report(self, task_bot_paths):

        bot_path_list = []
        bot_name_list = []
        bot_lines = []
        bot_variable_number = []
        bot_packages_number = []
        bot_error_handling = []
        bot_loops = []
        bot_steps = []
        bot_comments = []
        bot_scripts = []
        bot_send_emails = []

        for file in task_bot_paths:
            index = re.search("\\Bots", file).start() - 1

            bot_path_list.append(file[index:])

            # Aquí entra en juego la segunda class (!!)
            analyze_bot = BotAnalyzer_A360(file)

            bot_name_list.append(analyze_bot.get_bot_name())
            bot_lines.append(analyze_bot.get_count_total_lines())
            bot_variable_number.append(analyze_bot.get_number_of_variables())
            bot_packages_number.append(analyze_bot.get_number_of_packages())
            bot_error_handling.append(analyze_bot.get_if_error_handling())
            bot_loops.append(analyze_bot.get_number_of_loops())
            bot_steps.append(analyze_bot.get_if_steps())
            bot_comments.append(analyze_bot.get_if_comments())
            bot_scripts.append(analyze_bot.get_if_scripts())
            bot_send_emails.append(analyze_bot.get_if_notification_emails())

        df_overall_report = pd.DataFrame({"Bot": bot_name_list,
                                          "Path": bot_path_list,
                                          "Lines": bot_lines,
                                          "Variables": bot_variable_number,
                                          "Packages": bot_packages_number,
                                          "Error Handling": bot_error_handling,
                                          "Loops": bot_loops,
                                          "Steps": bot_steps,
                                          "Comments": bot_comments,
                                          "Scripts": bot_scripts,
                                          "Email send": bot_send_emails
                                          })
        df_overall_report = df_overall_report.sort_values(by=['Lines'], ascending=False).reset_index(drop=True)

        df_overall_report["Complexity Estimation"] = df_overall_report.apply(lambda row: complexity_formula(row),
                                                                             axis=1)

        return df_overall_report

    def _generate_file_dependency_report(self, other_dependencies_paths):

        file_path_list = []
        file_name_list = []
        file_content_type = []

        for file in other_dependencies_paths:
            index = re.search("\\Bots", file["path"]).start() - 1

            file_path_list.append(file["path"][index:])

            file_name_list.append(file["path"].split("\\")[-1])

            file_content_type.append(file["mimeType"])

        df_dependencies_report = pd.DataFrame({"Name": file_name_list,
                                               "Path": file_path_list,
                                               "Content Type": file_content_type
                                               })
        df_dependencies_report = df_dependencies_report.sort_values(by=['Content Type'], ascending=False).reset_index(
            drop=True)

        return df_dependencies_report

    def _generate_variable_report(self, task_bot_paths):
        df_variable_list = pd.DataFrame(
            {"Bot_Name": [], "Name": [], "Type": [], "Description": [], "Input": [],
             "Output": []})

        for file in task_bot_paths:
            analyze_bot = BotAnalyzer_A360(file)
            df_variable_list = pd.concat([df_variable_list, analyze_bot.variable_df()])
        df_variable_list = df_variable_list.drop_duplicates()
        return df_variable_list

    def _generate_packages_report(self, task_bot_paths):
        df_packages = pd.DataFrame(
            {"bot_name": [], "package_name": [], "package_version": []})
        for file in task_bot_paths:
            analyze_bot = BotAnalyzer_A360(file)
            df_packages = pd.concat([df_packages, analyze_bot.packages_df()])
        df_packages = df_packages.drop_duplicates()
        return df_packages

    @staticmethod
    def get_task_bot_paths(manifest_json_path):
        # RETURN LIST WITH ABSOLUTE PATHS TO TASK BOT FILES
        with open(manifest_json_path) as f:
            manifest_json = json.load(f)

        task_bot_paths = []
        for file in manifest_json["files"]:
            if file["contentType"] == "application/vnd.aa.taskbot":
                task_bot_paths.append(os.path.join(os.path.dirname(manifest_json_path), file["path"]))

        return task_bot_paths

    @staticmethod
    def get_file_dependency_paths(manifest_json_path):
        # RETURN LIST WITH ABSOLUTE PATHS TO ALL DEPENDENCIES BUT TASK BOTS
        with open(manifest_json_path) as f:
            manifest_json = json.load(f)

        other_dependencies_path = []
        for file in manifest_json["files"]:
            if file["contentType"] != "application/vnd.aa.taskbot" and not file["metadataForFile"]:
                other_dependencies_path.append({"path": os.path.join(os.path.dirname(manifest_json_path), file["path"]),
                                                "mimeType": file["contentType"]})

        return other_dependencies_path
