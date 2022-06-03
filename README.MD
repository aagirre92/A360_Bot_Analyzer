# A360 Bot Analyzer

# Description
With the aim of estimating the complexity of a process, this program takes as input the bot id of a bot (**within public folder**) and returns a dataframe with information
about the bot and all its dependencies.

For example, inserting the bot id from this url https://aa1-app2019.iacc.epam.com/#/bots/repository/public/taskbots/3669/view
we obtain: 

| Bot                 | Path                                                                  |   Lines |   Variables |   Packages |
|:--------------------|:----------------------------------------------------------------------|--------:|------------:|-----------:|
| Get_Data_From_Radar | Bots\Opportunities and Projects report automation\Get_Data_From_Radar |     131 |          31 |         13 |
| Tests               | Bots\Opportunities and Projects report automation\Tests               |       7 |           7 |          8 |
| Send_Email          | Bots\Opportunities and Projects report automation\Send_Email          |       6 |           8 |          5 |
| Init                | Bots\Opportunities and Projects report automation\Init                |       6 |           4 |          6 |
| Main_Radar          | Bots\Opportunities and Projects report automation\Main_Radar          |       4 |           3 |          1 |

# Dependencies
This code has been developed using Python 3.10.1. Requirements are located in the requirements.txt file