iTextBook Web App
================

iTextBook v1.0

julian kanjere <jkanjere@cs.uct.ac.za>

24 October 2012

_ Interactive Textbook Authoring and Learning Tool for Python Programming (iTextBook Python).The objective of iTextBook
Python project is two-fold: 
      
      i.To provide instructors(lecturers)with an easy to use platform for authoring, editing and  delivering online learning material.

      ii.To  provide studentswho  may  be  new  to  programming with a  platform  to  learn  and  test  their programming skills using learning material and practical assessments created by the instructor._


Getting Started:

- Create a new user account, nominally called "itextbook"
- Clone itextbook repo into /home/itextbook
- Update settings.py
- Add the rootcrons entries to the root's crontab for scheduled execution - $ crontab cron-file.txt
   (these prevent student programs from consuming too many server resources)
- Synchronise database
- Start the django server
- Create/update superuser and login to admin





Usage: 

- After successful login:
- Create a Course using Add Course then filling in the details and specifying the programming language.
- Add Topics to the course
- Add Subtopics (pdf slides, video, pdf textbook excerpt)
- Add Multiple Choice Questions to the Subtopic
- Add Coding Questions (question, 3 test cases, keywords)to the Subtopic
- Add Users by selecting users on menu and then add user
- Delete user from users page
- Make user admin from user page
- View Usage Analytics at Course/User Level
- View Subtopic Analytics for Multiple Choice Questions, Coding Questions and Comments
