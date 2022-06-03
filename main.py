from ReportGenerator import ReportGenerator
from functions import process_complexity
import config as cfg

if __name__ == '__main__':
    cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username, api_key=cfg.apiKey)
    # cr_instance = ReportGenerator(control_room_url=cfg.cr_url, username=cfg.username, password=cfg.password)
    df = cr_instance.get_bot_full_reports("3669")
    overall_complexity = process_complexity(df)
    print("Overall complexity: "+str(overall_complexity))

