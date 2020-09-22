from datetime import datetime
import calendar
import requests
import decimal
from json import dumps

# Getting the project billing dates from servers 
d = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume', params = {'function':"get-billing-date"})
project = d.json()
print(project)
project = {int(k):v for k,v in project.items()}
# After this put everything inside while loop to 1 ) monitor the bills generation 2 ) Generate bills in billing table 3 ) generate the csv of all residents
# bill details for the last month at admin level and 4 ) generate the pdf containing bill details of the residents for last month at admin level. The content stays
# the same for both csv and pdf but it's just that they get it in two formats.

# to check if project date has arrived or not and then if it matches then calculate the bills and files using the flow as in the code.
a = datetime.now()
if a.month == 1:
    year = a.year-1
    month = 12
else:
    year = a.year
    month = a.month-1
if month<10:
    month = '0'+str(month)
else:
    pass
start_date = str(year)+"-"+str(month)+"-01"
end_date = str(year)+"-"+str(month)+ "-"+str(calendar.monthrange(year, int(month))[1])
print(start_date,end_date)
if a.day in project.keys():
    total = 0
    for i in range(len(project[a.day])):
        r = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume', params = {'project':project[a.day][i],'function':"wings-list"}) 
        data = r.json()
        for j in data['wings']:
            q = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',
                             params = {'project':project[a.day][i],'function':"flat-list",'wing':j})
            flats = q.json()
            for k in flats['flats']:
                t = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project[a.day][i],'start':start_date,'end':end_date,'function':'bill-api-with-minimum','wing':j,'flat':k})
                bill = t.json()
                #print(bill['results']['bill_for_duration'],bill['results']['flat'])
                pload = {'wing':j,'flat':k,'month':month,'year':year,'consumption':bill['results']['total_consumption'],'duration':start_date+" to " +end_date,
                         'charges':bill['results']['usage_charges'],'tax':bill['results']['tax'],
                'id':str(project[a.day][i])+str(j)+str(k)+'-'+str(month)+"-"+str(year),'project':str(project[a.day][i]),'amount':bill['results']['bill_for_duration']}
                r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=generate-bills',data=dumps(pload))
                total = total + int(bill['results']['bill_for_duration'])
                print(r.json())
        g = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',
                         params = {'project':project[a.day][i],'function':"upload-csv",'month':month,'year':year})
        excel_response = g.json()
        print(excel_response)
        h = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',
                         params = {'project':project[a.day][i],'function':"upload-pdf",'month':month,'year':year,'total':total})
        pdf_response = h.json()
        print(pdf_response)
                
                
            
        
        
        
        

