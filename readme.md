iTextBook Web App
================

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

- Create assignments in the Assignments tool in Sakai.


- For each assignment, when the owner of the logs into the automatic marker,
they can "Edit" the assignment's marking scripts. Click on the
help link for more information or see the "sample_site_data" directory.

