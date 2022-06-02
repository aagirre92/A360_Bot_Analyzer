# A360 Bot Analyzer

# Description
With the aim of estimating the complexity of a process, this program takes as input the bot id of a bot (**within public folder**) and returns a dataframe with information
about the bot and all its dependencies.

For example, inserting the bot id from this url https://aa1-app2019.iacc.epam.com/#/bots/repository/public/taskbots/3669/view
we obtain: 

| Bot                                     |   Lines |   Variables |   Packages |
|:----------------------------------------|--------:|------------:|-----------:|
| Main - Signium                          |     200 |          27 |         18 |
| xx - SAP open and login                 |      73 |          19 |         42 |
| Create Bot Folders                      |      60 |          15 |         26 |
| Process Item                            |      58 |          12 |         11 |
| Read Config File                        |      48 |           7 |         12 |
| End process                             |      46 |          15 |         18 |
| Init                                    |      45 |           7 |         14 |
| Delete Old Files                        |      43 |           8 |         16 |
| xx - Write a NOTE within person JOURNAL |      33 |          13 |         14 |

# Dependencies
This code has been developed using Python 3.10.1. Requirements are located in the requirements.txt file