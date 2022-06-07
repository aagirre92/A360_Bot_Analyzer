from ReportGenerator import ReportGenerator
from functions import process_complexity
import config as cfg

if __name__ == '__main__':
    # cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username, api_key=cfg.apiKey)
    cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username_support_user,
                                  api_key=cfg.apiKey_support_user)

    df_dict = cr_instance.get_bot_full_reports("3669")

    # Save dataframes as csv:
    # 1) Task bots
    df_dict["bots"].to_csv("output/ProcessName_bots.csv", index=False, encoding="utf-8")

    # 2) Other dependencies (scripts, config files, etc.)
    df_dict["other_dependencies"].to_csv("output/ProcessName_other_dependencies.csv", index=False, encoding="utf-8")

    overall_complexity = process_complexity(df_dict["bots"])

    print("Overall complexity: " + str(overall_complexity))
