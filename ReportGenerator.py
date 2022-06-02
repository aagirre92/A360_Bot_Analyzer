import os
import requests
from datetime import datetime
import json
import tempfile
import zipfile
import pandas as pd


from BotAnalyzer_A360 import BotAnalyzer_A360


class ReportGenerator:

    def __init__(self, control_room_url, user, api_key):

        self.user = user

        self.api_key = api_key

        if control_room_url[-1] == "/":
            self.control_room_url = control_room_url[:-1]

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

        # reports_dict = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            self._download_file(export_id, temp_dir)
            task_bot_paths = ReportGenerator.get_task_bot_paths(os.path.join(temp_dir, "manifest.json"))

            df_overall_report = self._generate_overall_report(temp_dir, task_bot_paths)

            # reports_dict["overall_report"] = df_overall_report

            return df_overall_report

    # PRIVATE METHODS

    def _get_token(self):

        uri = f"{self.control_room_url}/v1/authentication"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "username": self.user,
            "apiKey": self.api_key
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

        print(f"File downloaded and saved in {path}")

    def _generate_overall_report(self, path, task_bot_paths):
        bot_name_list = []
        bot_lines = []
        bot_variable_number = []
        bot_packages_number = []
        for file in task_bot_paths:
            # Aquí entra en juego la segunda class (!!)
            analyze_bot = BotAnalyzer_A360(file)
            bot_name_list.append(analyze_bot.get_bot_name())
            bot_lines.append(analyze_bot.get_count_total_lines())
            bot_variable_number.append(analyze_bot.get_number_of_variables())
            bot_packages_number.append(analyze_bot.get_number_of_packages())

        df_overall_report = pd.DataFrame({"Bot": bot_name_list, "Lines": bot_lines, "Variables": bot_variable_number,
                                          "Packages": bot_packages_number})
        df_overall_report = df_overall_report.sort_values(by=['Lines'], ascending=False).reset_index(drop=True)
        return df_overall_report

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
