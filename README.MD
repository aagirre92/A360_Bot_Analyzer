# A360 Bot Analyzer

# Description
**This program is oriented ONLY for unattended bot runners. For attended bot runners (AARI Desktop/AARI Web) estimates are made differently**
With the aim of estimating the complexity of a process, this program takes as input the bot id of a bot (**within public folder**) and returns a dataframe with information
about the bot and all its dependencies as well as each bot complexity estimation (0<complexity<1).

On top of that this program returns an overall process complexity estimation, taking into consideration the number of bots involved

This program gives a first picture of a process. **However, more variables shall be considered to estimate the complexity, these are:**

* Does the process use any triggers?
* Does the process use Workload Management (queues)
* What is the retry logic of the process?
* Any kind of reporting?
* In how many VMs is this process executed?
* If process is attended (AARI Desktop/Web) then another approach shall be taken

> For example, inserting the bot id from this url  https://aa1-app2019.iacc.epam.com/#/bots/repository/public/taskbots/3669/view
we obtain: 
>> **NOTE THAT ONLY ACTIVE ACTIONS ARE COUNTED (PROGRAM DOES NOT TAKE INTO CONSIDERATION DISABLED ACTIONS)**
## Task bots
| Bot                                     | Path                                                                   |   Lines |   Variables |   Packages | Error Handling   |   Loops | Steps   | Comments   | Scripts   | Email send   |   Complexity Estimation |
|:----------------------------------------|:-----------------------------------------------------------------------|--------:|------------:|-----------:|:-----------------|--------:|:--------|:-----------|:----------|:-------------|------------------------:|
| Main - Signium                          | Bots\A360_Framework\Main\Main - Signium                                |     198 |          27 |         18 | True             |       3 | True    | True       | False     | True         |                0.5775   |
| xx - SAP open and login                 | Bots\A360_Framework\Child Bots\xx - SAP open and login                 |      71 |          19 |         42 | True             |       0 | True    | True       | True      | True         |                0.5895   |
| Create Bot Folders                      | Bots\A360_Framework\Framework\Create Bot Folders                       |      60 |          15 |         26 | True             |       0 | True    | True       | False     | False        |                0.344167 |
| Process Item                            | Bots\A360_Framework\Framework\Process Item                             |      54 |          12 |         11 | True             |       0 | True    | True       | False     | False        |                0.274667 |
| Read Config File                        | Bots\A360_Framework\Framework\Read Config File                         |      48 |           7 |         12 | True             |       0 | True    | True       | False     | False        |                0.2535   |
| End process                             | Bots\A360_Framework\Framework\End process                              |      45 |          15 |         18 | True             |       2 | True    | True       | False     | True         |                0.4375   |
| Delete Old Files                        | Bots\A360_Framework\Framework\Delete Old Files                         |      43 |           8 |         16 | True             |       5 | True    | True       | False     | False        |                0.359333 |
| Init                                    | Bots\A360_Framework\Framework\Init                                     |      42 |           7 |         14 | True             |       3 | True    | True       | False     | False        |                0.348167 |
| xx - Write a NOTE within person JOURNAL | Bots\A360_Framework\Child Bots\xx - Write a NOTE within person JOURNAL |      32 |          13 |         14 | True             |       0 | True    | True       | False     | False        |                0.243167 |

**Overall complexity**
**0.5935**

## Other dependencies but task bots

| Name                         | Path                                                             | Content Type             |
|:-----------------------------|:-----------------------------------------------------------------|:-------------------------|
| config.xml                   | Bots\A360_Framework\Files\config.xml                             | text/xml                 |
| readme.txt                   | Bots\A360_Framework\readme.txt                                   | text/plain               |
| Procedures_and_Functions.vbs | Bots\A360_Framework\SAP VBS Scripts\Procedures_and_Functions.vbs | application/octet-stream |

# Usage
As mentioned for executing this program you will need:
* **config.py** file is used for storing the sensitive variables such as username, password/apikey and control room url
* A360 Control Room user with appropriate permissions for exporting bots. At least user should have these permissions:
  * BOTS
    * View my bots
      * Export Bots
  * API
    * Generate API-Key
  * Permission to view content of public Bots folder (or specific folders within)
  
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