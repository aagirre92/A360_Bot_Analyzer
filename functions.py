def complexity_formula(row):
    """
    This function is used for calculating the complexity of each task bot
    :param row:
    :return: Float
    """
    COEF_LINES = 0.2
    COEF_VARIABLES = 0.1
    COEF_PACKAGES = 0.1
    COEF_ERR = 0.1
    COEF_LOOPS = 0.1
    COEF_STEPS = 0.05
    COEF_COMMENTS = 0.15
    COEF_SCRIPTS = 0.15
    COEF_EMAILS = 0.05

    lines = row["Lines"]
    variables = row["Variables"]
    packages = row["Packages"]

    if lines == 0:
        x_lines = 0
    elif 0 < lines < 100:
        x_lines = lines / 100
    else:
        x_lines = 1

    if variables == 0:
        x_variables = 0
    elif 0 < variables < 40:
        x_variables = variables / 40
    else:
        x_variables = 1

    if packages == 0:
        x_packages = 0
    elif 0 < packages < 30:
        x_packages = packages / 30
    else:
        x_packages = 1

    if row["Error Handling"]:
        x_error_handling = COEF_ERR
    else:
        x_error_handling = 0

    if row["Loops"]:
        x_loops = COEF_LOOPS

    else:
        x_loops = 0

    if not row["Steps"]:
        x_steps = COEF_STEPS
    else:
        x_steps = 0

    if not row["Comments"]:
        x_comments = COEF_COMMENTS
    else:
        x_comments = 0

    if row["Scripts"]:
        x_scripts = COEF_SCRIPTS
    else:
        x_scripts = 0

    if row["Email send"]:
        x_email_notifications = COEF_EMAILS
    else:
        x_email_notifications = 0

    y = COEF_LINES * x_lines + COEF_VARIABLES * x_variables + COEF_PACKAGES * x_packages + x_error_handling + x_loops + x_steps + x_comments + x_scripts + x_email_notifications

    return y


def process_complexity(df):
    """
    Calculates process overall complexity, taking into consideration how many bots are involved
    :param df: DataFrame
    :return: Float
    """
    complexity_max = df["Complexity Estimation"].max()
    overall_complexity = 0
    if len(df) > 10:
        overall_complexity = complexity_max * 1.5
        if overall_complexity > 1:
            overall_complexity = 1
    elif len(df) < 10:
        overall_complexity = complexity_max

    return overall_complexity
