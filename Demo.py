import pyodbc
import json
import requests
import os
import sys
import smtplib
import datetime
import time
from email.mime.text import MIMEText
from StringIO import StringIO

def sendEmail(fromm, to, subject, message):
    today = str(time.strftime("%m-%d-%y"))
    try:
        smtpObj = smtplib.SMTP('10.10.2.247')
        smtpObj.set_debuglevel(1)
        msg = MIMEText(message)
        sender = fromm
        receivers = to
        msg['Subject'] = "Stale Crash Events | " + today
        msg['From'] = sender
        smtpObj.sendmail(sender, receivers, msg.as_string())

        print "Successfully sent email: {}".format(subject)
    except Exception, e:
        print e
        print "Error: unable to send email"


# SERVER CREDENTIALS
server = '10.10.2.16,1432'
db ='sacars'
user ='sacars'
password ='sacars'

# CONNECT TO THE SERVER VIA THE ABOVE CREDENTIALS
conn = pyodbc.connect("DRIVER={/usr/local/lib/libmsodbcsql.13.dylib};SERVER=" + server + ';DATABASE=' + db +';UID=' + user + ';PWD=' + password)
cursor = conn.cursor()

# GET CRASHES OLDER THAN 8 HOURS VIA SQL
cursor.execute('SELECT sub.* FROM(SELECT situation_id, update_number, update_timestamp, situation_update_json FROM (SELECT *, maxnum = MAX(update_number) OVER (PARTITION BY situation_id) FROM [SACARS].[dbo].[evt_Situations]) as s WHERE update_number = maxnum) sub WHERE situation_update_json LIKE \'%"headline":{\"category\":2%\' AND update_timestamp < DATEADD(hh, -11, GETDATE()) AND situation_update_json NOT LIKE \'%DELETE%\' AND situation_update_json NOT LIKE \'%ENDED%\'')

# FETCH ALL DATA FROM THE SQL QUERY AND PRINT IT
allEventsJson = cursor.fetchall()
numberOfEvents = len(allEventsJson)
print '\n' + 'Events In The Database: ' + str(numberOfEvents)

crashEventIDs = []
for item in allEventsJson:
        crashEventIDs.append(item[0])
print 'The number of crash items in need of review: ' + str(len(crashEventIDs))

# SEND EMAIL
if numberOfEvents > 0:
        emailString = 'Hello,' + '\n' + '\n' + 'The following Crash Events in Sacog Staging are older than 8 hours: ' + '\n' + '\n'
        for item in crashEventIDs:
                emailString = emailString + str(item) + '\n'
        emailString = emailString + '\n' + '\n' + 'Best regards,' + '\n' + '\n' + 'Castle Rock QA Robot'

if emailString != '':
        Message = emailString
        Subject = 'Test Email'
        From = 'ryan.kavanaugh@crc-corp.com'
        To = ['ryan.kavanaugh@crc-corp.com', 'lauren.jenkins@crc-corp.com']  # 'mary.crowe@crc-corp.com',
        print emailString
        sendEmail(From, To, Subject, Message)







deleteCounter = 0
itemsInIDList = len(crashEventIDs)











# # # Deletes first item in ID list
# # url = 'http://cramgmt.carsprogram.int/deleteEvent/deleteEvent.php?platform=Staging&state=SACOG&eID=' + str(crashEventIDs[0]) + '&mode=Delete'
# # print url
# # r = requests.get(url)
# # print r.status_code
# #
# # Deletes events in loop
# for id in crashEventIDs:
#     if deleteCounter < itemsInIDList:
#         url = 'http://cramgmt.carsprogram.int/deleteEvent/deleteEvent.php?platform=Staging&state=SACOG&eID=' + str(crashEventIDs[deleteCounter]) + '&mode=Delete'
#         print url
#         r = requests.get(url)
#         print r.status_code
#         #deleteCounter += 1