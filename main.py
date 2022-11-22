from argparse import ArgumentParser
from ReportGenerator import ReportGenerator
from functions import process_complexity
from functions import create_output_folder
import config as cfg

if __name__ == '__main__':
    DESCRIPTION = "This program will create some csv files within local output folder containing information about task " \
                  "bots " \
                  "and other dependency files. It is necessary that config.py file exists and contains the following " \
                  "variables:\n1)cr_url\n2)username\n3)apiKey OR password. Default method of authentication is " \
                  "via api key"

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--id", dest="bot_id", type=int,
                        help="Numeric bot id", required=True)

    parser.add_argument("--process_name", dest="process_name", type=str,
                        help="Process Name", required=True)

    parser.add_argument("--password", dest="password", help="Flag for password authentication (not recommended)",
                        action='store_true')
    args = parser.parse_args()

    if args.bot_id:
        if args.password:
            print("Password authentication")
            cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username,
                                          password=cfg.password)
        else:
            print("Api key authentication")
            cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username,
                                          api_key=cfg.apiKey)
        # Create output folder if not present
        create_output_folder()

        # Get dataframe list with all reports
        df_dict = cr_instance.get_bot_full_reports(str(args.bot_id))

        # Save dataframes as csv:
        # 1) Task bots
        task_bot_file = f"output/{args.process_name}_bots.csv"
        df_dict["bots"].to_csv(task_bot_file, index=False, encoding="utf-8")

        # 2) Other dependencies (scripts, config files, etc.)
        other_dependencies_file = f"output/{args.process_name}_other_dependencies.csv"
        df_dict["other_dependencies"].to_csv(other_dependencies_file, index=False, encoding="utf-8")

        overall_complexity = process_complexity(df_dict["bots"])

        # 3) Variable csv
        variables_file = f"output/{args.process_name}_variables.csv"
        df_dict["variable_list"].to_csv(variables_file, index=False, encoding="utf-8")

        # 4) Packages csv
        packages_file = f"output/{args.process_name}_packages.csv"
        df_dict["packages"].to_csv(packages_file, index=False, encoding="utf-8")

        print("Overall complexity: " + str(overall_complexity))
        print("Output csv files saved under outputs folder")
