# Python Coronavirus and News Dashboard - Alex Gulliver
## **INTRODUCTION**
 
 This is a university programming project designed to provide an interface where coronavirus figures from England and Exeter are shown and are able to be updated at set scheduled times. There is also a news section which sorts by set keywords for coronavirus news and posts them on the side on toast widgets. 

 GITHUB LINK:

 https://github.com/AlexGulliver/ECM1400Project

---

## **PREREQUISITES** 
Before running the code please ensure the following modules are installed and the correct version of Python is being used. 
### **Python 3.9.9**


    INSTALLATION
    Enter the following into the command line:
    pip install flask
    pip install pytest

---
## **GETTING STARTED**

To run the program, you must first enter in your API key into the news section of the config file. Then, launch the flask_interface module to launch the server and enter: http://127.0.0.1:5000/ into your browser. 

From here you will be able to see the interface. The centre shows all the data collected from the API. Towards the bottom, there are controls to allow you to set a time (repeating for the next day if ticked) and whether you would like to update the covid data, the news articles or both. 

Finally, either side you can remove scheduled events or news articles. News articles that are deleted will be placed on a blacklist and will never be seen again.

---
## **TESTING**

To conduct testing on the program, launch the cmd and make sure you are in the right directory. Then simply type in pytest. There are seperate testing module for each module that has been coded. 

---
## **DEVELOPER DOCUMENTATION**

This program consists of 5 main modules. Also included is the html template, sample csv file, news blacklist file, config file and logging file. 

---

### *flask_interface*

The flask_interface provides the main functionality for the interface.  

Code runthrough (LINE NUMBERS):

Firstly the schedulers are initialised with seperate ones for the news and covid updates. (19-23)

The config file is opened and the variable "key" is assigened to the API key for the NewsAPI. The country is also set here. (26-31)

Logging initalised. (33)

The actual request then takes place and is stored in the "data" variable. (35) 

News article list is initalised (37)

Toast widget lists are initalised here (38)

### FUNCTIONS:

    initial_news_articles -> returns Any
    This function is loaded when the program is launched so that news articles appear when the interface is accessed. It takes the formatted data (which is a tuple of two lists, the first one being the news article titles and the second being their corresponding content) and checks that they aren't in the blacklist file before appending them to the news list. This creates a news list of dictionaries. So each index in the list corresponds to an article. This article is a dictionary with a "title" and "content" key.

    update_news -> returns None
    This function is used to update the news articles and is called by the scheduler. A list is initialised (current_news_titles) and the news titles being displayed are appended to it. It then calls the NewsAPI again to get the most recent selection of articles and checks they aren't in the blacklist file or were already being displayed before appending the remaining articles to the news list.

    update_covid -> returns None
    This function is used for updating the covid figures. It calls the API and overwrites the current figures.

    schedule_covid_updates -> returns sched.Event
    This function takes two arguments: update_interval : int and update_name : str. It enters an update into the covid_schedule scheduler and returns it. 

    schedule_news_update -> returns sched.Event
    This function takes two arguments: update_interval : int and update_name : str. It enters an update into the news_schedule scheduler and returns it.

    check_repeat -> returns Any
    This function takes a request to see if the user has clicked the tickbox to show they want repeated updates for their scheduler update and returns a Boolean.

    check_covid -> returns Any
    This function takes a request to see if the user has clicked the tickbox to show they want covid updates for their scheduler update and returns a Boolean.

    check_news -> returns Any
    This function takes a request to see if the user has clicked the tickbox to show they want repeated news for their scheduler update and returns a Boolean.

    schedule_add_toast -> returns Any
    This function checks to see if anything has been inputted into the label and will evaluate what to do with the users inputs. There are four possible combinations of tickbox ticking (not including no entries) which are all accounted for. The function takes the arguments up_time: int, up_label: str, new_covid: Any, new_news: Any, will_repeat: Any. up_time tells the function how long until the next update. up_label is the label entered by the user. new_covid, new_news and will_repeat are where the check_covid, check_news and check_repeat functions are used respectively. Their values determine how the function will behave and what it will subsequently schedule. 

    delete_schedule_toast -> returns None
    This function provides functionality to allow the user to delete schedule toasts. It works by getting the request when a user clicks on the x button and comparing the title with the titles of the schedule toasts currently being shown. The one that matches is then removed from the list and will disappear from the interface.

    delete_news_toast -> returns list
    This function has the same purpose as the above but also writes the title of the news article to a blacklist file so it will never be shown again after being deleted.

    redirection
    This function redirects the user so they don't have to manually enter /index after every time they launch.

    hello
    This is the main interface functionality of the code. It reads covid data from a file and then returns a template which maps to the html.

---

### *covid_news_handling*

The covid_news_handling module pulls news articles from the NewsAPI and formats them for use in the interface.

Code runthrough (LINE NUMBERS):

Article title list and article description list initalised (11-12)

Logging initialised (14)

Config file opened (16-21)

### FUNCTIONS:

    news_API_request -> returns tuple
    This function takes the arguments: config_key: str, country_setting: str, covid_terms=["Covid", "COVID-19", "coronavirus"]. The first two arguments are pulled from the config. The function takes the top headlines from the news api and formats the response into a tuple of two lists. The first list being a list of news article titles and the second being their corresponding (by index) contents.

    update_news -> tuple
    Used in scheduler to update the news articles

---

### *uk_covid_api_request*

The uk_covid_api_request module pulls covid data from the NHS and formats it for use in the interface. 

Code runthrough (LINE NUMBERS):

covid_figures dictionary initalised (11)

Logging initialised (13)

Unique area dictionary structures initialised (15-28)

The structure for how data from the API is to be returned is initalised (30-38)

Release timestamp found for logging (42)

### FUNCTIONS:

    covid_api_request -> returns dictionary
    Takes arguments: location_type: str='ltla', location: str='Exeter' with default location. Calls the covid 19 api and uses the filters to format the data and return it as a dictionary for use. 

    process_data_weekly_infections -> returns Any
    Takes the data and works out the number of weekly infections by getting the last 7 days worth of daily infections and summing them. Skips the first day due to incomplete results. 

    process_data_hospital -> returns any
    Takes data and retrieves the culmulative number of deaths from the most recent day

    covid_data_to_file -> returns None
    Writes the covid information shown on the interface to a file to allow for easy updating. When a scheduled update occurs, the file is wiped and reloaded with new data which is then read again.

---

### *covid_data_handler*

The covid_data_handler is used for static csv files. 

Code runthrough (LINE NUMBERS):

Scheduler initalised (10)

### FUNCTIONS:

    parse_csv_data -> returns list
    Converts the csv file to a list. Skips first row as it is a title line. 

    process_covid_csv_data -> returns tuple
    Goes through the list from the parsed csv data and works out the values for the last 7 days of cases, hospital cases and culmulative deaths. 

---

### *time_conversions*

The time conversions module contains useful conversions. They are used in the schedulers. 

Code runthrough (LINE NUMBERS):

### FUNCTIONS:

    minutes_to_seconds -> returns int
    Converts mins to seconds

    hours_to_minutes -> returns int
    Converts hours to minutes

    hhmm_to_seconds -> returns int
    Converts hhmm format to seconds

## OTHER FILES

The sys.txt file contains all the logging information. ERROR messages signify something has gone critically wrong whilst info messages are used for debugging and show routine. 

The config json file can be used to easily add in your API keys and change the country for the figures. 

The deleted_news file is a blacklist for all deleted news articles. 

The tests folder contains all the tests. 


---
## **DETAILS**

@Author: Alex Gulliver

Updated: 10/12/21

---

Acknowledgements:

Dr Matt Collison

https://emps.exeter.ac.uk/computer-science/staff/mmc212

Dr Hugo Barbosa

https://emps.exeter.ac.uk/computer-science/staff/hs613

---

https://choosealicense.com/licenses/mit/

MIT License

Copyright (c) [2021] [Alex Gulliver]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."# ECM1400Project" 
"# ECM1400Project" 
