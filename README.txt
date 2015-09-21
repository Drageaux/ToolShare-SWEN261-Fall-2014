
1) Installation
---------------

a. Extract the contents of the "mysite.zip" file into the folder of your choice



2) Known bugs and disclaimers
-----------------------------




3) Basic Executions
-------------------

a. Open the Command Prompt (This can be done by searching for "cmd" in the windows search bar, and selecting the program that is found.

b. Navigate ("cd" command) to the directory where the file manage.py is in and delete the file called "db.sqlite3"
	-For Example: If the absolute path to the project folder is 
		"C:\Users\Me\Documents\Project_Folder\mysite" 
	 then the command 
		"cd C:\Users\Me\Documents\Project_Folder\mysite" 
	 can be used to reach the project directory.

c. Type in and run the command "python manage.py syncdb" to create a database for the program. When prompted to create an admin account, input "no" without the quotation marks.

d. Type in and run the command "python manage.py runserver" to enable the local server.

e. Open a browser and go to the following url: "http://127.0.0.1:8000/home/" to access the site homepage.



4) Site Usage Instructions
--------------------------

The following describes what actions a typical user would perform when using the site:

a. User is redirected to the home page (login page)

b. Click "New User"

c. Fill in the fields with correct information

d. Click "Submit"

e. If information is filled in correctly the new user account is made and you are brought to a confirmation page. Click "Login"

f. You will be redirected to the login page, type in the credentials you just made and click "Submit".

e. You will be redirected to your profile page, from here you can see the tools you own as well as a drop down list of the tools you don't own and could borrow.

f. Click the "Create Tools" button at the top of the page. You will be redirected to the tool creation page.

g. Here you can type in the name of the tool, a description of it, input a model number, select a condition from the dropdown menu, as well as check a checkbox for if it is a power tool or not. After filling out the fields click "Register".

h. You will be redirected to the tool creation confirmation page, click "Return" to be redirected to your profile page.

i. Click "Other" at the top of the page and from the drop down list select the "Log Out" button.

j. You will now be logged out of your account and brought to the log out confirmation page. If you click the "Login" link, you will be redirected to the login page.