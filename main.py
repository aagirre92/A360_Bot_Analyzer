from ReportGenerator import ReportGenerator
import config as cfg

if __name__ == '__main__':
    cr_instance = ReportGenerator(cfg.cr_url, cfg.username, cfg.apiKey)
    df = cr_instance.get_bot_full_reports("3669")
    print(df)

