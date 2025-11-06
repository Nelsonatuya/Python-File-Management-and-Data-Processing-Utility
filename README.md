# Python-File-Management-and-Data-Processing-Utility
Python File Management and Data Processing Utility

Purpose:
Simple utility to create, back up, organize, log, and analyze student data files.

Features:

Initialize project folder: StudentFiles
Create daily student record files (records_YYYY-MM-DD.txt)
Display file contents and metadata (size, last modified)
Create backup copies and move them to StudentFiles/Archive
Append activity and error logs to activity_log.txt
Prompt to delete files from StudentFiles and log deletions
Generate CSV report from students.json (report.csv)
How to run:

Open a terminal in the project folder (c:\Users\User\Desktop\python\filemanagement).
Run the main utility:
python file_manager.py
Follow prompts to enter 5 student names.
Creates StudentFiles/records_YYYY-MM-DD.txt, backs it up to StudentFiles/Archive/, and logs actions in StudentFiles/activity_log.txt.
Generate CSV report from JSON:
python students_report.py
If students.json is missing, the script can prompt to create it with 5 students.
Output: report.csv
Where outputs live:

StudentFiles/ — contains records, backups, Archive, activity_log.txt, students.json, report.csv