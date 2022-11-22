from ReportGenerator import ReportGenerator
from functions import process_complexity
from functions import create_output_folder
import config as cfg

if __name__ == '__main__':

    print("Api key authentication")
    cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username,
                                  api_key=cfg.apiKey)
    # Create output folder if not present
    create_output_folder()

    df_dict = cr_instance.get_bot_full_reports("3788")

    # Save dataframes as csv:
    # 1) Task bots csv
    task_bot_file = f"output/test123_bots.csv"
    df_dict["bots"].to_csv(task_bot_file, index=False, encoding="utf-8")

    # 2) Other dependencies (scripts, config files, etc.) csv
    other_dependencies_file = f"output/test123_other_dependencies.csv"
    df_dict["other_dependencies"].to_csv(other_dependencies_file, index=False, encoding="utf-8")

    overall_complexity = process_complexity(df_dict["bots"])

    # 3) Variable csv
    variables_file = f"output/test123_variables.csv"
    df_dict["variable_list"].to_csv(variables_file, index=False, encoding="utf-8")

    # 4) Packages csv
    packages_file = f"output/test123_packages.csv"
    df_dict["packages"].to_csv(packages_file, index=False, encoding="utf-8")

    print("Overall complexity: " + str(overall_complexity))
    print(f"Task bots file saved in output folder as: test123_bots.csv")
    print(f"Other dependencies file saved in output folder as: test123_other_dependencies.csv")
    print(f"Other dependencies file saved in output folder as: test123_variables.csv")
