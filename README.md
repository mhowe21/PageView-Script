# PageView-Script
This is an old Ad-Hoc script that was written for a one-off project. It should pull the page views of users over the course of specified dates and output a csv file for each user. As this was never intended for anything other than ad-hoc use it will likely not be maintained going forward. 

Prerequisites: 
You will need to have the latest version of Python 3 with pip installed. You can download that here. https://www.python.org/downloads/
The program will attempt to install the requests nonstandard library if you do not already have it. to install manually type python -m pip install requests from your terminal. 
The program will also attempt to install the pandas library if you do not already have it installed. To install manually type python -m pip install pandas from your terminal. 

Usage. 
The script will ask you for a canvas instance to target. You will want to input the sub domain and domain (example: instance.instructure.com)
The script will then ask you for your rest token. You will need to have sufficient privileges to view pages views. You can find how to generate a token here https://community.canvaslms.com/docs/DOC-14409-4214861717. 
The script will then ask you for a list of users separated by commas. These are the users canvas IDs not SIS IDs. (example: 20,21,23,25)
The script will then prompt for a start date and end date. You can leave these blank if you want to gather all page views present for a user (depending on how many there are this may take some time.) or you can enter a time frame in a yyyy-mm-dd format (example 2017-01-01)

Please note that at the current time the output files will be placed in the current working directory.




