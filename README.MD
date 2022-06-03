# A360 Bot Analyzer

# Description
**This program is oriented ONLY for unattended bot runners. For attended bot runners (AARI Desktop/AARI Web) estimates are made differently**
With the aim of estimating the complexity of a process, this program takes as input the bot id of a bot (**within public folder**) and returns a dataframe with information
about the bot and all its dependencies as well as each bot complexity estimation (0<complexity<1).

On top of that this program returns an overall process complexity estimation, taking into consideration the number of bots involved

This program gives a first picture of a process. However more variables shall be considered to estimate the complexity, these are:

* Does the process use any triggers?
* Does the process use Workload Management (queues)
* What is the retry logic of the process?
* Any kind of reporting?
* In how many VMs is this process executed?
* If process is attended (AARI Desktop/Web) then another approach shall be taken

For example, inserting the bot id from this url https://aa1-app2019.iacc.epam.com/#/bots/repository/public/taskbots/3669/view
we obtain: 

| Bot                                     | Path                                                                   |   Lines |   Variables |   Packages | Error Handling   | Loops   | Steps   | Comments   | Scripts   | Email send   |   Complexity |
|:----------------------------------------|:-----------------------------------------------------------------------|--------:|------------:|-----------:|:-----------------|:--------|:--------|:-----------|:----------|:-------------|-------------:|
| Main - Signium                          | Bots\A360_Framework\Main\Main - Signium                                |     200 |          27 |         18 | True             | True    | True    | True       | False     | True         |     0.9275   |
| xx - SAP open and login                 | Bots\A360_Framework\Child Bots\xx - SAP open and login                 |      73 |          19 |         42 | True             | False   | True    | True       | True      | True         |     0.8935   |
| Create Bot Folders                      | Bots\A360_Framework\Framework\Create Bot Folders                       |      60 |          15 |         26 | True             | False   | True    | True       | False     | False        |     0.844167 |
| Process Item                            | Bots\A360_Framework\Framework\Process Item                             |      58 |          12 |         11 | True             | False   | True    | True       | False     | False        |     0.782667 |
| Read Config File                        | Bots\A360_Framework\Framework\Read Config File                         |      48 |           7 |         12 | True             | False   | True    | True       | False     | False        |     0.7535   |
| End process                             | Bots\A360_Framework\Framework\End process                              |      46 |          15 |         18 | True             | True    | True    | True       | False     | True         |     0.7895   |
| Init                                    | Bots\A360_Framework\Framework\Init                                     |      45 |           7 |         14 | True             | True    | True    | True       | False     | False        |     0.754167 |
| Delete Old Files                        | Bots\A360_Framework\Framework\Delete Old Files                         |      43 |           8 |         16 | True             | True    | True    | True       | False     | False        |     0.759333 |
| xx - Write a NOTE within person JOURNAL | Bots\A360_Framework\Child Bots\xx - Write a NOTE within person JOURNAL |      33 |          13 |         14 | True             | False   | True    | True       | False     | False        |     0.745167 |

**Overall complexity**
**0.5935**

# Usage
As mentioned for executing this program you will need:

* A360 Control Room user with appropriate permissions for exporting bots
* A360 Control Room username and password/apiKey (it works with both)
* Access to the Control Room so that you can get the bot id from the Public folder
* You only need to point to the Master/Main bot. All dependencies are automatically detected and added

# Dependencies
This code has been developed using Python 3.10.1. Requirements are located in the requirements.txt file

# Author
Andoni Aguirre Aranguren

# Contact
[![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/aaguirrearanguren)
[![GitHub](https://i.stack.imgur.com/tskMh.png) GitHub](https://github.com/aagirre92)