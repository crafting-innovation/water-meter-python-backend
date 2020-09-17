import json,boto3
from datetime import datetime , timedelta, date
from boto3.dynamodb.conditions import Key,Attr
import decimal
import time
import requests
import csv
import botocore
import calendar
from json import dumps
from fpdf import FPDF
# Design get and post methods for all six services to show data
# from db and post data to db from sensor endpoints 
# Post request will have IAM roles None in API gateway
# Get requets will have IAM roles enabled in API gateway
# helper class to format data received from querying dynamo_db
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def water_meter_update_db(event):
    try:
        a = eval(event["body"])
        device_id = a["device_id"]
        consumption = a["consumption"]
        project = a["project"]
        timestamp = a["timestamp"]
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('dev-water-meter-python-backend')
        response = table.put_item(Item={'device_id':device_id,'timestamp':timestamp ,'consumption':consumption,'project':project})
        return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        return {'statusCode':400,'body':json.dumps(str(e)),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_update_db(event):
    try:
        a = eval(event["body"])
        sprinkler_id = a["sprinkler_id"]
        consumption = a["consumption"]
        project = a["project"]
        timestamp = a["timestamp"]
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('sprinkler_consumption')
        response = table.put_item(Item={'sprinkler_id':sprinkler_id,'timestamp':timestamp ,'consumption':consumption,'project':project})
        return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        return {'statusCode':400,'body':json.dumps(str(e)),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
   
def insert_meter_card(event):
    a = eval(event["body"])
    project  = a["project"]
    types = a['types']
    tax = a['tax']
    minimum = a['minimum']
    cpl_slab_1 = str(a['cpl_1'])
    cpl_slab_2 = str(a['cpl_2'])
    cpl_slab_3 = str(a['cpl_3'])
    cpl_slab_4 = str(a['cpl_4'])
    cpl_slab_5 = str(a['cpl_5'])
    slab1_limit = a['slab1_limit']
    slab1_rate = str(a['slab1_rate'])
    slab2_limit = a['slab2_limit']
    slab2_rate = str(a['slab2_rate'])
    slab3_limit = a['slab3_limit']
    slab3_rate = str(a['slab3_rate'])
    slab4_limit = a['slab4_limit']
    slab4_rate = str(a['slab4_rate'])
    slab5_rate = str(a['slab5_rate'])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('meter_card')
    try:
        response = table.put_item(Item={'project': project,'types': types,'tax': tax,'minimum':minimum,'cpl':[decimal.Decimal(cpl_slab_1),decimal.Decimal(cpl_slab_2),decimal.Decimal(cpl_slab_3),decimal.Decimal(cpl_slab_4),decimal.Decimal(cpl_slab_5)],'slab1':{'ranges':[0,slab1_limit],'rate':decimal.Decimal(slab1_rate)},'slab2':{'ranges':[slab1_limit+1,slab2_limit],'rate':decimal.Decimal(slab2_rate)},'slab3':{'ranges':[slab2_limit+1,slab3_limit],'rate':decimal.Decimal(slab3_rate)},'slab4':{'ranges':[slab3_limit+1,slab4_limit],'rate':decimal.Decimal(slab4_rate)},'slab5':{'ranges':[slab4_limit+1],'rate':decimal.Decimal(slab5_rate)}})
        return {'statusCode':200,'body':json.dumps("updated successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("error occured"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    
def insert_user_valve(event):
    a = eval(event["body"])
    wing  = a["wing"]
    flat = a['flat']
    kitchen = a['kitchen']
    bath1 = a['bath1']
    bath2 = a['bath2']
    bath3 = a['bath3']
    misc = a['misc']
    monthly_limit = a['limit']
    project = a['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    try:
        response = table.put_item(Item={'wing': wing,'flat': flat,'kitchen': {'id':kitchen,'statuss':decimal.Decimal(1)},'bathroom1':{'id':bath1,'statuss':decimal.Decimal(0)},'bathroom2':{'id':bath2,'statuss':decimal.Decimal(0)},'bathroom3':{'id':bath3,'statuss':decimal.Decimal(0)},'misc':{'id':misc,'statuss':decimal.Decimal(0)},'project':project,'limit':monthly_limit})
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("Error Occured"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}} 

def insert_rfid_data(event):
    a = eval(event["body"])
    #flat is combination of wing anf flat i.e W1101
    flat = a["flat"]
    vehicle_no = a["vehicle_no"]
    types = a["type"]
    brand = a["brand"]
    model = a["model"]
    rfid = a["rfid"]
    project = a["project"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    try:
        response = table.put_item(Item={'flat':flat,'vehicle_no':vehicle_no ,'types':types ,'brand':brand,'model':model,'rfid':rfid,'project':project})
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("Error Occured"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def insert_rfid_in_out_data(event):
    a = eval(event["body"])
    rfid = a["rfid"]
    timestamp = a['timestamp']
    types = a["type"]
    project= a["project"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_data')
    try:
        response = table.put_item(Item={'rfid':rfid,'timestamp':timestamp ,'types':types,'project':project})
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("Error Occured"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def user_valve_control(event):
    # test pending by craeting a post request in python 
    # update valve status for particular wing and flat and area
    a = eval(event["body"])
    wing_selected = a["wing"]
    flat_selected = a["flat"]
    area_selected = a["area"]
    status = int(a["status"])
    string = "set "+str(area_selected)+".statuss = :s"
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    try:
        response = table.update_item(Key={'wing': wing_selected,'flat': flat_selected},UpdateExpression=string,ExpressionAttributeValues={':s': decimal.Decimal(status)},ReturnValues="UPDATED_NEW")
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}     

def control_all_water_meter_valve(event):
    a = eval(event['body'])
    wing_selected = a["wing"]
    flat_selected = a["flat"]
    status = int(a['status'])
    string ="set bathroom1.statuss = :s1, bathroom2.statuss=:s2, bathroom3.statuss=:s3, kitchen.statuss=:s4, misc.statuss=:s5"
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    try:
        response = table.update_item(Key={'wing': wing_selected,'flat': flat_selected},UpdateExpression=string,ExpressionAttributeValues={':s1': decimal.Decimal(status),':s2': decimal.Decimal(status),':s3': decimal.Decimal(status),':s4': decimal.Decimal(status),':s5': decimal.Decimal(status)},ReturnValues="UPDATED_NEW")  
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def insert_amenity_list(event):
    service  = []
    a = eval(event['body'])
    project = a["project"]
    number = a['number']
    for i in range(number):
        service.append(a['service'+str(i+1)])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_info')
    try:
        response = table.put_item(Item={'project':project,'amenities':number ,'services':service})
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def insert_amenity_flat_mapping(event):
    a = eval(event['body'])
    flat = a['flat']
    access_card_id = a['access_card_id']
    project = a['project'] 
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_flat_info')
    try:
        response = table.put_item(Item={'flat':flat,'access_card_id':access_card_id,'project':project})
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def insert_amenity_data(event):
    a = eval(event['body'])
    ids = a['access_card_id']
    timestamp = a['timestamp']
    project = a['project']
    amenity = a['amenity']
    types = a['type']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_data')
    try:
        response = table.put_item(Item={'access_id':ids,'timestamp':timestamp,'amenity':amenity,'project':project,'types':types})
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}


def insert_sprinkler_data(event):
    try:
        a = eval(event["body"])
        sprinkler_id = a["sprinkler_id"]
        area = a["area"]
        no_of_units = a["number"]
        start_hour = a['start_hour']
        start_minutes = a["start_minutes"]
        duration = a['duration']
        status = a['status']
        project = a["project"]
        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(TableName='sprinkler_data',Item={'sprinkler_id':{'S':sprinkler_id},'area':{'S':area},'no_of_units':{'N':str(no_of_units)},'project':{'S':project},'statuss':{'N':str(status)},'timings':{'L':[{'N':str(start_hour)},{'N':str(start_minutes)},{'N':str(duration)}]}})
        return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        return {'statusCode':400,'body':json.dumps(str(e)),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def set_billing_date(event):
    a = eval(event['body'])
    project = a['project']
    day = a['day']
    address = a['address']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('billing_date')
    try:
        response = table.put_item(Item={'project':project,'days':day,'address':address}) 
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    

def modify_billing_date(event):
    a = eval(event['body'])
    day = a['day']
    project = a['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    string = "set days = :d"
    table = dynamodb.Table('billing_date')
    try:
        response = table.update_item(Key={'project': project},UpdateExpression=string,ExpressionAttributeValues={':d': day},ReturnValues="UPDATED_NEW")  
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    
def put_lighting_data(event):
    try:
        a = eval(event["body"])
        light_id = a["light_id"]
        area = a["area"]
        no_of_units = a["number"]
        start_hour = a['start_hour']
        start_minutes = a["start_minutes"]
        duration_hour = a['duration_hour']
        duration_minute = a['duration_minute']
        status = a['status']
        project = a["project"]
        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(TableName='light_data',Item={'light_id':{'S':light_id},'Area':{'S':area},'no_of_units':{'N':str(no_of_units)},'project':{'S':project},'statuss':{'N':str(status)},'timings':{'L':[{'N':str(start_hour)},{'N':str(start_minutes)},{'N':str(duration_hour)},{'N':str(duration_minute)}]}})
        return {'statusCode':200,'body':json.dumps("Updated Successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        return {'statusCode':400,'body':json.dumps(str(e)),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def update_lighting_schedule(event):
    a = eval(event["body"])
    project = a['project']
    area = a['area']
    hour = a['hour']
    minutes = a['minutes']
    duration_hour = a['duration_hour']
    duration_minute = a['duration_minute']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("light_data")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_light_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['Area']==area:
            ids = eval(json.dumps(i,cls=DecimalEncoder))['light_id']
            try:
                response = table.update_item(Key={'Area': area,'light_id': ids},UpdateExpression="set timings = :a",ExpressionAttributeValues={':a': [hour, minutes, duration_hour,duration_minute]},ReturnValues="UPDATED_NEW")
                return{'statusCode':200,'body':json.dumps('Updated Successfully'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
            except Exception as e:
                return{'statusCode':400,'body':json.dumps('Updation Unsuccessfull'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
         
def raise_ticket(event):
    a = eval(event['body'])
    flat = a['wing']+str(a['flat'])
    now= a['timestamp']
    status  = 'InProcess'
    project = a['project']
    subject = a['subject']
    description = a['description']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('tickets')
    try:
        response = table.put_item(Item={'project':project,'timestamp':now,'Subject':subject,'Description':description,'flat':flat,'statuss':status}) 
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def insert_device_alert_data(event):
    a = eval(event['body']) 
    device_id = a['device_id']
    timestamp = a['timestamp']
    consumption = a['consumption']
    threshold = a['threshold']
    area = a['area']
    project = a['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('device_alerts')
    try:
        response = table.put_item(Item={'device_id':device_id,'status_timestamp':timestamp,'consumption':consumption,'threshold':threshold,'project':project,'area':area}) 
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps(e),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def update_ping_timestamp(event):
    a = eval(event['body'])
    timestamp = a['timestamp']
    device_id = a['device_id']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("device_alerts")
    try:
        response = table.update_item(Key={'device_id': device_id},UpdateExpression="set status_timestamp = :a",ExpressionAttributeValues={':a': timestamp},ReturnValues="UPDATED_NEW")
        return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   
    except Exception as e:
        return {'statusCode':400,'body':json.dumps(e),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}


########     GET  ############## 

def todays_water_usage(event):
    #results ={"results":[]}
    now = datetime.now() + timedelta(minutes=330)
    overall_yest_usage = 0
    todays_usage = {"K":0,"B":0,"M":0}
    yesterday = now - timedelta(days=1)
    starting_epoch_today = int(datetime(now.year,now.month,now.day,0,0,0).timestamp()-19800)
    end_epoch_today = int(datetime(now.year,now.month,now.day,23,59,59).timestamp()-19800)
    print(starting_epoch_today,end_epoch_today)
    starting_epoch_yesterday = int(datetime(yesterday.year,yesterday.month,yesterday.day,0,0,0).timestamp()-19800)
    end_epoch_yesterday = int(datetime(yesterday.year,yesterday.month,yesterday.day,23,59,59).timestamp()-19800)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        #results['results'].append(eval(json.dumps(i, cls=DecimalEncoder)))
        if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_today,end_epoch_today+1):
            if eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="K":
                todays_usage["K"] = todays_usage["K"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="B":
                todays_usage["B"] = todays_usage["B"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="M":
                todays_usage["M"] = todays_usage["M"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])    
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_yesterday,end_epoch_yesterday+1):
            overall_yest_usage = overall_yest_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    todays_usage["total"]  = int(todays_usage["K"]+todays_usage["B"]+todays_usage["M"])
    try:
        percent = int((int(todays_usage["K"]+todays_usage["B"]+todays_usage["M"])-overall_yest_usage)*(100)/(overall_yest_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    todays_usage["percent"] = percent 
    todays_usage["previous-day_usage"]  = round(overall_yest_usage/1000)
    todays_usage['K'] = round(todays_usage['K']/1000)
    todays_usage['M'] = round(todays_usage['M']/1000)
    todays_usage['B'] = round(todays_usage['B']/1000)
    todays_usage['total']  = round(todays_usage['total']/1000)
    return {'statusCode':200,'body':json.dumps(todays_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def weekly_water_usage(event):
    week_end = datetime.now() + timedelta(minutes=330)
    week_start = week_end - timedelta(days=6)
    prev_week_end = week_end - timedelta(days=7)
    prev_week_start = week_start - timedelta(days=7)
    week_usage = {"K":0,"B":0,"M":0}
    overall_prev_week_usage = 0
    starting_epoch_week = int(datetime(week_start.year,week_start.month,week_start.day,0,0,0).timestamp()-19800)
    end_epoch_week = int(datetime(week_end.year,week_end.month,week_end.day,23,59,59).timestamp()-19800)
    starting_epoch_prev_week = int(datetime(prev_week_start.year,prev_week_start.month,prev_week_start.day,0,0,0).timestamp()-19800)
    end_epoch_prev_week = int(datetime(prev_week_end.year,prev_week_end.month,prev_week_end.day,23,59,59).timestamp()-19800)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_week,end_epoch_week+1):
            if eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="K":
                week_usage["K"] = week_usage["K"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="B":
                week_usage["B"] = week_usage["B"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="M":
                week_usage["M"] = week_usage["M"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])    
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_prev_week,end_epoch_prev_week+1):
            overall_prev_week_usage = overall_prev_week_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    week_usage["total"]  = int(week_usage["K"]+week_usage["B"]+week_usage["M"])
    try:
        percent = int((int(week_usage["K"]+week_usage["B"]+week_usage["M"])-overall_prev_week_usage)*(100)/(overall_prev_week_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    week_usage["percent"] = percent 
    week_usage["previous_week_usage"]  = round(overall_prev_week_usage/1000)
    week_usage['K'] = round(week_usage['K']/1000)
    week_usage['M'] = round(week_usage['M']/1000)
    week_usage['B'] = round(week_usage['B']/1000)
    week_usage['total'] = round(week_usage['total']/1000)
    return {'statusCode':200,'body':json.dumps(week_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def monthly_water_usage(event):
    now = datetime.now() + timedelta(minutes=330)
    if now.month<10:
        if now.month==1:
            month = "01"
            year = str(now.year)
            prev_month = "12"
            prev_month_year = now.year-1
        else:
            month = "0"+str(now.month)
            year = str(now.year)
            prev_month = "0" + str(now.month-1)
            prev_month_year = year
    else:
        month = str(now.month)
        year = str(now.year)
        prev_month = str(now.month-1)
        prev_month_year = year
    month_usage = {"K":0,"B":0,"M":0}
    overall_prev_month_usage = 0
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend') 
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        if a[:4]==year and a[5:7]==month and eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="K":
            month_usage["K"] = month_usage["K"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==year and a[5:7]==month and eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="B":
            month_usage["B"] = month_usage["B"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==year and a[5:7]==month and eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="B":
            month_usage["M"] = month_usage["M"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==prev_month_year and a[5:7]==prev_month:
            overall_prev_month_usage = overall_prev_month_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    month_usage["total"]  = int(month_usage["K"]+month_usage["B"]+month_usage["M"])
    try:
        percent = int((int(month_usage["K"]+month_usage["B"]+month_usage["M"])-overall_prev_month_usage)*(100)/(overall_prev_month_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    month_usage["percent"] = percent 
    month_usage["previous_month_usage"]  = round(overall_prev_month_usage/1000)
    month_usage['K'] = round(month_usage['K']/1000)
    month_usage['M'] = round(month_usage['M']/1000)
    month_usage['B'] = round(month_usage['B']/1000)
    month_usage['total'] = round(month_usage['total']/1000)
    return {'statusCode':200,'body':json.dumps(month_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def yearly_water_usage(event):
    year = str((datetime.now() + timedelta(minutes=330)).year)
    prev_year = str(int(year)-1)
    year_usage = {"K":0,"B":0,"M":0}
    overall_prev_year_usage = 0
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        # +19800 as witjout it timestamp get converted in UTC TIME
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        if a[:4]==year and eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="K":
            year_usage["K"] = year_usage["K"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==year and eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="B":
            year_usage["B"] = year_usage["B"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==year and eval(json.dumps(i,cls=DecimalEncoder))["device_id"][-1]=="M":
            year_usage["M"] = year_usage["M"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==prev_year:
            overall_prev_year_usage = overall_prev_year_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    year_usage["total"]  = int(year_usage["K"]+year_usage["B"]+year_usage["M"])
    try:
        percent = int((int(year_usage["K"]+year_usage["B"]+year_usage["M"])-overall_prev_year_usage)*(100)/(overall_prev_year_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    year_usage["percent"] = percent 
    year_usage["previous_month_usage"]  = round(overall_prev_year_usage/1000)
    year_usage['K'] = round(year_usage['K']/1000)
    year_usage['M'] = round(year_usage['M']/1000)
    year_usage['B'] = round(year_usage['B']/1000)
    year_usage['total'] = round(year_usage['total']/1000)
    return {'statusCode':200,'body':json.dumps(year_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def weekly_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    epochs = []
    usage_graph = {(now-timedelta(days=6)).strftime('%a'):0,(now-timedelta(days=5)).strftime('%a'):0,(now-timedelta(days=4)).strftime('%a'):0,(now-timedelta(days=3)).strftime('%a'):0,(now-timedelta(days=2)).strftime('%a'):0,(now-timedelta(days=1)).strftime('%a'):0,now.strftime("%a"):0}
    #usage_graph = {now.strftime("%a"):0,(now-timedelta(days=1)).strftime('%a'):0,(now-timedelta(days=2)).strftime('%a'):0,(now-timedelta(days=3)).strftime('%a'):0,(now-timedelta(days=4)).strftime('%a'):0,(now-timedelta(days=5)).strftime('%a'):0,(now-timedelta(days=6)).strftime('%a'):0}
    for i in range(7):
        a = now-timedelta(days=i)
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),a.strftime("%a")])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[0][0],epochs[0][1]+1):
            usage_graph[epochs[0][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[1][0],epochs[1][1]+1):
            usage_graph[epochs[1][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[2][0],epochs[2][1]+1):
            usage_graph[epochs[2][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[3][0],epochs[3][1]+1):
            usage_graph[epochs[3][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])  
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[4][0],epochs[4][1]+1):
            usage_graph[epochs[4][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"]) 
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[5][0],epochs[5][1]+1):
            usage_graph[epochs[5][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[6][0],epochs[6][1]+1):
            usage_graph[epochs[6][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])                     
    return {'statusCode':200,'body':json.dumps(usage_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}



def monthly_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    monthly_graph = {}
    epochs=[]
    for i in range(30):
        a = now-timedelta(days=i)
        monthly_graph[str(i+1)] = 0
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),str(i+1)])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        for j in epochs:
            if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(j[0],j[1]+1):
                monthly_graph[j[2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
                break
    return {'statusCode':200,'body':json.dumps(monthly_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}} 
def year_graph(event):
    year = (datetime.now() + timedelta(minutes=330)).year
    yearly_graph = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,'Jun':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
    mapping = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('dev-water-meter-python-backend')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        if a[:4]==str(year):
            yearly_graph[mapping[a[5:7]]]+= int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    return {'statusCode':200,'body':json.dumps(yearly_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}       

def populate_wings_list(event):
    #someday use GSI to Eliminate the scan operation 
    wing = {}
    wings = []
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))["project"]== project:
                    wings.append(eval(json.dumps(i,cls=DecimalEncoder))["wing"])
        else: 
            response = table.scan()
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))["project"]== project:
                    wings.append(eval(json.dumps(i,cls=DecimalEncoder))["wing"])
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            wings = list(set(wings))
            wing["wings"]=wings
            break 
    return {'statusCode':200,'body':json.dumps(wing),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}    

def populate_flat_list(event):
    wing_selected = event["queryStringParameters"]["wing"]
    project = event['queryStringParameters']['project']
    flat = {}
    flats = []
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))["wing"]==wing_selected and eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
                    flats.append(eval(json.dumps(i,cls=DecimalEncoder))["flat"])
        else: 
            response = table.scan()
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))["wing"]==wing_selected and eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
                    flats.append(eval(json.dumps(i,cls=DecimalEncoder))["flat"])
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            flat["flats"] = flats
            break   
    return {'statusCode':200,'body':json.dumps(flat),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}        

############## if any project requires more than 5 devices then it can be implemented here. not sure but mostly#######
# As of now project table is queried instead first see how many columns are there then accordingly include
# that many number areas in devices list
def populate_device_list(event):
    wing_selected = event["queryStringParameters"]["wing"]
    flat_selected = event["queryStringParameters"]["flat"]
    project = event['queryStringParameters']['project']
    device_list = {"devices":{}}
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing_selected) & Key('flat').eq(flat_selected))
    for i in response["Items"]:
        device_list["devices"]["kitchen"] = eval(json.dumps(i,cls=DecimalEncoder))["kitchen"]["id"]   
        device_list["devices"]["bathroom1"] = eval(json.dumps(i,cls=DecimalEncoder))["bathroom1"]["id"]
        device_list["devices"]["bathroom2"] = eval(json.dumps(i,cls=DecimalEncoder))["bathroom2"]["id"]
        device_list["devices"]["bathroom3"] = eval(json.dumps(i,cls=DecimalEncoder))["bathroom3"]["id"]
        device_list["devices"]["misc"] = eval(json.dumps(i,cls=DecimalEncoder))["misc"]["id"]
    device_list["devices"] = {key:val for key, val in device_list["devices"].items() if val != "NA"}               
    return {'statusCode':200,'body':json.dumps(device_list),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}    

def user_valve_status(event):
    # Returns device lists based on two conditions 
    # 1 if area given in query string parameter i.e return a particular device ids status 
    # 2 if area not given and all five needs to be populated.
    results = {'status':[]}
    temp = populate_device_list(event)
    temp = eval(temp['body'])["devices"]
    status_list = {"status":{}}
    if event["queryStringParameters"]["area"]!="All":
        wing_selected = event["queryStringParameters"]["wing"]
        flat_selected = event["queryStringParameters"]["flat"]
        area_selected = event["queryStringParameters"]["area"]
        project  = event["queryStringParameters"]["project"]
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('project_wing_device_data')
        response = table.query(KeyConditionExpression=Key('wing').eq(wing_selected) & Key('flat').eq(flat_selected))
        for i in response["Items"]:
            status_list['status'][area_selected] = eval(json.dumps(i,cls=DecimalEncoder))[area_selected]["statuss"]
    elif event["queryStringParameters"]["area"]=="All":
        wing_selected = event["queryStringParameters"]["wing"]
        flat_selected = event["queryStringParameters"]["flat"]
        project  = event["queryStringParameters"]["project"]
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('project_wing_device_data')
        response = table.query(KeyConditionExpression=Key('wing').eq(wing_selected) & Key('flat').eq(flat_selected))
        for i in response["Items"]:
            for key,values in temp.items():
                status_list['status'][key] = eval(json.dumps(i,cls=DecimalEncoder))[key]["statuss"]
    results['status'].append(status_list['status'])
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def consumption_flat_wise(event): 
    temp = populate_device_list(event)
    consumption = {"results":{}}
    start_epoch = int(datetime(int(event["queryStringParameters"]["start"][0:4]),int(event["queryStringParameters"]["start"][5:7]),int(event["queryStringParameters"]["start"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["end"][0:4]),int(event["queryStringParameters"]["end"][5:7]),int(event["queryStringParameters"]["end"][8:]),23,59,59).timestamp())-19800
    project = event["queryStringParameters"]["project"] 
    temp = eval(temp['body'])["devices"]
    for keys,value in temp.items():
        consumption["results"][keys] = 0
    for key,values in temp.items():
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('dev-water-meter-python-backend')
        response = table.query(KeyConditionExpression=Key('device_id').eq(values) & Key('timestamp').between(start_epoch, end_epoch))
        for i in response['Items']:
            consumption["results"][key] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    table = dynamodb.Table('meter_card')
    response = table.scan()
    sum1 = 0 
    charges = 0
    tax = 0
    bill = 0
    for i in response["Items"]:
        if eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
            if (eval(json.dumps(i,cls=DecimalEncoder))["types"])=="slab":
                other_charges = eval(json.dumps(i,cls=DecimalEncoder))["minimum"]
                for keys,value in consumption["results"].items():
                    sum1 += value  
                slab1 = eval(json.dumps(i,cls=DecimalEncoder))["slab1"]["ranges"][1]
                slab2 =  eval(json.dumps(i,cls=DecimalEncoder))["slab2"]["ranges"][1]
                slab3 = eval(json.dumps(i,cls=DecimalEncoder))["slab3"]["ranges"][1]
                slab4 = eval(json.dumps(i,cls=DecimalEncoder))["slab4"]["ranges"][1]
                if sum1 in range(0,slab1+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab1"]["rate"]*sum1)/1000,1) 
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
                elif sum1 in range(slab1+1,slab2+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab2"]["rate"]*sum1)/1000,1) 
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
                elif sum1 in range(slab2+1,slab3+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab3"]["rate"]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
                elif sum1 in range(slab3+1,slab4+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab4"]["rate"]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)        
                elif sum1>slab4:
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab5"]["rate"]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
            elif eval(json.dumps(i,cls=DecimalEncoder))["types"]=="CPL":
                other_charges = eval(json.dumps(i,cls=DecimalEncoder))["minimum"]
                for keys,value in consumption["results"].items():
                    sum1 += value
                slab1 = eval(json.dumps(i,cls=DecimalEncoder))["slab1"]["ranges"][1]
                slab2 =  eval(json.dumps(i,cls=DecimalEncoder))["slab2"]["ranges"][1]
                slab3 = eval(json.dumps(i,cls=DecimalEncoder))["slab3"]["ranges"][1]
                slab4 = eval(json.dumps(i,cls=DecimalEncoder))["slab4"]["ranges"][1]
                if sum1 in range(0,slab1+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][0]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
                elif sum1 in range(slab1+1,slab2+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][1]*sum1)/1000,1) 
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
                elif sum1 in range(slab2+1,slab3+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][2]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)
                elif sum1 in range(slab3+1,slab4+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][3]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)        
                elif sum1>slab4:
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][4]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax)      
    consumption["results"]["usage_charges"] = charges
    consumption["results"]["tax"] = tax
    consumption["results"]["bill_for_duration"]=bill
    consumption["results"]["total_consumption"] = sum1
    consumption["results"]["flat"] = event["queryStringParameters"]["wing"]+event["queryStringParameters"]["flat"]
    consumption['results']['other_charges'] = other_charges
    return {'statusCode':200,'body':json.dumps(consumption),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def bill_api_with_minimum_charges(event):
    temp = populate_device_list(event)
    consumption = {"results":{}}
    start_epoch = int(datetime(int(event["queryStringParameters"]["start"][0:4]),int(event["queryStringParameters"]["start"][5:7]),int(event["queryStringParameters"]["start"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["end"][0:4]),int(event["queryStringParameters"]["end"][5:7]),int(event["queryStringParameters"]["end"][8:]),23,59,59).timestamp())-19800
    project = event["queryStringParameters"]["project"] 
    temp = eval(temp['body'])["devices"]
    for keys,value in temp.items():
        consumption["results"][keys] = 0
    for key,values in temp.items():
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('dev-water-meter-python-backend')
        response = table.query(KeyConditionExpression=Key('device_id').eq(values) & Key('timestamp').between(start_epoch, end_epoch))
        for i in response['Items']:
            consumption["results"][key] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    table = dynamodb.Table('meter_card')
    response = table.scan()
    sum1 = 0 
    charges = 0
    tax = 0
    bill = 0
    for i in response["Items"]:
        if eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
            if (eval(json.dumps(i,cls=DecimalEncoder))["types"])=="slab":
                other_charges = eval(json.dumps(i,cls=DecimalEncoder))["minimum"]
                for keys,value in consumption["results"].items():
                    sum1 += value  
                slab1 = eval(json.dumps(i,cls=DecimalEncoder))["slab1"]["ranges"][1]
                slab2 =  eval(json.dumps(i,cls=DecimalEncoder))["slab2"]["ranges"][1]
                slab3 = eval(json.dumps(i,cls=DecimalEncoder))["slab3"]["ranges"][1]
                slab4 = eval(json.dumps(i,cls=DecimalEncoder))["slab4"]["ranges"][1]
                if sum1 in range(0,slab1+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab1"]["rate"]*sum1)/1000,1) 
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
                elif sum1 in range(slab1+1,slab2+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab2"]["rate"]*sum1)/1000,1) 
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
                elif sum1 in range(slab2+1,slab3+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab3"]["rate"]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
                elif sum1 in range(slab3+1,slab4+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab4"]["rate"]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])        
                elif sum1>slab4:
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["slab5"]["rate"]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["types"]=="CPL":
                other_charges = eval(json.dumps(i,cls=DecimalEncoder))["minimum"]
                for keys,value in consumption["results"].items():
                    sum1 += value
                slab1 = eval(json.dumps(i,cls=DecimalEncoder))["slab1"]["ranges"][1]
                slab2 =  eval(json.dumps(i,cls=DecimalEncoder))["slab2"]["ranges"][1]
                slab3 = eval(json.dumps(i,cls=DecimalEncoder))["slab3"]["ranges"][1]
                slab4 = eval(json.dumps(i,cls=DecimalEncoder))["slab4"]["ranges"][1]
                if sum1 in range(0,slab1+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][0]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
                elif sum1 in range(slab1+1,slab2+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][1]*sum1)/1000,1) 
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
                elif sum1 in range(slab2+1,slab3+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][2]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])
                elif sum1 in range(slab3+1,slab4+1):
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][3]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])        
                elif sum1>slab4:
                    charges  = round((eval(json.dumps(i,cls=DecimalEncoder))["cpl"][4]*sum1)/1000,1)
                    tax = round((eval(json.dumps(i,cls=DecimalEncoder))["tax"]*charges)/100,1)
                    bill = round(charges+tax+eval(json.dumps(i,cls=DecimalEncoder))["minimum"])      
    consumption["results"]["usage_charges"] = charges
    consumption["results"]["tax"] = tax
    consumption["results"]["bill_for_duration"]=bill
    consumption["results"]["total_consumption"] = sum1
    consumption["results"]["flat"] = event["queryStringParameters"]["wing"]+event["queryStringParameters"]["flat"]
    consumption['results']['other_charges'] = other_charges
    return {'statusCode':200,'body':json.dumps(consumption),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}



def update_meter_card(event):
    a = eval(event["body"])
    if a["enable_slab"]=="yes":
        project = a["project"]
        minimum = str(a["minimum"])
        tax  = str(a["tax"])
        slab1_limit = a["slab_1_limit"]
        slab2_limit = a["slab_2_limit"]
        slab3_limit = a["slab_3_limit"]
        slab4_limit = a["slab_4_limit"]
        slab_1_rate = str(a["rate1"])
        slab_2_rate = str(a["rate2"])
        slab_3_rate = str(a["rate3"])
        slab_4_rate = str(a["rate4"])
        slab_5_rate = str(a["rate5"])
        string = "set slab1.ranges = :s1ra, slab1.rate=:s1r, slab2.ranges = :s2ra, slab2.rate=:s2r, slab3.ranges = :s3ra, slab3.rate=:s3r, slab4.ranges = :s4ra, slab4.rate=:s4r, slab5.ranges = :s5ra, slab5.rate=:s5r, types=:t, minimum=:m, tax=:a"
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('meter_card')
        try:
            response = table.update_item(Key={'project': project},UpdateExpression=string,ExpressionAttributeValues={':s1ra':[0,slab1_limit],':s1r':decimal.Decimal(slab_1_rate),':s2ra':[slab1_limit+1,slab2_limit],':s2r':decimal.Decimal(slab_2_rate),':s3ra':[slab2_limit+1,slab3_limit],':s3r':decimal.Decimal(slab_3_rate),':s4ra':[slab3_limit+1,slab4_limit],':s4r':decimal.Decimal(slab_4_rate),':s5ra':[slab4_limit+1],':s5r':decimal.Decimal(slab_5_rate),':t':"slab",':m':decimal.Decimal(minimum),':a':decimal.Decimal(tax) },ReturnValues="UPDATED_NEW")
            return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
        except Exception as e:
            print(e)
            return {'statusCode':200,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    elif a["enable_slab"]=="no":
        project  = a["project"]
        minimum = str(a["minimum"])
        slab1_limit = a["slab_1_limit"]
        slab2_limit = a["slab_2_limit"]
        slab3_limit = a["slab_3_limit"]
        slab4_limit = a["slab_4_limit"]
        cpl_slab1 = str(a["rate1"])
        cpl_slab2 = str(a["rate2"])
        cpl_slab3 = str(a["rate3"])
        cpl_slab4 = str(a["rate4"])
        cpl_slab5 = str(a["rate5"])
        tax = str(a["tax"])
        string = "set slab1.ranges = :s1ra, slab2.ranges = :s2ra, slab3.ranges = :s3ra, slab4.ranges = :s4ra, slab5.ranges = :s5ra, types=:t, minimum=:m, tax=:a, cpl=:c"
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('meter_card')
        try:
            response = table.update_item(Key={'project': project},UpdateExpression=string,ExpressionAttributeValues={':s1ra':[0,slab1_limit],':s2ra':[slab1_limit+1,slab2_limit],':s3ra':[slab2_limit+1,slab3_limit],':s4ra':[slab3_limit+1,slab4_limit],':s5ra':[slab4_limit+1],':t':"CPL",':m':decimal.Decimal(minimum),':a':decimal.Decimal(tax),':c':[decimal.Decimal(cpl_slab1),decimal.Decimal(cpl_slab2),decimal.Decimal(cpl_slab3),decimal.Decimal(cpl_slab4),decimal.Decimal(cpl_slab5)] },ReturnValues="UPDATED_NEW")
            return {'statusCode':200,'body':json.dumps("status updated"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
        except Exception as e:
            print(e)
            return {'statusCode':200,'body':json.dumps("status updation failed "),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def get_meter_card(event):
    results = {}
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('meter_card')
    project = event["queryStringParameters"]["project"]
    response = table.query(KeyConditionExpression=Key('project').eq(project))
    if response["Items"][0]['types']=="slab":
        results["slab1"] = [eval(json.dumps(response["Items"][0]['slab1'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab1'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['slab1'],cls=DecimalEncoder))["rate"]]
        results["slab2"] = [eval(json.dumps(response["Items"][0]['slab2'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab2'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['slab2'],cls=DecimalEncoder))["rate"]]
        results["slab3"] = [eval(json.dumps(response["Items"][0]['slab3'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab3'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['slab3'],cls=DecimalEncoder))["rate"]]
        results["slab4"] = [eval(json.dumps(response["Items"][0]['slab4'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab4'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['slab4'],cls=DecimalEncoder))["rate"]]
        results["slab5"] = [eval(json.dumps(response["Items"][0]['slab5'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab5'],cls=DecimalEncoder))["rate"]]
        results['tax'] = eval(json.dumps(response["Items"][0]['tax'],cls=DecimalEncoder))
        results['minimum'] = eval(json.dumps(response["Items"][0]['minimum'],cls=DecimalEncoder))
        results['project'] = project
    elif response["Items"][0]["types"]=="CPL":
        results["tax"] = eval(json.dumps(response["Items"][0]['tax'],cls=DecimalEncoder))
        results['minimum'] = eval(json.dumps(response["Items"][0]['minimum'],cls=DecimalEncoder))
        results["slab1"] = [eval(json.dumps(response["Items"][0]['slab1'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab1'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['cpl'],cls=DecimalEncoder))[0]]
        results["slab2"] = [eval(json.dumps(response["Items"][0]['slab2'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab2'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['cpl'],cls=DecimalEncoder))[1]]
        results["slab3"] = [eval(json.dumps(response["Items"][0]['slab3'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab3'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['cpl'],cls=DecimalEncoder))[2]]
        results["slab4"] = [eval(json.dumps(response["Items"][0]['slab4'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['slab4'],cls=DecimalEncoder))["ranges"][1],eval(json.dumps(response["Items"][0]['cpl'],cls=DecimalEncoder))[3]]
        results["slab5"] = [eval(json.dumps(response["Items"][0]['slab5'],cls=DecimalEncoder))["ranges"][0],eval(json.dumps(response["Items"][0]['cpl'],cls=DecimalEncoder))[4]]        
        results['project'] = project
    final_results = {'slab-rates':[results]}
    return {'statusCode':200,'body':json.dumps(final_results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    
def get_meter_details(event):
    wing = event["queryStringParameters"]["wing"]
    flat = event["queryStringParameters"]["flat"]
    results = {'results':[]}
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("project_wing_device_data")
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response["Items"]:
        dict1 = {"id":eval(json.dumps(i,cls=DecimalEncoder))["kitchen"]["id"],'location':'kitchen','flat':wing+flat,'category':'Residential Meters' }
        dict2 = {"id":eval(json.dumps(i,cls=DecimalEncoder))["bathroom1"]["id"],'location':'bathroom','flat':wing+flat,'category':'Residential Meters' }
        dict3 = {"id":eval(json.dumps(i,cls=DecimalEncoder))["bathroom2"]["id"],'location':'bathroom','flat':wing+flat,'category':'Residential Meters' }
        dict4 = {"id":eval(json.dumps(i,cls=DecimalEncoder))["bathroom3"]["id"],'location':'bathroom','flat':wing+flat,'category':'Residential Meters' }
        dict5 = {"id":eval(json.dumps(i,cls=DecimalEncoder))["misc"]["id"],'location':'misc','flat':wing+flat,'category':'Residential Meters' }
        results['results'].append(dict1)
        results['results'].append(dict2)
        results['results'].append(dict3)
        results['results'].append(dict4)
        results['results'].append(dict5)
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_area_list(event):
    results = {}
    areas = []
    project = event['queryStringParameters']["project"]
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("sprinkler_data")
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
                    areas.append(eval(json.dumps(i,cls=DecimalEncoder))['area'])
        else: 
            response = table.scan()
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
                    areas.append(eval(json.dumps(i,cls=DecimalEncoder))['area'])
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            results['areas'] = areas
            break 
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
  
    
def sprinkler_valve_info(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    area = event['queryStringParameters']['area']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("sprinkler_data")
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))['project']==project and eval(json.dumps(i,cls=DecimalEncoder))['area']==area:
                    ids = eval(json.dumps(i,cls=DecimalEncoder))['sprinkler_id']
                    number = eval(json.dumps(i,cls=DecimalEncoder))['no_of_units']
                    timings = str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][0])+":"+str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][1])
                    duration = str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][2])
                    status = eval(json.dumps(i,cls=DecimalEncoder))['statuss']
        else: 
            response = table.scan()
            for i in response["Items"]:
                if eval(json.dumps(i,cls=DecimalEncoder))['project']==project and eval(json.dumps(i,cls=DecimalEncoder))['area']==area:
                    ids = eval(json.dumps(i,cls=DecimalEncoder))['sprinkler_id']
                    number = eval(json.dumps(i,cls=DecimalEncoder))['no_of_units']
                    timings = str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][0])+":"+str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][1])
                    duration = str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][2])
                    status = eval(json.dumps(i,cls=DecimalEncoder))['statuss']
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            results['results'].append({'area':area,'id':ids,'number':number,'status':status,'start':timings,'duration':duration})
            break            
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   


def sprinkler_modify_schedule(event):
    a = eval(event["body"])
    project = a['project']
    area = a['area']
    hour = a['hour']
    minutes = a['minutes']
    duration = a['duration']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("sprinkler_data")
    response = table.scan()
    for i in response['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['project']==project and eval(json.dumps(i,cls=DecimalEncoder))['area']==area:
            ids = eval(json.dumps(i,cls=DecimalEncoder))['sprinkler_id']
            try:
                response = table.update_item(Key={'area': area,'sprinkler_id': ids},UpdateExpression="set timings = :a",ExpressionAttributeValues={':a': [hour, minutes, duration]},ReturnValues="UPDATED_NEW")
                return{'statusCode':200,'body':json.dumps('Updated Successfully'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
            except Exception as e:
                return{'statusCode':400,'body':json.dumps('Updation Unsuccessfull'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
         

def sprinkler_valve_status_change(event):
    project = event['queryStringParameters']['project']
    area = event['queryStringParameters']['area']
    status = event['queryStringParameters']['status']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("sprinkler_data")
    response = table.scan()
    for i in response['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['project']==project and eval(json.dumps(i,cls=DecimalEncoder))['area']==area:
            ids = eval(json.dumps(i,cls=DecimalEncoder))['sprinkler_id']
            try:
                response = table.update_item(Key={'area': area,'sprinkler_id': ids},UpdateExpression="set statuss = :a",ExpressionAttributeValues={':a':status },ReturnValues="UPDATED_NEW")
                return {'statusCode':200,'body':json.dumps('Valve Status Updated Successfully'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
            except Exception as e:
                return {'statusCode':400,'body':json.dumps('Updation Unsuccessfull'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    

def sprinkler_todays_usage(event):
    now = datetime.now() + timedelta(minutes=330)
    overall_yest_usage = 0
    todays_usage = {"total":0,"percent":0}
    yesterday = now - timedelta(days=1)
    starting_epoch_today = int(datetime(now.year,now.month,now.day,0,0,0).timestamp()-19800)
    end_epoch_today = int(datetime(now.year,now.month,now.day,23,59,59).timestamp()-19800)
    starting_epoch_yesterday = int(datetime(yesterday.year,yesterday.month,yesterday.day,0,0,0).timestamp()-19800)
    end_epoch_yesterday = int(datetime(yesterday.year,yesterday.month,yesterday.day,23,59,59).timestamp()-19800)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        #results['results'].append(eval(json.dumps(i, cls=DecimalEncoder)))
        if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_today,end_epoch_today+1):
            todays_usage["total"] = todays_usage["total"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_yesterday,end_epoch_yesterday+1):
            overall_yest_usage = overall_yest_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    try:
        percent = int((int(todays_usage['total'])-overall_yest_usage)*(100)/(overall_yest_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    todays_usage["percent"] = percent 
    todays_usage["previous-day_usage"]  = overall_yest_usage
    return {'statusCode':200,'body':json.dumps(todays_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_weekly_usage(event):
    week_end = datetime.now() + timedelta(minutes=330)
    week_start = week_end - timedelta(days=6)
    prev_week_end = week_end - timedelta(days=7)
    prev_week_start = week_start - timedelta(days=7)
    week_usage = {"total":0,"percent":0,"previous_week_usage":0}
    overall_prev_week_usage = 0
    starting_epoch_week = int(datetime(week_start.year,week_start.month,week_start.day,0,0,0).timestamp()-19800)
    end_epoch_week = int(datetime(week_end.year,week_end.month,week_end.day,23,59,59).timestamp()-19800)
    starting_epoch_prev_week = int(datetime(prev_week_start.year,prev_week_start.month,prev_week_start.day,0,0,0).timestamp()-19800)
    end_epoch_prev_week = int(datetime(prev_week_end.year,prev_week_end.month,prev_week_end.day,23,59,59).timestamp()-19800)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_week,end_epoch_week+1):
            week_usage["total"] = week_usage["total"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])    
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(starting_epoch_prev_week,end_epoch_prev_week+1):
            overall_prev_week_usage = overall_prev_week_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    try:
        percent = int((int(week_usage['total'])-overall_prev_week_usage)*(100)/(overall_prev_week_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    week_usage["percent"] = percent 
    week_usage["previous_week_usage"]  = overall_prev_week_usage 
    return {'statusCode':200,'body':json.dumps(week_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_month_usage(event):
    now = datetime.now() + timedelta(minutes=330)
    if now.month<10:
        if now.month==1:
            month = "01"
            year = str(now.year)
            prev_month = "12"
            prev_month_year = now.year-1
        else:
            month = "0"+str(now.month)
            year = str(now.year)
            prev_month = "0" + str(now.month-1)
            prev_month_year = year
    else:
        month = str(now.month)
        year = str(now.year)
        prev_month = str(now.month-1)
        prev_month_year = year
    month_usage = {"total":0,"percent":0,"previous_month_usage":0}
    overall_prev_month_usage = 0
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption') 
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        if a[:4]==year and a[5:7]==month:
            month_usage["total"] = month_usage["total"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==prev_month_year and a[5:7]==prev_month:
            overall_prev_month_usage = overall_prev_month_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    try:
        percent = int((int(month_usage["total"])-overall_prev_month_usage)*(100)/(overall_prev_month_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    month_usage["percent"] = percent 
    month_usage["previous_month_usage"]  = overall_prev_month_usage
    return {'statusCode':200,'body':json.dumps(month_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_year_usage(event):
    year = str((datetime.now() + timedelta(minutes=330)).year)
    prev_year = str(int(year)-1)
    year_usage = {"total":0,"percent":0,"previous_year_usage":0}
    overall_prev_year_usage = 0
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        # +19800 as witjout it timestamp get converted in UTC TIME
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        if a[:4]==year:
            year_usage["total"] = year_usage["total"] + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif a[:4]==prev_year:
            overall_prev_year_usage = overall_prev_year_usage + int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    try:
        percent = int((int(year_usage["total"])-overall_prev_year_usage)*(100)/(overall_prev_year_usage))
    except Exception as e:
        percent = "Data Unavailable"    
    year_usage["percent"] = percent 
    year_usage["previous_year_usage"]  = overall_prev_year_usage
    return {'statusCode':200,'body':json.dumps(year_usage),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_weekly_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    epochs = []
    usage_graph = {now.strftime("%a"):0,(now-timedelta(days=1)).strftime('%a'):0,(now-timedelta(days=2)).strftime('%a'):0,(now-timedelta(days=3)).strftime('%a'):0,(now-timedelta(days=4)).strftime('%a'):0,(now-timedelta(days=5)).strftime('%a'):0,(now-timedelta(days=6)).strftime('%a'):0}
    for i in range(7):
        a = now-timedelta(days=i)
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),a.strftime("%a")])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[0][0],epochs[0][1]+1):
            usage_graph[epochs[0][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[1][0],epochs[1][1]+1):
            usage_graph[epochs[1][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[2][0],epochs[2][1]+1):
            usage_graph[epochs[2][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[3][0],epochs[3][1]+1):
            usage_graph[epochs[3][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])  
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[4][0],epochs[4][1]+1):
            usage_graph[epochs[4][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"]) 
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[5][0],epochs[5][1]+1):
            usage_graph[epochs[5][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
        elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[6][0],epochs[6][1]+1):
            usage_graph[epochs[6][2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])                     
    return {'statusCode':200,'body':json.dumps(usage_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_yearly_graph(event):
    year = (datetime.now() + timedelta(minutes=330)).year
    yearly_graph = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,'Jun':0,'July':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
    mapping = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        if a[:4]==str(year):
            yearly_graph[mapping[a[5:7]]]+= int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
    return {'statusCode':200,'body':json.dumps(yearly_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_monthly_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    monthly_graph = {}
    epochs=[]
    for i in range(30):
        a = now-timedelta(days=i)
        monthly_graph[str(i+1)] = 0
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),str(i+1)])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_consumption')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_sprinkler_project",
    KeyConditionExpression=Key('project').eq(event["queryStringParameters"]["project"]),)
    for i in resp['Items']:
        for j in epochs:
            if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(j[0],j[1]+1):
                monthly_graph[j[2]] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
                break
    return {'statusCode':200,'body':json.dumps(monthly_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def sprinkler_consumption(event):
    results ={'consumption':0}
    start_epoch = int(datetime(int(event["queryStringParameters"]["start"][0:4]),int(event["queryStringParameters"]["start"][5:7]),int(event["queryStringParameters"]["start"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["end"][0:4]),int(event["queryStringParameters"]["end"][5:7]),int(event["queryStringParameters"]["end"][8:]),23,59,59).timestamp())-19800
    project = event["queryStringParameters"]["project"] 
    area = event['queryStringParameters']['area']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('sprinkler_data')
    response = table.scan()
    for i in response['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['project']==project and eval(json.dumps(i,cls=DecimalEncoder))['area']==area:
            table1 = dynamodb.Table('sprinkler_consumption')
            response1 = table1.query(KeyConditionExpression=Key('sprinkler_id').eq(eval(json.dumps(i,cls=DecimalEncoder))['sprinkler_id']) & Key('timestamp').between(start_epoch, end_epoch))
            results['area'] = eval(json.dumps(i,cls=DecimalEncoder))['area']
            results['sprinkler_id'] = eval(json.dumps(i,cls=DecimalEncoder))['sprinkler_id']
            results['no_of_units'] = eval(json.dumps(i,cls=DecimalEncoder))['no_of_units']
            results['timings'] = str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][0])+':'+str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][1])
            results['duration'] = str(eval(json.dumps(i,cls=DecimalEncoder))['timings'][2])
            break
    for k in response1['Items']:
        results['consumption']+=eval(json.dumps(k,cls=DecimalEncoder))['consumption']
    final_results = {'results': [results]}
    return {'statusCode':200,'body':json.dumps(final_results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def boom_barrier_info_by_flat(event):
    results = {'results':[]}
    flat = event["queryStringParameters"]["wing"]+event["queryStringParameters"]["flat"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    response = table.query(KeyConditionExpression=Key('flat').eq(flat))
    for i in response['Items']:
        flat_number =  eval(json.dumps(i,cls=DecimalEncoder))['flat']
        vehicle_no = eval(json.dumps(i,cls=DecimalEncoder))['vehicle_no']
        model = eval(json.dumps(i,cls=DecimalEncoder))['model']
        brand = eval(json.dumps(i,cls=DecimalEncoder))['brand']
        types  = eval(json.dumps(i,cls=DecimalEncoder))['types']
        rfid = eval(json.dumps(i,cls=DecimalEncoder))['rfid']
        dict1 = {"vehicle_no":vehicle_no,"model":model,"brand":brand,"types":types,"rfid":rfid,"flat":flat_number}
        results['results'].append(dict1)
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   

def rfid_monitoring_by_date(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_data')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_rfid_by_project_timestamp",
    KeyConditionExpression=Key('project').eq(project) & Key('timestamp').between(start_epoch, end_epoch),)
    rfid_list = {}
    for i in resp['Items']:
        if str(eval(json.dumps(i,cls=DecimalEncoder))['rfid']) in rfid_list.keys():
            temp1 = str(eval(json.dumps(i,cls=DecimalEncoder))['rfid'])
            results['results'].append({'flat':rfid_list[temp1]['flat'],'vehicle_type':rfid_list[temp1]['vehicle_types'],'vehicle_no':rfid_list[temp1]['vehicle_no'],'Brand':rfid_list[temp1]['brand'],'model':rfid_list[temp1]['model'],'rfid':temp1,'time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800)),'IN_or_OUT':eval(json.dumps(i,cls=DecimalEncoder))["types"]})
        else:
            rfid_list[str(eval(json.dumps(i,cls=DecimalEncoder))['rfid'])] = {}
            temp = str(eval(json.dumps(i,cls=DecimalEncoder))['rfid'])
            table = dynamodb.Table('boom_barrier_info')
            response = table.query(
            # Add the name of the index you want to use in your query.
            IndexName="query_boom_barrier_project",
            KeyConditionExpression=Key('project').eq(project),)
            for j in response['Items']:
                if eval(json.dumps(j,cls=DecimalEncoder))['rfid'] == temp:
                    rfid_list[temp]['flat'] = eval(json.dumps(j,cls=DecimalEncoder))['flat']
                    rfid_list[temp]['vehicle_types'] = eval(json.dumps(j,cls=DecimalEncoder))['types']
                    rfid_list[temp]['vehicle_no'] = eval(json.dumps(j,cls=DecimalEncoder))['vehicle_no']
                    rfid_list[temp]['brand'] = eval(json.dumps(j,cls=DecimalEncoder))['brand']
                    rfid_list[temp]['model'] = eval(json.dumps(j,cls=DecimalEncoder))['model']
                    break
            results['results'].append({'flat':rfid_list[temp]['flat'],'vehicle_type':rfid_list[temp]['vehicle_types'],'vehicle_no':rfid_list[temp]['vehicle_no'],'Brand':rfid_list[temp]['brand'],'model':rfid_list[temp]['model'],'rfid':temp,'time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800)),'IN_or_OUT':eval(json.dumps(i,cls=DecimalEncoder))["types"]})     
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   


def boom_barrier_info_by_rfid(event):
    results = {'results':[]}
    project = event["queryStringParameters"]["project"]
    rfid = event["queryStringParameters"]["rfid"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_boom_barrier_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['rfid']==rfid:
            flat_number =  eval(json.dumps(i,cls=DecimalEncoder))['flat']
            vehicle_no = eval(json.dumps(i,cls=DecimalEncoder))['vehicle_no']
            model = eval(json.dumps(i,cls=DecimalEncoder))['model']
            brand = eval(json.dumps(i,cls=DecimalEncoder))['brand']
            types  = eval(json.dumps(i,cls=DecimalEncoder))['types']
            rfid = eval(json.dumps(i,cls=DecimalEncoder))['rfid']
            dict1 = {"vehicle_no":vehicle_no,"model":model,"brand":brand,"types":types,"rfid":rfid,"flat":flat_number}
            results['results'].append(dict1)    
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def get_vehicle_list(event):
    results = {'results':[]}
    flat = event["queryStringParameters"]["wing"]+event["queryStringParameters"]["flat"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    response = table.query(KeyConditionExpression=Key('flat').eq(flat))
    for i in response['Items']:
        vehicle_no = eval(json.dumps(i,cls=DecimalEncoder))['vehicle_no']
        results["results"].append(vehicle_no)
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    
def delete_rfid_card(event):
    flat = event["queryStringParameters"]["wing"]+event["queryStringParameters"]["flat"]
    vehicle = event["queryStringParameters"]["vehicle"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    try:
        response = table.delete_item(Key={'flat': flat,'vehicle_no': vehicle}) 
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("Card deletion failed"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps("card deleted successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}        

def rfid_monitoring_by_rfid(event):
    results = {"results":[]}
    rfid = event['queryStringParameters']["rfid"]
    project = event['queryStringParameters']['project']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_boom_barrier_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['rfid']==rfid:
            flat_number =  eval(json.dumps(i,cls=DecimalEncoder))['flat']
            vehicle_no = eval(json.dumps(i,cls=DecimalEncoder))['vehicle_no']
            model = eval(json.dumps(i,cls=DecimalEncoder))['model']
            brand = eval(json.dumps(i,cls=DecimalEncoder))['brand']
            types  = eval(json.dumps(i,cls=DecimalEncoder))['types']
            rfid = eval(json.dumps(i,cls=DecimalEncoder))['rfid']
            break
    table = dynamodb.Table('boom_barrier_data')
    response = table.query(KeyConditionExpression=Key('rfid').eq(rfid) & Key('timestamp').between(start_epoch, end_epoch))
    for i in response["Items"]:
        stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        in_out = eval(json.dumps(i,cls=DecimalEncoder))["types"]
        results["results"].append({'flat':flat_number,"vehicle_no":vehicle_no,'model':model,"brand":brand,'vehicle_type':types,'rfid':rfid,'time':stamp,'IN/OUT':in_out})

    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def rfid_monitoring_by_flat(event):
    results = {"results":[]}
    flat = event['queryStringParameters']['wing'] + event['queryStringParameters']['flat']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('boom_barrier_info')
    response = table.query(KeyConditionExpression=Key('flat').eq(flat))
    for i in response['Items']:
        flat_number =  eval(json.dumps(i,cls=DecimalEncoder))['flat']
        vehicle_no = eval(json.dumps(i,cls=DecimalEncoder))['vehicle_no']
        model = eval(json.dumps(i,cls=DecimalEncoder))['model']
        brand = eval(json.dumps(i,cls=DecimalEncoder))['brand']
        types  = eval(json.dumps(i,cls=DecimalEncoder))['types']
        rfid = eval(json.dumps(i,cls=DecimalEncoder))['rfid']
        table = dynamodb.Table('boom_barrier_data')
        response1  = table.query(KeyConditionExpression=Key('rfid').eq(rfid) & Key('timestamp').between(start_epoch, end_epoch))
        for k in response1['Items']:
            stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(k,cls=DecimalEncoder))["timestamp"]+19800))
            in_out = eval(json.dumps(i,cls=DecimalEncoder))["types"]
            results['results'].append({'flat':flat_number,'vehicle_no':vehicle_no,'model':model,'brand':brand,'vehicle_type':types,'rfid':rfid,'time':stamp,'IN/OUT':in_out})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def amenity_list(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_info')
    response = table.query(KeyConditionExpression=Key('project').eq(project))
    for i in response['Items']:
        for j in range(int(eval(json.dumps(i,cls=DecimalEncoder))["amenities"])):
            results['results'].append(eval(json.dumps(i,cls=DecimalEncoder))["services"][j]) 
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def amenity_by_access_id(event):
    results = {'results':[]}
    ids = event['queryStringParameters']['id']
    project = event['queryStringParameters']['project']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table1 = dynamodb.Table('amenities_info')
    response1 = table1.query(KeyConditionExpression=Key('project').eq(project))
    stamps = {}
    amenities = []
    for i in response1['Items']:
        for j in range(int(eval(json.dumps(i,cls=DecimalEncoder))["amenities"])):
            amenities.append(eval(json.dumps(i,cls=DecimalEncoder))["services"][j])
            stamps[eval(json.dumps(i,cls=DecimalEncoder))["services"][j]+"IN"] = list()
            stamps[eval(json.dumps(i,cls=DecimalEncoder))["services"][j]+"OUT"] = list()
    table2 = dynamodb.Table('amenities_flat_info')
    resp2 = table2.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_access_flat_project",
    KeyConditionExpression=Key('project').eq(project),)
    for k in resp2['Items']:
        if eval(json.dumps(k,cls=DecimalEncoder))["access_card_id"]==ids:
            flat = eval(json.dumps(k,cls=DecimalEncoder))["flat"]           
    table3 = dynamodb.Table('amenities_data')
    response3  = table3.query(KeyConditionExpression=Key('access_id').eq(ids) & Key('timestamp').between(start_epoch, end_epoch))
    for l in response3['Items']:
        stamps[eval(json.dumps(l,cls=DecimalEncoder))["amenity"]+eval(json.dumps(l,cls=DecimalEncoder))["types"]].append(eval(json.dumps(l,cls=DecimalEncoder))["timestamp"])
        stamps[eval(json.dumps(l,cls=DecimalEncoder))["amenity"]+eval(json.dumps(l,cls=DecimalEncoder))["types"]].sort()
    for m in amenities:
        key1 = m+'IN'
        key2 = m+'OUT'
        if len(stamps[key1]) == len(stamps[key2]) and len(stamps[key1])!=0 and len(stamps[key2])!=0:
            for n in range(len(stamps[key1])):
                in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][n]+19800))
                out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][n]+19800))
                results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
        elif len(stamps[key1])==len(stamps[key2]) and len(stamps[key1])==0 and len(stamps[key2])==0:
            pass
        elif len(stamps[key1])!= len(stamps[key2]):
            if len(stamps[key1])-len(stamps[key2])>0:
                for n in range(len(stamps[key1])-len(stamps[key2])):
                    stamps[key2].append("NA")
                for h in range(len(stamps[key1])):
                    if stamps[key2][h]!="NA":
                        if stamps[key1][h]>stamps[key2][h]:
                            a = stamps[key1][h]
                            stamps[key1][h] = stamps[key2][h]
                            stamps[key2][h] = a
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][h]+19800))
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][h]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
                    else:
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][h]+19800))
                        out_time = 'NA'
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
            else:
                for n in range(len(stamps[key2])-len(stamps[key1])):
                    stamps[key1].append("NA")
                for g in range(len(stamps[key1])):
                    if stamps[key1][g]!="NA":
                        if stamps[key1][g]>stamps[key2][g]:
                            a = stamps[key1][g]
                            stamps[key1][g] = stamps[key2][g]
                            stamps[key2][g] = a
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][g]+19800))
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][g]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
                    else:
                        in_time = 'NA'
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][g]+19800)) 
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def amenity_by_flat(event):
    results = {'results':[]}
    flat = event['queryStringParameters']['flat']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table2 = dynamodb.Table('amenities_flat_info')
    response2 = table2.query(KeyConditionExpression=Key('flat').eq(flat))
    for i in response2['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["flat"]==flat:
            ids = eval(json.dumps(i,cls=DecimalEncoder))["access_card_id"]
    project = event['queryStringParameters']['project']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    table1 = dynamodb.Table('amenities_info')
    response1 = table1.query(KeyConditionExpression=Key('project').eq(project))
    stamps = {}
    amenities = []
    for i in response1['Items']:
        for j in range(int(eval(json.dumps(i,cls=DecimalEncoder))["amenities"])):
            amenities.append(eval(json.dumps(i,cls=DecimalEncoder))["services"][j])
            stamps[eval(json.dumps(i,cls=DecimalEncoder))["services"][j]+"IN"] = list()
            stamps[eval(json.dumps(i,cls=DecimalEncoder))["services"][j]+"OUT"] = list()           
    table3 = dynamodb.Table('amenities_data')
    response3  = table3.query(KeyConditionExpression=Key('access_id').eq(ids) & Key('timestamp').between(start_epoch, end_epoch))
    for l in response3['Items']:
        stamps[eval(json.dumps(l,cls=DecimalEncoder))["amenity"]+eval(json.dumps(l,cls=DecimalEncoder))["types"]].append(eval(json.dumps(l,cls=DecimalEncoder))["timestamp"])
        stamps[eval(json.dumps(l,cls=DecimalEncoder))["amenity"]+eval(json.dumps(l,cls=DecimalEncoder))["types"]].sort()
    for m in amenities:
        key1 = m+'IN'
        key2 = m+'OUT'
        if len(stamps[key1]) == len(stamps[key2]) and len(stamps[key1])!=0 and len(stamps[key2])!=0:
            for n in range(len(stamps[key1])):
                in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][n]+19800))
                out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][n]+19800))
                results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
        elif len(stamps[key1])==len(stamps[key2]) and len(stamps[key1])==0 and len(stamps[key2])==0:
            pass
        elif len(stamps[key1])!= len(stamps[key2]):
            if len(stamps[key1])-len(stamps[key2])>0:
                for n in range(len(stamps[key1])-len(stamps[key2])):
                    stamps[key2].append("NA")
                for h in range(len(stamps[key1])):
                    if stamps[key2][h]!="NA":
                        if stamps[key1][h]>stamps[key2][h]:
                            a = stamps[key1][h]
                            stamps[key1][h] = stamps[key2][h]
                            stamps[key2][h] = a
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][h]+19800))
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][h]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
                    else:
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][h]+19800))
                        out_time = 'NA'
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
            else:
                for n in range(len(stamps[key2])-len(stamps[key1])):
                    stamps[key1].append("NA")
                for g in range(len(stamps[key1])):
                    if stamps[key1][g]!="NA":
                        if stamps[key1][g]>stamps[key2][g]:
                            a = stamps[key1][g]
                            stamps[key1][g] = stamps[key2][g]
                            stamps[key2][g] = a
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key1][g]+19800))
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][g]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
                    else:
                        in_time = 'NA'
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamps[key2][g]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def amenity_by_amenity(event):
    results = {'results':[]}
    amenity = event['queryStringParameters']['amenity']
    project = event['queryStringParameters']['project']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    card = {}
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_data')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_access_data_project",
    KeyConditionExpression=Key('amenity').eq(amenity) & Key('timestamp').between(start_epoch, end_epoch),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["access_id"] not in card.keys():
            card[eval(json.dumps(i,cls=DecimalEncoder))["access_id"]] = [list(),list()]
            if eval(json.dumps(i,cls=DecimalEncoder))["types"] =="IN":
                card[eval(json.dumps(i,cls=DecimalEncoder))["access_id"]][0].append(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["types"] =="OUT":
                card[eval(json.dumps(i,cls=DecimalEncoder))["access_id"]][1].append(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"])
        else:
            if eval(json.dumps(i,cls=DecimalEncoder))["types"] =="IN":
                card[eval(json.dumps(i,cls=DecimalEncoder))["access_id"]][0].append(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["types"] =="OUT":
                card[eval(json.dumps(i,cls=DecimalEncoder))["access_id"]][1].append(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"])        
    for key,values in card.items():
        flat = ''
        card[key][0].sort()
        card[key][1].sort()
        table1 =  dynamodb.Table('amenities_flat_info')
        resp1 = table1.query(
        # Add the name of the index you want to use in your query.
        IndexName="query_access_flat_project",
        KeyConditionExpression=Key('project').eq(project),)
        for i in resp1['Items']:
            if key==eval(json.dumps(i,cls=DecimalEncoder))["access_card_id"]:
                flat = eval(json.dumps(i,cls=DecimalEncoder))["flat"]
                break
        if len(card[key][0]) == len(card[key][0]) and len(card[key][0])!=0 and len(card[key][0])!=0:
            for n in range(len(card[key][0])):
                in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][0][n]+19800))
                out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][1][n]+19800))
                results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':key,'amenity':amenity})
        elif len(card[key][0])==len(card[key][0]) and len(card[key][0])==0 and len(card[key][0])==0:
            pass
        elif len(card[key][0])!= len(card[key][1]):
            if len(card[key][0])-len(card[key][1])>0:
                for n in range(len(card[key][0])-len(card[key][1])):
                    card[key][1].append("NA")
                for h in range(len(card[key][0])):
                    if card[key][1]!="NA":
                        if card[key][0][h]>card[key][1][h]:
                            a = card[key][0][h]
                            card[key][0][h] = card[key][1][h]
                            card[key][1][h] = a
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][0][h]+19800))
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][0][h]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':key,'amenity':amenity})
                    else:
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][0][h]+19800))
                        out_time = 'NA'
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':ids,'amenity':m})
            else:
                for n in range(len(card[key][1])-len(card[key][0])):
                    card[key][0].append("NA")
                for g in range(len(card[key][0])):
                    if card[key][0][g]!="NA":
                        if card[key][0][g]>card[key][1][g]:
                            a = card[key][0][g]
                            card[key][0][g] = card[key][1][g]
                            card[key][1][g] = a
                        in_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][0][g]+19800))
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][1][g]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':key,'amenity':amenity})
                    else:
                        in_time = 'NA'
                        out_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card[key][1][g]+19800))
                        results['results'].append({'flat':flat,'IN':in_time,'OUT':out_time,'access_id':key,'amenity':amenity})        
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def access_card_by_id(event):
    results = {'results':[]}
    ids = event['queryStringParameters']['id']
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table1 =  dynamodb.Table('amenities_flat_info')
    resp1 = table1.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_access_flat_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp1['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["access_card_id"]==ids:
            results['results'].append({'flat':eval(json.dumps(i,cls=DecimalEncoder))["flat"],'id':ids})
            break
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def access_card_by_flat(event):
    results = {'results':[]}
    flat = event['queryStringParameters']['wing'] + event['queryStringParameters']['flat']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table1 =  dynamodb.Table('amenities_flat_info')
    response1 = table1.query(KeyConditionExpression=Key('flat').eq(flat))
    for i in response1['Items']:
        results['results'].append({'flat':eval(json.dumps(i,cls=DecimalEncoder))["flat"],'id':eval(json.dumps(i,cls=DecimalEncoder))["access_card_id"]})
        break
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def access_card_list_for_deassign(event):
    results = {'results':[]}
    flat = event['queryStringParameters']['wing'] + event['queryStringParameters']['flat']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table1 =  dynamodb.Table('amenities_flat_info')
    response1 = table1.query(KeyConditionExpression=Key('flat').eq(flat))
    for i in response1['Items']:
        results['results'].append({'id':eval(json.dumps(i,cls=DecimalEncoder))["access_card_id"]})
        break
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def delete_access_card(event):
    flat = event["queryStringParameters"]["wing"]+event["queryStringParameters"]["flat"]
    ids = event["queryStringParameters"]["access_card_no"]
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_flat_info')
    try:
        response = table.delete_item(Key={'flat': flat,'access_card_id': ids}) 
    except Exception as e:
        return {'statusCode':400,'body':json.dumps("Card deletion failed"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps("card deleted successfully"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}        


def amenity_month_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    monthly_graph = {}
    amenity = event['queryStringParameters']['amenity']
    epochs=[]
    for i in range(30):
        a = now-timedelta(days=i)
        monthly_graph[str(i+1)] = 0
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),str(i+1)])
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_data')
    for j in epochs:
        resp = table.query(
        # Add the name of the index you want to use in your query.
        IndexName="query_access_data_project",
        KeyConditionExpression=Key('amenity').eq(amenity) & Key('timestamp').between(j[0],j[1]),)
        for i in resp['Items']:
            if eval(json.dumps(i,cls=DecimalEncoder))["types"]=="IN":
                monthly_graph[j[2]] += 1            
    return {'statusCode':200,'body':json.dumps(monthly_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def amenity_peak_graph(event):
    monthly_peak_graph = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,
    "15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0}
    amenity = event['queryStringParameters']['amenity']
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('amenities_data')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_access_data_project",
    KeyConditionExpression=Key('amenity').eq(amenity),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["types"]=="IN" and eval(json.dumps(i,cls=DecimalEncoder))["project"]== project:
            a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
            monthly_peak_graph[str(int(a[11:13]))] +=1
    results = {'results':monthly_peak_graph}        
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}       

def get_billing_data(event):
    results = {}
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('billing_date')
    resp = table.scan()
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["days"] not in results.keys():
            results[int(eval(json.dumps(i,cls=DecimalEncoder))["days"])] = list()
            results[int(eval(json.dumps(i,cls=DecimalEncoder))["days"])].append(eval(json.dumps(i,cls=DecimalEncoder))["project"])
        else:
            results[int(eval(json.dumps(i,cls=DecimalEncoder))["days"])].append(eval(json.dumps(i,cls=DecimalEncoder))["project"])
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def generate_bills(event):
    results = {}
    a = eval(event['body'])
    wing = a['wing']
    flat = a['flat']+'-'+str(a['month'])+"-"+ str(a['year'])
    bill_id = a['id']
    month = a['month']
    year = a['year']
    amount = a['amount']
    project = a['project'] 
    tax = a['tax']
    duration = a['duration']
    consumption = a['consumption']
    charges = a['charges']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('billings')
    try:
        response = table.put_item(Item={'wing':wing,'flat':flat ,'bill_id':bill_id,'month':month,'year':year,'project':project,'amount':amount,'tax':decimal.Decimal(str(tax)),'duration':duration,'consumption':consumption,'charges':decimal.Decimal(str(charges))})
        results['message']=200
    except Exception as e:
        print(e)
        results['message'] = 400
        return {'statusCode':400,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   

def bill_by_default(event):
    results = {'results':[]}
    months = []
    now = datetime.now() + timedelta(minutes=330)
    current_month = now.month
    current_year = now.year
    if current_month>=7:
        for i in range(6):
            months.append([current_month-(i+1),current_year])
    elif current_month==6:
        months = [[5,current_year],[4,current_year],[3,current_year],[2,current_year],[1,current_year],[12,current_year-1]]
    elif current_month==5:
        months = [[4,current_year],[3,current_year],[2,current_year],[1,current_year],[12,current_year-1],[11,current_year-1]]    
    elif current_month==4:
        months = [[3,current_year],[2,current_year],[1,current_year],[12,current_year-1],[11,current_year-1],[10,current_year-1]]
    elif current_month==3:
        months = [[2,current_year],[1,current_year],[12,current_year-1],[11,current_year-1],[10,current_year-1],[9,current_year-1]]
    elif current_month==2:
        months = [[1,current_year],[12,current_year-1],[11,current_year-1],[10,current_year-1],[9,current_year-1],[8,current_year-1]]
    elif current_month==1:
        months = [[12,current_year-1],[11,current_year-1],[10,current_year-1],[9,current_year-1],[8,current_year-1],[7,current_year-1]]
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    for j in months:
        wing = event['queryStringParameters']['wing']
        flat = event['queryStringParameters']['flat']+'-'+str(j[0])+'-'+str(j[1])
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('billings')
        response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
        print(response)
        for i in response["Items"]:
            flat = event['queryStringParameters']['wing']+event['queryStringParameters']['flat']
            duration = eval(json.dumps(i,cls=DecimalEncoder))["duration"]
            consumption = eval(json.dumps(i,cls=DecimalEncoder))["consumption"]
            charges = eval(json.dumps(i,cls=DecimalEncoder))["charges"]
            tax = eval(json.dumps(i,cls=DecimalEncoder))["tax"]
            total = eval(json.dumps(i,cls=DecimalEncoder))["amount"]
            bill_id = eval(json.dumps(i,cls=DecimalEncoder))["bill_id"]
            results['results'].append({'flat':flat,'duration':duration,'consumption':consumption,'charges_for_consumption':charges,'tax':tax,'total_bill':total,'invoice-no':bill_id})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def bill_by_month(event):
    results = {'results':[]}
    month_map = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,
    'October':10,'November':11,'December':12}
    current_month = month_map[event['queryStringParameters']['month']]
    year = event['queryStringParameters']['year']
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']+'-'+str(current_month)+'-'+str(year)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('billings')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response['Items']:
        flat = event['queryStringParameters']['wing']+event['queryStringParameters']['flat']
        duration = eval(json.dumps(i,cls=DecimalEncoder))["duration"]
        consumption = eval(json.dumps(i,cls=DecimalEncoder))["consumption"]
        charges = eval(json.dumps(i,cls=DecimalEncoder))["charges"]
        tax = eval(json.dumps(i,cls=DecimalEncoder))["tax"]
        total = eval(json.dumps(i,cls=DecimalEncoder))["amount"]
        bill_id = eval(json.dumps(i,cls=DecimalEncoder))["bill_id"]
        results['results'].append({'flat':flat,'duration':duration,'consumption':consumption,'charges_for_consumption':charges,'tax':tax,'total_bill':total,'invoice-no':bill_id})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}    

def get_flat_count(event):
    results = {}
    project = event['queryStringParameters']['project']
    temp = populate_wings_list(event)
    wing_list = eval(temp['body'])['wings']
    count = 0
    for i in wing_list:
        event['queryStringParameters']['wing'] = i
        temp = populate_flat_list(event)
        flat_list = eval(temp['body'])['flats']
        count += len(flat_list)
    results['flats_count'] = count    
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}



def upload_csv(event):
    results = {}
    project = event['queryStringParameters']['project']
    month = int(event['queryStringParameters']['month'])
    year = int(event['queryStringParameters']['year'])
    import os
    os.chdir('/tmp')
    BUCKET_NAME = 'crafting-cloud-formation' # replace with your bucket name
    KEY = 'excel_bills/'+str(project)+'-'+str(month)+'-'+str(year)+".csv" # replace with your object key
    with open('data_csv', "w") as file:
        csv_file = csv.writer(file)
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('billings')
        resp = table.query(
        # Add the name of the index you want to use in your query.
        IndexName="query_billing_project",
        KeyConditionExpression=Key('project').eq(project),)
        csv_file.writerow(['wing', 'flat','consumption','usage_charges','tax','Period','Total Bill','Invoice No'])
        for i in resp['Items']:
            if eval(json.dumps(i,cls=DecimalEncoder))["month"]==month and eval(json.dumps(i,cls=DecimalEncoder))["year"]==year:
                csv_file.writerow([str(eval(json.dumps(i,cls=DecimalEncoder))["wing"]),str(eval(json.dumps(i,cls=DecimalEncoder))["flat"][0:3]),str(eval(json.dumps(i,cls=DecimalEncoder))["consumption"]),str(eval(json.dumps(i,cls=DecimalEncoder))["charges"]),str(eval(json.dumps(i,cls=DecimalEncoder))["tax"]),str(eval(json.dumps(i,cls=DecimalEncoder))["duration"]),str(eval(json.dumps(i,cls=DecimalEncoder))["amount"]),str(eval(json.dumps(i,cls=DecimalEncoder))["bill_id"])])
    csv_binary = open('data_csv', 'rb').read()
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(BUCKET_NAME, KEY)
        obj.put(Body=csv_binary)
        if os.path.isfile('data_csv'):
            os.remove('data_csv')
        results['message'] = 'csv bill uploaded successfully'  
        return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        results['message'] = 400
        return {'statusCode':400,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def download_csv(event):
    results = {}
    project = event['queryStringParameters']['project']
    month_map = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,
    'October':10,'November':11,'December':12}
    month = month_map[event['queryStringParameters']['month']]
    year = event['queryStringParameters']['year']
    BUCKET_NAME = 'crafting-cloud-formation'
    KEY = 'excel_bills/'+str(project)+'-'+str(month)+'-'+str(year)+'.csv'
    s3client = boto3.client('s3')
    try:
        download_url = s3client.generate_presigned_url(
                         'get_object',
                          Params={
                              'Bucket': BUCKET_NAME,
                              'Key': KEY
                              },
                          ExpiresIn=300
        )
        results['csv_link'] = download_url
        return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("Bill not found"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    

def check_tmp(event):
    import os
    os.chdir('/tmp')
    files = os.listdir(os.curdir)
    print(files)
    return {'statusCode':200,'body':json.dumps('ok'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def upload_image(event):
    import os
    os.chdir('/tmp')
    s3_client = boto3.client('s3')
    files = os.listdir(os.curdir)
    print(files)
    s3_client.download_file('crafting-cloud-formation', 'Capture.JPG',os.curdir+'/image.jpg')
    files = os.listdir(os.curdir)
    print(files)
    return {'statusCode':200,'body':json.dumps('ok'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    
def upload_pdf(event):
    now = datetime.now() + timedelta(minutes=330)
    results ={}
    import os
    data=[]
    os.chdir('/tmp')
    project = event['queryStringParameters']['project']
    month = event['queryStringParameters']['month']
    year = event['queryStringParameters']['year']
    total = event['queryStringParameters']['total']
    duration = ''
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table1 =  dynamodb.Table('billing_date')
    response1 = table1.query(KeyConditionExpression=Key('project').eq(project))
    for i in response1['Items']:
        address = eval(json.dumps(i,cls=DecimalEncoder))["address"]
    table = dynamodb.Table('billings')
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_billing_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        if str(eval(json.dumps(i,cls=DecimalEncoder))["month"])==str(month) and str(eval(json.dumps(i,cls=DecimalEncoder))["year"])==str(year):
            data.append([str(eval(json.dumps(i,cls=DecimalEncoder))["wing"])+str(eval(json.dumps(i,cls=DecimalEncoder))["flat"][0:3]),str(eval(json.dumps(i,cls=DecimalEncoder))["consumption"]),str(eval(json.dumps(i,cls=DecimalEncoder))["charges"]),str(eval(json.dumps(i,cls=DecimalEncoder))["tax"]),str(eval(json.dumps(i,cls=DecimalEncoder))["amount"]),str(eval(json.dumps(i,cls=DecimalEncoder))["bill_id"])])
            duration = str(eval(json.dumps(i,cls=DecimalEncoder))["duration"])
    s3_client = boto3.client('s3')
    s3_client.download_file('crafting-cloud-formation', 'Crafting Innovation _logo (1).jpg',os.curdir+'/image1.jpg')
    s3_client.download_file('crafting-cloud-formation', 'footer.JPG',os.curdir+'/footer1.jpg')
    BUCKET_NAME = 'crafting-cloud-formation'
    KEY = 'pdf_bills/'+str(project)+'-'+str(month)+'-'+str(year)+'.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.image('footer1.jpg',x=-3, y=0, w=220,h=28)
    pdf.image('image1.jpg', x=57, y=0, w=95)
    pdf.set_font("Arial", size=8)
    pdf.ln(30)
    txt = "Diamond District Office Building, HAL Old, Airport Rd, ISRO Colony, Kodihalli, Bengaluru, Karnataka 560017"
    pdf.cell(0, 10, txt=txt, ln=1, align="C")
    pdf.set_font("Arial", size=14,style='B')
    pdf.ln(1)
    pdf.cell(180, 10, txt="Crafting Innovation Water Service Statement", ln=1, align="R")
    pdf.set_line_width(1)
    pdf.set_draw_color(26, 214, 32)
    pdf.line(70, 70, 200, 70)
    pdf.set_font("Arial", size=12,style='B')
    pdf.cell(180, 10, txt="Statement Summary",  align="R")
    pdf.ln(8)
    pdf.set_font("Arial", size=7,style='B')
    pdf.cell(180, 10, txt="Billing Address : {}".format(address),  align="R")
    pdf.ln(5)
    pdf.set_font("Arial", size=10,style='B')
    pdf.cell(180, 10, txt="Statement Date : {}".format(str(now.day)+'-'+str(now.month)+'-'+str(now.year)),  align="R")
    pdf.ln(5)
    pdf.cell(180, 10, txt="Statement Number : {}".format(project+'-'+str(month)+'-'+str(year)),  align="R")
    pdf.ln(5)
    pdf.cell(180, 10, txt="Total Collection : Rs. {}".format(str(total)),  align="R")
    pdf.ln(5)
    pdf.cell(180, 10, txt="Billing Duration : {}".format(duration),  align="R")
    pdf.ln(13)
    pdf.set_font("Arial", size=8,style='B')
    pdf.cell(80, 10, txt="Greetings from Crafting Innovation Private Ltd. We are writing to provide you with an summary of water usage for all residents of your apartment." ,  align="L")
    pdf.ln(3)
    pdf.cell(80, 10, txt="In case of any queries feel free to contact us to help us serve you better" ,  align="L")
    pdf.ln(15)
    header = [['Flat', 'Consumption', 'Usage charges', 'Tax','Total','Invoice No']]
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_font("Arial", size=9,style='B')
    pdf. set_text_color(26, 214, 32)
    col_width = pdf.w / 8.3
    invoice_col_width = pdf.w/3
    row_height = pdf.font_size+2
    for row in header:
        count=0
        for item in row:
            count = count+1
            if count==6:
                pdf.cell(invoice_col_width, row_height*1,
                     txt=item, border=1)
            else:
                pdf.cell(col_width, row_height*1,
                     txt=item, border=1)      
        pdf.ln(row_height*1)
    pdf.ln(3)
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_font("Arial", size=8,style='B')
    pdf. set_text_color(0, 0, 0)
    col_width = pdf.w / 8.3
    invoice_col_width = pdf.w/3
    row_height = pdf.font_size+5
    for row in data:
        count=0
        for item in row:
            count = count+1
            if count==6:
                pdf.cell(invoice_col_width, row_height*1,
                     txt=item, border=1)
            else:
                pdf.cell(col_width, row_height*1,
                     txt=item, border=1)      
        pdf.ln(row_height*1)
    pdf.output('bill.pdf')
    try:
        s3_client.upload_file('/tmp/bill.pdf',BUCKET_NAME,KEY)
        os.remove('bill.pdf')
        os.remove('footer1.jpg')
        os.remove('image1.jpg')
        results['message']='pdf file uploaded successfully'
        return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        results['message'] = e
        return {'statusCode':400,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
        
def download_pdf(event):
    results = {}
    project = event['queryStringParameters']['project']
    month_map = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,
    'October':10,'November':11,'December':12}
    month = month_map[event['queryStringParameters']['month']]
    year = event['queryStringParameters']['year']
    BUCKET_NAME = 'crafting-cloud-formation'
    KEY = 'pdf_bills/'+str(project)+'-'+str(month)+'-'+str(year)+'.pdf'
    s3client = boto3.client('s3')
    try:
        download_url = s3client.generate_presigned_url(
                         'get_object',
                          Params={
                              'Bucket': BUCKET_NAME,
                              'Key': KEY
                              },
                          ExpiresIn=300
        )
        results['pdf_link'] = download_url
        return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
    except Exception as e:
        print(e)
        return {'statusCode':400,'body':json.dumps("Bill not found"),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def get_light_area(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("light_data")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_light_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        results['results'].append(eval(json.dumps(i,cls=DecimalEncoder))["Area"])
        
    return{'statusCode':400,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def get_light_status(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    area = event['queryStringParameters']['area']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("light_data")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_light_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["Area"]==area:
            ids = eval(json.dumps(i,cls=DecimalEncoder))["light_id"]
            number = eval(json.dumps(i,cls=DecimalEncoder))["no_of_units"]
            status = eval(json.dumps(i,cls=DecimalEncoder))["statuss"]
            # selecting any random birthday i.e mine 
            s = datetime(2020,5,13,int(eval(json.dumps(i,cls=DecimalEncoder))["timings"][0]),int(eval(json.dumps(i,cls=DecimalEncoder))["timings"][1]),0) + timedelta(minutes=int(eval(json.dumps(i,cls=DecimalEncoder))["timings"][2])*60+int(eval(json.dumps(i,cls=DecimalEncoder))["timings"][3]))
            end_hour = s.hour
            end_minute = s.minute
            if end_hour<10:
                end_hour = '0'+str(end_hour)
            else:
                end_hour = str(end_hour)
            if end_minute<10:
                end_minute = '0'+str(end_minute)
            else:
                end_minute = str(end_minute)
            schedule = str(eval(json.dumps(i,cls=DecimalEncoder))["timings"][0])+":"+str(eval(json.dumps(i,cls=DecimalEncoder))["timings"][1])+' to '+end_hour+':'+end_minute
            results['results'].append({'area':area,'device_id':ids,'number':number,'status':status,'schedule':schedule})    
    return {'statusCode':400,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def set_light_status(event):
    project = event['queryStringParameters']['project']
    area = event['queryStringParameters']['area']
    status = event['queryStringParameters']['status']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("light_data")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_light_project",
    KeyConditionExpression=Key('project').eq(project),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["Area"]==area:
            ids = eval(json.dumps(i,cls=DecimalEncoder))["light_id"]
            try:
                response = table.update_item(Key={'Area': area,'light_id': ids},UpdateExpression="set statuss = :a",ExpressionAttributeValues={':a': status},ReturnValues="UPDATED_NEW")
                return {'statusCode':200,'body':json.dumps('Updated Successfully'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
            except Exception as e:
                return{'statusCode':400,'body':json.dumps('Failed to Update Status'),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def get_tickets_count(event):
    results = {}
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("tickets")
    count_total = 0
    count_process = 0
    count_resolved = 0
    count_hold = 0
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_helpdesk_project",
    KeyConditionExpression=Key('project').eq(project) & Key('statuss').eq('InProcess'),)
    for i in resp['Items']:
        count_process+=1
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_helpdesk_project",
    KeyConditionExpression=Key('project').eq(project) & Key('statuss').eq('Resolved'),)
    for i in resp['Items']:
        count_resolved+=1  
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_helpdesk_project",
    KeyConditionExpression=Key('project').eq(project) & Key('statuss').eq('Hold'),)
    for i in resp['Items']:
        count_hold+=1 
    results['total'] = count_hold+count_process+count_resolved 
    results['InProcess']  = count_process
    results['Resolved'] = count_resolved
    results['Hold'] = count_hold
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}} 

def get_inprocess_tickets(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("tickets")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_helpdesk_project",
    KeyConditionExpression=Key('project').eq(project) & Key('statuss').eq('InProcess'),)
    for i in resp['Items']:
        flat = eval(json.dumps(i,cls=DecimalEncoder))["flat"]
        subject = eval(json.dumps(i,cls=DecimalEncoder))["Subject"]
        description = eval(json.dumps(i,cls=DecimalEncoder))["Description"]
        created_At = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        results['results'].append({'flat':flat,'subject':subject,'Desciption':description,'status':'InProcess','createdAt':created_At})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}} 

def get_hold_tickets(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("tickets")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_helpdesk_project",
    KeyConditionExpression=Key('project').eq(project) & Key('statuss').eq('Hold'),)
    for i in resp['Items']:
        flat = eval(json.dumps(i,cls=DecimalEncoder))["flat"]
        subject = eval(json.dumps(i,cls=DecimalEncoder))["Subject"]
        description = eval(json.dumps(i,cls=DecimalEncoder))["Description"]
        created_At = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
        results['results'].append({'flat':flat,'subject':subject,'Desciption':description,'status':'Hold','createdAt':created_At})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}} 

    
def scan_device_alerts(event):
    # getting the exact timestamp so no +330 minutes
    # +330 is done when when we need the hour minutes or day etc
    # but in timstamp same timestamp without +330 gives time in UTC 
    # and in local where time is +5:30 hrs from UTC.
    now = int(datetime.now().timestamp())
    results = {}
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("device_alerts")
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
            for i in response["Items"]:
                if (now - eval(json.dumps(i,cls=DecimalEncoder))['status_timestamp'])>7200:
                    if eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="K" or eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="B" or eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="M":
                        service = 'Smart-Water-Meter'
                    elif eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="S":
                        service = 'Smart-Sprinkler'
                    elif eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="L":
                        service = 'Smart-Lighting'       
                    table1 = dynamodb.Table("service_alerts")
                    response1 = table1.put_item(Item={'device_id': eval(json.dumps(i,cls= DecimalEncoder))['device_id'],'timestamp':now,'project':eval(json.dumps(i,cls= DecimalEncoder))['project'],'area_or_flat':eval(json.dumps(i,cls=DecimalEncoder))['area'],'service':service,'alert':'Device went in offline State','Last_seen':int(eval(json.dumps(i,cls=DecimalEncoder))['status_timestamp'])})    
        else: 
            response = table.scan()
            for i in response["Items"]:
                if (now-eval(json.dumps(i,cls=DecimalEncoder))['status_timestamp'])>7200:
                    if eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="K" or eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="B" or eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="M":
                        service = 'Smart-Water-Meter'
                    elif eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="S":
                        service = 'Smart-Sprinkler'
                    elif eval(json.dumps(i,cls=DecimalEncoder))['device_id'][-1]=="L":
                        service = 'Smart-Lighting'       
                    table1 = dynamodb.Table("service_alerts")
                    response1 = table1.put_item(Item={'device_id': eval(json.dumps(i,cls= DecimalEncoder))['device_id'],'timestamp':now,'project':eval(json.dumps(i,cls= DecimalEncoder))['project'],'area_or_flat':eval(json.dumps(i,cls=DecimalEncoder))['area'],'service':service,'alert':'Device went in offline State','Last_seen':int(eval(json.dumps(i,cls=DecimalEncoder))['status_timestamp'])})
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            # Do when all the elements have been scanned 
            results['message'] = 'Service alerts check completed'
            break            
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   

def service_alerts_today(event):
    now = datetime.now() + timedelta(minutes=330)
    results = {}
    starting_epoch_today = int(datetime(now.year,now.month,now.day,0,0,0).timestamp()-19800)
    end_epoch_today = int(datetime(now.year,now.month,now.day,23,59,59).timestamp()-19800)  
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
    table = dynamodb.Table("service_alerts")
    resp = table.query(
    # Add the name of the index you want to use in your query.
    IndexName="query_service_alert_project",
    KeyConditionExpression=Key('project').eq(project) & Key('timestamp').between(starting_epoch_today,end_epoch_today),)
    count = 0
    for i in resp['Items']:
        count = count+1
    results['alerts_today'] = count   
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}   

def service_alerts_last_7_days(event):
    week_end = datetime.now() + timedelta(minutes=330)
    week_start = week_end - timedelta(days=6)
    results = {}
    end_epoch= int(datetime(week_end.year,week_end.month,week_end.day,23,59,59).timestamp()-19800)
    starting_epoch = int(datetime(week_start.year,week_start.month,week_start.day,0,0,0).timestamp()-19800)
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
    table = dynamodb.Table('service_alerts')
    resp = table.query(
    # Add the name of the index you want to use in your query
    IndexName='query_service_alert_project',
    KeyConditionExpression=Key('project').eq(project) & Key('timestamp').between(starting_epoch,end_epoch),)
    count = 0
    for i in resp['Items']:
        count = count+1
    results['alerts_last_7_days']  = count    
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def alerts_by_service(event):
    results = {'results':[]}
    project = event['queryStringParameters']['project']
    service = event['queryStringParameters']['service']
    start_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["date"][0:4]),int(event["queryStringParameters"]["date"][5:7]),int(event["queryStringParameters"]["date"][8:]),23,59,59).timestamp())-19800
    #print(start_epoch,end_epoch)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('service_alerts')
    resp = table.query(
    # Add the name of the index you want to use in your query
    IndexName='query_service_alert_project',
    KeyConditionExpression=Key('project').eq(project) & Key('timestamp').between(start_epoch,end_epoch),)
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))['service']==service:
            area_or_flat = eval(json.dumps(i,cls=DecimalEncoder))['area_or_flat']
            alert = eval(json.dumps(i,cls=DecimalEncoder))['alert']
            alert_generation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))
            device_last_seen = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["Last_seen"]+19800))
            results['results'].append({'area_or_flat':area_or_flat,'alert':alert,'alert_generation_time':alert_generation_time,'device_last_seen':device_last_seen,'service':service})
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def water_meter_app_dashboard(event):
    now = datetime.now() + timedelta(minutes=330)
    results = {}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    area = event['queryStringParameters']['area']
    project = event['queryStringParameters']['project']
    daily_range = int(calendar.monthrange(now.year, now.month)[1])
    if now.month<10:
        month = '0'+str(now.month)
    else:
        month = str(now.month)
    if now.day<10:
        day = '0'+str(now.day)
    else:
        day = str(now.day)
    end_date = str(now.year) + '-' + month + '-' + day
    y=0
    if event['queryStringParameters']['parameter']=="today":
        y = 1
        start_date = str(now.year) +'-'+ month + '-' + day
    elif event['queryStringParameters']['parameter']=='weekly':
        y = 2
        start = (now - timedelta(days=6)).day
        month1 = (now - timedelta(days=6)).month
        if month1<10:
            month1 = '0'+str(month1)
        else:
            month1 = str(month1)
        if start<10:
            start = '0'+str(start)
        else:
            start = str(start)
        start_date = str(now.year) +'-'+ month1 + '-' + start
    elif event['queryStringParameters']['parameter']=='monthly':
        y = 0
        start_date = str(now.year)+'-'+month+'-01'
    elif event['queryStringParameters']['parameter']=='yearly':
        y = 3
        start_date = str(now.year) + '-' + '01-01'     
    start_date_month = str(now.year)+'-'+month+'-01'
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat)) 
    limit_array = []
    for i in response['Items']:
        # monthly limit
        limit_array.append(int(eval(json.dumps(i,cls=DecimalEncoder))["limit"]))
        # daily limit
        limit_array.append(int(limit_array[0]/daily_range))
        # weekly limit
        limit_array.append(limit_array[1]*7)
        # yearly limit
        limit_array.append(limit_array[0]*12)
    print(start_date,end_date,start_date_month)    
    result = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'start':start_date,'end':end_date,'function':'bill-api-with-minimum','wing':wing,'flat':flat})
    t = result.json()
    result1 = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'start':start_date_month,'end':end_date,'function':'bill-api-with-minimum','wing':wing,'flat':flat})
    s = result1.json()
    if area == "All":
        spend = int(t['results']['total_consumption'])
        results['consumption'] = round(spend/1000)
        percentage = round(int(spend/1000)*100/limit_array[y],1)
        results['percentage'] = percentage
        results['limit'] = limit_array[y]
        results['unbilled_usage'] = s['results']["bill_for_duration"]
    else:
        area = area.lower() 
        spend = int(t['results'][area]) 
        results['consumption'] = round(spend/1000)
        percentage = round(int(spend/1000)*100/limit_array[y],1)  
        results['percentage'] = percentage
        results['limit'] = limit_array[y]
        results['unbilled_usage'] =  s['results']['bill_for_duration']    
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def water_meter_reports_app(event):
    results = {'TableData':[]}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    start_epoch = int(datetime(int(event["queryStringParameters"]["start_date"][0:4]),int(event["queryStringParameters"]["start_date"][6]),int(event["queryStringParameters"]["start_date"][8:]),0,0,0).timestamp())-19800
    end_epoch = int(datetime(int(event["queryStringParameters"]["end_date"][0:4]),int(event["queryStringParameters"]["end_date"][6]),int(event["queryStringParameters"]["end_date"][8:]),23,59,59).timestamp())-19800
    start_date = date(int(event["queryStringParameters"]["start_date"][0:4]),int(event["queryStringParameters"]["start_date"][6]),int(event["queryStringParameters"]["start_date"][8:]))
    end_date = date(int(event["queryStringParameters"]["end_date"][0:4]),int(event["queryStringParameters"]["end_date"][6]),int(event["queryStringParameters"]["end_date"][8:]))
    delta = end_date - start_date
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        results['TableData'].append([str(day),0])
        #results  
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response['Items']:
        dict1 = eval(json.dumps(i,cls=DecimalEncoder))
    del dict1['limit'],dict1['wing'],dict1['flat'],dict1['project']
    for keys,value in dict1.items():
        table = dynamodb.Table('dev-water-meter-python-backend')
        response = table.query(KeyConditionExpression=Key('device_id').eq(value['id']) & Key('timestamp').between(start_epoch,end_epoch))
        for k in response['Items']:
            for j in range(len(results['TableData'])):
                if time.strftime('%Y-%m-%d', time.localtime(eval(json.dumps(k,cls=DecimalEncoder))["timestamp"]+19800))==results['TableData'][j][0]:
                    results['TableData'][j][1] += int(eval(json.dumps(k,cls=DecimalEncoder))["consumption"])  
                    break     
    for i in results['TableData']:
        i[1] = round(i[1]/1000)
    #results = {k: round(v /1000) for k, v in results.items()}
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
     
def water_meter_today_graph(event):
    now  = datetime.now() + timedelta(minutes=330)
    today_graph = {'data':[{'x':'0','y':0},{'x':'1','y':0},{'x':'2','y':0},{'x':'3','y':0},{'x':'4','y':0},{'x':'5','y':0},{'x':'6','y':0},{'x':'7','y':0},{'x':'8','y':0},{'x':'9','y':0},{'x':'10','y':0},{'x':'11','y':0},{'x':'12','y':0},{'x':'13','y':0},{'x':'14','y':0},{'x':'15','y':0},{'x':'16','y':0},{'x':'17','y':0},{'x':'18','y':0},{'x':'19','y':0},{'x':'20','y':0},{'x':'21','y':0},{'x':'22','y':0},{'x':'23','y':0}]}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    start_epoch = int(datetime(now.year,now.month,now.day,0,0,0).timestamp()-19800)
    end_epoch = int(datetime(now.year,now.month,now.day,23,59,59).timestamp()-19800)
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response['Items']:
        dict1 = eval(json.dumps(i,cls=DecimalEncoder))
    del dict1['limit'],dict1['wing'],dict1['flat'],dict1['project']
    table = dynamodb.Table('dev-water-meter-python-backend')
    for keys,value in dict1.items():
        response = table.query(KeyConditionExpression=Key('device_id').eq(value['id']) & Key('timestamp').between(start_epoch,end_epoch))
        for k in response['Items']:
            a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(k,cls=DecimalEncoder))["timestamp"]+19800))
            today_graph['data'][int(a[11:13])]['y'] += int(eval(json.dumps(k,cls=DecimalEncoder))["consumption"])
    for i in today_graph['data']:
        i['y'] = round(i['y']/1000)
    return {'statusCode':200,'body':json.dumps(today_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}
     
def water_meter_week_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    epochs = []
    usage_graph = {'data':[{'x':(now-timedelta(days=6)).strftime('%a'),'y':0},{'x':(now-timedelta(days=5)).strftime('%a'),'y':0},{'x':(now-timedelta(days=4)).strftime('%a'),'y':0},{'x':(now-timedelta(days=3)).strftime('%a'),'y':0},{'x':(now-timedelta(days=2)).strftime('%a'),'y':0},{'x':(now-timedelta(days=1)).strftime('%a'),'y':0},{'x':now.strftime("%a"),'y':0}]}
    end_epoch = int(datetime(now.year,now.month,now.day,23,59,59).timestamp()-19800)
    for i in range(7):
        a = now-timedelta(days=i)
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),a.strftime("%a")])
        if i==6:
            start_epoch =  int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800) 
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response['Items']:
        dict1 = eval(json.dumps(i,cls=DecimalEncoder))
    del dict1['limit'],dict1['wing'],dict1['flat'],dict1['project']    
    for keys,value in dict1.items():
        table1 = dynamodb.Table('dev-water-meter-python-backend')
        resp = table1.query(KeyConditionExpression=Key('device_id').eq(value['id']) & Key('timestamp').between(start_epoch,end_epoch))
        for i in resp['Items']:
            if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[0][0],epochs[0][1]+1):
                usage_graph['data'][6]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[1][0],epochs[1][1]+1):
                usage_graph['data'][5]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[2][0],epochs[2][1]+1):
                usage_graph['data'][4]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[3][0],epochs[3][1]+1):
                usage_graph['data'][3]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])  
            elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[4][0],epochs[4][1]+1):
                usage_graph['data'][2]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"]) 
            elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[5][0],epochs[5][1]+1):
                usage_graph['data'][1]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
            elif eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[6][0],epochs[6][1]+1):
                usage_graph['data'][0]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])                         
    usage_graph['data'][0]['y'] = round(usage_graph['data'][0]['y']/1000)
    usage_graph['data'][1]['y'] = round(usage_graph['data'][1]['y']/1000)
    usage_graph['data'][2]['y'] = round(usage_graph['data'][2]['y']/1000)
    usage_graph['data'][3]['y'] = round(usage_graph['data'][3]['y']/1000)
    usage_graph['data'][4]['y'] = round(usage_graph['data'][4]['y']/1000)
    usage_graph['data'][5]['y'] = round(usage_graph['data'][5]['y']/1000)
    usage_graph['data'][6]['y'] = round(usage_graph['data'][6]['y']/1000)
    return {'statusCode':200,'body':json.dumps(usage_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}


def water_meter_month_graph(event):
    now = datetime.now() + timedelta(minutes=330)
    monthly_graph = {'data':[]}
    epochs=[]
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    end_epoch = int(datetime(now.year,now.month,now.day,23,59,59).timestamp()-19800)
    for i in range(30):
        a = now-timedelta(days=i)
        monthly_graph['data'].append({'x':str(a)[0:10],'y':0})
        epochs.append([int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800),int(datetime(a.year,a.month,a.day,23,59,59).timestamp()-19800),str(a)[0:10]])
        if i==29:
            start_epoch =  int(datetime(a.year,a.month,a.day,0,0,0).timestamp()-19800) 
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response['Items']:
        dict1 = eval(json.dumps(i,cls=DecimalEncoder))
    del dict1['limit'],dict1['wing'],dict1['flat'],dict1['project']    
    for keys,value in dict1.items():
        table1 = dynamodb.Table('dev-water-meter-python-backend')
        resp = table1.query(KeyConditionExpression=Key('device_id').eq(value['id']) & Key('timestamp').between(start_epoch,end_epoch))
        for i in resp['Items']:
            for j in range(len(epochs)):
                if eval(json.dumps(i,cls=DecimalEncoder))["timestamp"] in range(epochs[j][0],epochs[j][1]+1):
                    monthly_graph['data'][j]['y'] += int(eval(json.dumps(i,cls=DecimalEncoder))["consumption"])
                    break    
    for i in monthly_graph['data']:
        i['y'] = round(i['y']/1000)
    return {'statusCode':200,'body':json.dumps(monthly_graph),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def water_meter_last_year_consumption(event):
    now = datetime.now() + timedelta(minutes=330)
    results = {'data':[{'x':'Jan','y':0},{'x':'Feb','y':0},{'x':'Mar','y':0},{'x':'Apr','y':0},{'x':'May','y':0},{'x':'Jun','y':0},{'x':'Jul','y':0},{'x':'Aug','y':0},{'x':'Sep','y':0},{'x':'Oct','y':0},{'x':'Nov','y':0},{'x':'Dec','y':0}]}
    #map_array = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    start_epoch =  int(datetime(now.year,1,1,0,0,0).timestamp())-19800
    end_epoch = int(datetime(now.year,12,31,11,59,59).timestamp())-19800
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('project_wing_device_data')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for i in response['Items']:
        dict1 = eval(json.dumps(i,cls=DecimalEncoder))
    del dict1['limit'],dict1['wing'],dict1['flat'],dict1['project']    
    for keys,value in dict1.items():
        table1 = dynamodb.Table('dev-water-meter-python-backend')
        resp = table1.query(KeyConditionExpression=Key('device_id').eq(value['id']) & Key('timestamp').between(start_epoch,end_epoch))
        for i in resp['Items']:
            results['data'][int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eval(json.dumps(i,cls=DecimalEncoder))["timestamp"]+19800))[5:7])-1]['y'] += eval(json.dumps(i,cls=DecimalEncoder))["consumption"]
    for i in results['data']:
        i['y'] = round(i['y']/1000)
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}



def water_meter_consumption_split(event):
    now  = datetime.now() + timedelta(minutes=330)
    results = {}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    project = event['queryStringParameters']['project']
    start_date = [str(now.year) + '-' + str(now.month)+'-01' if now.month>9 else str(now.year) + '-0' + str(now.month)+'-01'][0]
    enddate_month = calendar.monthrange(now.year, now.month)[1]
    end_date = [str(now.year)+'-'+str(now.month)+str(enddate_month) if now.month>10 else str(now.year)+'-0'+str(now.month)+'-'+str(enddate_month)][0]
    result = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'start':start_date,'end':end_date,'function':'consumption-flat-wise','wing':wing,'flat':flat})
    t = result.json()
    kitchen  =  [t['results']['kitchen'] if 'kitchen' in t['results'].keys() else 0][0]
    bathroom1 = [t['results']['bathroom1'] if 'bathroom1' in t['results'].keys() else 0][0]
    bathroom2 = [t['results']['bathroom2'] if 'bathroom2' in t['results'].keys()else 0][0]
    bathroom3 = [t['results']['bathroom3'] if 'bathroom3' in t['results'].keys() else 0][0]
    misc = [t['results']['misc'] if 'misc' in t['results'].keys() else 0][0]
    bathroom_total = bathroom1+bathroom2+bathroom3
    total = t['results']['total_consumption']
    results['percentages'] = {'Kitchen':round(t['results']['kitchen']*100/total,2),'Bathroom':round(bathroom_total*100/total,2),'Misc':round(misc*100/total,2)}
    results['usage_values'] = {'Kitchen':round(kitchen/1000),'Bathroom':round(bathroom_total/1000),'Misc':round(misc/1000)}
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def water_meter_billing_unbilled(event):
    now  = datetime.now() + timedelta(minutes=330)
    results = {}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    project = event['queryStringParameters']['project']
    bathroom_contribution = 0
    start_date = [str(now.year) + '-' + str(now.month)+'-01' if now.month>10 else str(now.year) + '-0' + str(now.month)+'-01'][0]
    enddate_month = calendar.monthrange(now.year, now.month)[1]
    end_date = [str(now.year)+'-'+str(now.month)+str(enddate_month) if now.month>10 else str(now.year)+'-0'+str(now.month)+'-'+str(enddate_month)][0]
    result = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'start':start_date,'end':end_date,'function':'consumption-flat-wise','wing':wing,'flat':flat})
    t = result.json()
    total_consumption_charges = t['results']['usage_charges']
    bathroom1 = [t['results']['bathroom1'] if 'bathroom1' in t['results'].keys() else 0][0]
    bathroom2 = [t['results']['bathroom2'] if 'bathroom2' in t['results'].keys() else 0][0]
    bathroom3 = [t['results']['bathroom3'] if 'bathroom3' in t['results'].keys() else 0][0]
    bathroom_total = bathroom1+bathroom2+bathroom3
    try:
        kitchen_contribution = [round(t['results']['kitchen']*total_consumption_charges/t['results']['total_consumption'],2) if 'kitchen' in t['results'].keys() else 0][0]
        bathroom_contribution = round(bathroom_total*total_consumption_charges/t['results']['total_consumption'],2)
        misc_contribution = [round(t['results']['misc']*total_consumption_charges/t['results']['total_consumption'],2) if 'misc' in t['results'].keys() else 0][0]
    except Exception as e:
        kitchen_contribution = 0
        bathroom_contribution = 0
        misc_contribution = 0           
    results['total_usage_charges'] = total_consumption_charges
    results['bathroom_usage_charges'] = bathroom_contribution
    results['kitchen_usage_charges'] = kitchen_contribution
    results['misc_usage_charges']  = misc_contribution
    results['other_charges'] = t['results']['other_charges']
    results['tax'] = t['results']['tax']
    results['total'] = t['results']['bill_for_duration']+t['results']['other_charges']
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def water_meter_billing_three_months(event):
    now  = datetime.now() + timedelta(minutes=330)
    results = {}
    past_3_months_array = []
    past_3_months_year_array = []
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    flat1 = flat
    project = event['queryStringParameters']['project']
    if now.month>3:
        for i in range(3):
            past_3_months_array.append([now.month-(i+1) if now.month>9 else '0'+str(now.month-(i+1))][0])
            past_3_months_year_array.append(str(now.year))
    else:
        if now.month == 1:
            past_3_months_array.append('12')
            past_3_months_year_array.append(str(now.year-1))
            past_3_months_array.append('11')
            past_3_months_year_array.append(str(now.year-1))
            past_3_months_array.append('10')
            past_3_months_year_array.append(str(now.year-1))
        elif now.month == 2:
            past_3_months_array.append('01')
            past_3_months_year_array.append(str(now.year))
            past_3_months_array.append('12')
            past_3_months_year_array.append(str(now.year-1))
            past_3_months_array.append('11')
            past_3_months_year_array.append(str(now.year-1))
        elif now.month == 3:
            past_3_months_array.append('02')
            past_3_months_year_array.append(str(now.year))
            past_3_months_array.append('01')
            past_3_months_year_array.append(str(now.year))
            past_3_months_array.append('12')
            past_3_months_year_array.append(str(now.year-1))
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('billing_date')
    resp = table.scan()
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
            bill_generation_date = eval(json.dumps(i,cls=DecimalEncoder))["days"]
    data=['a','b','c']
    for i in range(3):
        month = past_3_months_array[i]
        year = past_3_months_year_array[i]
        bill_for = year + '-' + month + '-01 to ' + year + '-' + month + '-' + str(calendar.monthrange(int(year),int(month))[1])
        invoice_no = ''
        billed_date = [year+'-'+str(int(month)+1)+'-'+str(bill_generation_date) if int(month)!=12 else str(int(year)+1)+'-01-'+str(bill_generation_date)][0]
        consumption = 0
        amount = 0
        flat = flat1+'-'+month+'-'+year
        table = dynamodb.Table('billings')
        response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
        for j in response['Items']:
            invoice_no = eval(json.dumps(j,cls=DecimalEncoder))["bill_id"]
            consumption = round(eval(json.dumps(j,cls=DecimalEncoder))["consumption"]/1000)
            amount = eval(json.dumps(j,cls=DecimalEncoder))["amount"]
        results[data[i]] = {'bill_for':bill_for,'invoice_no':invoice_no,'billed_date':billed_date,'bill':amount,'consumption':round(consumption/1000)}
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}


def water_meter_billing_graph(event):
    now  = datetime.now() + timedelta(minutes=330)
    results = {'data':[{'x':'Jan','y':0},{'x':'Feb','y':0},{'x':'Mar','y':0},{'x':'Apr','y':0},{'x':'May','y':0},{'x':'Jun','y':0},{'x':'Jul','y':0},{'x':'Aug','y':0},{'x':'Sep','y':0},{'x':'Oct','y':0},{'x':'Nov','y':0},{'x':'Dec','y':0}]}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    flat1 = flat
    mapping = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(len(mapping)):
        flat = [flat1 + '-' + str(i+1)+'-'+str(now.year) if i+1>9 else flat1+'-0'+ str(i+1)+'-'+str(now.year)][0]
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        table = dynamodb.Table('billings')
        response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
        for j in response['Items']:
            results['data'][i]['y'] = eval(json.dumps(j,cls=DecimalEncoder))["amount"]
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def water_meter_bill_by_month(event):
    year = event['queryStringParameters']['date'][0:4]
    month = event['queryStringParameters']['date'][5:7]
    results = {}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    project = event['queryStringParameters']['project']
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('billing_date')
    resp = table.scan()
    for i in resp['Items']:
        if eval(json.dumps(i,cls=DecimalEncoder))["project"]==project:
            bill_generation_date = eval(json.dumps(i,cls=DecimalEncoder))["days"]
    bill_for = year + '-' + month + '-01 to ' + year + '-' + month + '-' + str(calendar.monthrange(int(year),int(month))[1])
    invoice_no = ''
    billed_date = [year+'-'+str(int(month)+1)+'-'+str(bill_generation_date) if int(month)!=12 else str(int(year)+1)+'-01-'+str(bill_generation_date)][0]
    consumption = 0
    amount = 0
    flat = flat+'-'+month+'-'+year
    table = dynamodb.Table('billings')
    response = table.query(KeyConditionExpression=Key('wing').eq(wing) & Key('flat').eq(flat))
    for j in response['Items']:
        invoice_no = eval(json.dumps(j,cls=DecimalEncoder))["bill_id"]
        consumption = round(eval(json.dumps(j,cls=DecimalEncoder))["consumption"]/1000)
        amount = eval(json.dumps(j,cls=DecimalEncoder))["amount"]
    results['result'] = {'bill_for':bill_for,'invoice_no':invoice_no,'billed_date':billed_date,'bill':amount,'consumption':round(consumption/1000)}
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}

def bill_api_with_minimum_v2(event):
    now = datetime.now()+timedelta(minutes=330)
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    project = event['queryStringParameters']['project']
    month_range = int(calendar.monthrange(now.year, now.month)[1])
    if now.month<10:
        month = '0'+str(now.month)
    else:
        month = str(now.month)
    if now.day<10:
        day = '0'+str(now.day)
    else:
        day = str(now.day)
    start_date = str(now.year) + '-' + month + '-01'
    end_date = str(now.year) + '-' + month + '-'+str(month_range)
    result = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'start':start_date,'end':end_date,'function':'bill-api-with-minimum','wing':wing,'flat':flat})
    t = result.json()
    t['results']['kitchen'] = [round(t['results']['kitchen']/1000) if 'kitchen' in t['results'].keys() else 0][0]
    t['results']['bathroom1'] = [round(t['results']['bathroom1']/1000) if 'bathroom1' in t['results'].keys() else 0][0]
    t['results']['bathroom2'] = [round(t['results']['bathroom2']/1000) if 'bathroom2' in t['results'].keys() else 0][0]
    t['results']['bathroom3'] = [round(t['results']['bathroom3']/1000) if 'bathroom3' in t['results'].keys() else 0][0]
    t['results']['misc'] = [round(t['results']['misc']/1000) if 'misc' in t['results'].keys() else 0][0]
    t['results']['total_consumption'] = round(t['results']['total_consumption']/1000)
    results = {'results':[t['results']]}
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}


def populate_device_list_v2(event):
    results = {'devices':[]}
    project = event['queryStringParameters']['project']
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    result = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'function':'device-list','wing':wing,'flat':flat})
    t = result.json()
    for keys,values in t['devices'].items():
        results['devices'].append(values)
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}    

def bill_api_with_minimum_v3(event):
    results = {'results':[]}
    wing = event['queryStringParameters']['wing']
    flat = event['queryStringParameters']['flat']
    project = event['queryStringParameters']['project']
    start_date = event['queryStringParameters']['start']
    end_date = event['queryStringParameters']['end']
    result = requests.get(url = 'https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume',params = {'project':project,'start':start_date,'end':end_date,'function':'bill-api-with-minimum','wing':wing,'flat':flat})
    t = result.json()
    t['results']['kitchen'] = [round(t['results']['kitchen']/1000) if 'kitchen' in t['results'].keys() else 0][0]
    t['results']['bathroom1'] = [round(t['results']['bathroom1']/1000) if 'bathroom1' in t['results'].keys() else 0][0]
    t['results']['bathroom2'] = [round(t['results']['bathroom2']/1000) if 'bathroom2' in t['results'].keys() else 0][0]
    t['results']['bathroom3'] = [round(t['results']['bathroom3']/1000) if 'bathroom3' in t['results'].keys() else 0][0]
    t['results']['misc'] = [round(t['results']['misc']/1000) if 'misc' in t['results'].keys() else 0][0]
    t['results']['total_consumption'] = round(t['results']['total_consumption']/1000)
    results['results'].append(t['results'])
    return {'statusCode':200,'body':json.dumps(results),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': True}}    

    
    
######################################### MAIN LAMBDA FUNCTION BEGINS HERE ###################################
def lambda_handler(event, context):
    # Endpoint for get requests  
    if event['resource']=="/resume" and event['httpMethod']=='GET':
        if event["queryStringParameters"]["function"]=="today-usage":
            # Webapp water consumption tab function
            return todays_water_usage(event)
        elif event["queryStringParameters"]["function"]=="weekly-usage":
            # Webapp water consumption tab function
            return weekly_water_usage(event) 
        elif event["queryStringParameters"]["function"]=="monthly-usage":
            # Webapp water consumption tab function
            return monthly_water_usage(event) 
        elif event["queryStringParameters"]["function"]=="yearly-usage":
            # Webapp water consumption tab function
            return yearly_water_usage(event)
        elif event["queryStringParameters"]["function"]=="week-graph":
            # Webapp water consumption tab function
            return weekly_graph(event) 
        elif event["queryStringParameters"]["function"]=="month-graph":
            # Webapp water consumption tab function
            return monthly_graph(event) 
        elif event["queryStringParameters"]["function"]=="year-graph":
            # Webapp water consumption tab function
            return year_graph(event)
        elif event["queryStringParameters"]["function"]=="wings-list":
            # webapp water consumption , solenoid valve , billings tab function
            return populate_wings_list(event)
        elif event["queryStringParameters"]["function"]=="flat-list":
            # webapp water consumption , solenoid valve , billings tab function
            return populate_flat_list(event)
        elif event["queryStringParameters"]["function"]=="device-list":
            # webapp solenoid valve tab function 
            return populate_device_list(event)
        elif event["queryStringParameters"]["function"]=="valve-status":
            # webapp solenoid valve tab function
            return user_valve_status(event) 
        elif event["queryStringParameters"]["function"]=="consumption-flat-wise":
            # webapp water consumption tab function
            return consumption_flat_wise(event)
        elif event["queryStringParameters"]["function"]=="get-meter-card":
            # webapp meter-card tab function
            return get_meter_card(event)
        elif event["queryStringParameters"]["function"]=="get-status":
            # webapp meter master tab function
            # changes to be made after discussion or extra information needs to be added 
            return get_meter_details(event)
        elif event["queryStringParameters"]["function"]=="sprinkler-area-list":
            # webapp sprinkler tab function
            return sprinkler_area_list(event)
        elif event["queryStringParameters"]["function"]=="sprinkler-valve":
            # webapp sprinkler solenoid valve information fetch  tab function
            return sprinkler_valve_info(event)
        elif event['queryStringParameters']['function']=='sprinkler-change-status':
            # webapp sprinkler solenoid valve control tab function  
            return sprinkler_valve_status_change(event)
        elif event['queryStringParameters']['function'] == 'sprinkler-today-usage':
            # webapp sprinkler todays usage function
            return sprinkler_todays_usage(event)
        elif event['queryStringParameters']['function'] =='sprinkler-weekly-usage':
            # webapp sprinkler weekly usage function
            return sprinkler_weekly_usage(event) 
        elif event['queryStringParameters']['function'] =="sprinkler-month-usage":
            # webapp sprinkler monthly usage function
            return sprinkler_month_usage(event) 
        elif event['queryStringParameters']['function'] =="sprinkler-year-usage":
            # webapp sprinkler yearly usage function
            return sprinkler_year_usage(event) 
        elif event['queryStringParameters']['function'] =='sprinkler-week-graph':
            # webapp sprinkler weekly graph function
            return sprinkler_weekly_graph(event) 
        elif event['queryStringParameters']['function']=='sprinkler-year-graph':
            # webapp sprinkler yearly graph function
            return sprinkler_yearly_graph(event)
        elif event['queryStringParameters']['function']=='sprinkler-month-graph':
            # webapp sprinkler monthly graph function
            return sprinkler_monthly_graph(event)
        elif event['queryStringParameters']['function']=='sprinkler-consumption':
            # webapp sprinkler consumption based on selection function
            return sprinkler_consumption(event)
        elif event['queryStringParameters']['function']=='boom-barrier-info-by-rfid':
            # webapp boom barrier info by rfid number method
            return boom_barrier_info_by_rfid(event) 
        elif event['queryStringParameters']['function']=='boom-barrier-info-by-flat':
            # webapp boom barrier info by wing and flat method
            return boom_barrier_info_by_flat(event)
        elif event['queryStringParameters']['function']=='get-vehicle-list':
            # webapp rfid card master deassign card vehicle list feature
            return get_vehicle_list(event)                             
        elif event['queryStringParameters']['function']=='delete-card':
            # webapp rfid card master delete card function
            return delete_rfid_card(event) 
        elif event['queryStringParameters']['function']=="rfid-monitoring":
            # webapp rfid IN/OUT monitoring based on rfid number 
            return  rfid_monitoring_by_rfid(event)
        elif event['queryStringParameters']['function']=="rfid-monitoring-by-date":
            # webapp rfid and getting all IN/OUT logs for a day based on date input
            return rfid_monitoring_by_date(event)
        elif event['queryStringParameters']['function']=="rfid-monitoring-flat":
            # webapp rfid IN/OUT monitoring based on wing and flat numbers
            return rfid_monitoring_by_flat(event)
        elif event['queryStringParameters']['function']=="amenity-list":
            # webapp populate aminity list
            return amenity_list(event) 
        elif event['queryStringParameters']['function']=="amenity-by-access-id":
            # webapp amenity IN/OUT timestamps using access card id's
            return amenity_by_access_id(event)
        elif event['queryStringParameters']['function']=="amenity-by-flat":
            # webapp amenity IN/OUT timestamps using access card id's
            return amenity_by_flat(event) 
        elif event['queryStringParameters']['function']=="amenity-by-amenity":
            # webapp amenity IN/OUT timestamps using access card id's
            return amenity_by_amenity(event)
        elif event['queryStringParameters']['function']=="access-card-by-id":
            # webapp amenity access master function
            return access_card_by_id(event)
        elif event['queryStringParameters']['function']=="access-card-by-flat":
            # webapp amenity access master function
            return access_card_by_flat(event)
        elif event['queryStringParameters']['function']=="access-card-list-for-deassign":
            # webapp amenity access master function
            return access_card_list_for_deassign(event)
        elif event['queryStringParameters']['function']=="delete-access-card":
            # webapp amenity access master function
            return delete_access_card(event) 
        elif event['queryStringParameters']['function']=="amenity-month-graph":
            # webapp amenity access master function
            return amenity_month_graph(event) 
        elif event['queryStringParameters']['function']=="amenity-peak-graph":
            # webapp amenity access master function
            return amenity_peak_graph(event)
        elif event['queryStringParameters']['function']=="get-billing-date":
            # get dates when bill needs to be generated function
            # To be used in billing thread code
            return get_billing_data(event)    
        elif event['queryStringParameters']['function']=="bill-by-default":
            # get bill for last 6 months bill for a flat from a project
            return bill_by_default(event)
        elif event['queryStringParameters']['function']=="bill-api-with-minimum":
            # get bill including the minimum charges 
            return bill_api_with_minimum_charges(event)                                     
        elif event['queryStringParameters']['function']=="bill-by-month":
            # get bill for month selected for a flat from a project
            return bill_by_month(event)
        elif event['queryStringParameters']['function']=="get-flat-count":
            # get total number of flats for a project
            return get_flat_count(event) 
        elif event['queryStringParameters']['function']=="upload-csv":
            # added in the billing api code 
            # api to generate bills excel in s3 when billing api is hit 
            return upload_csv(event)
        elif event['queryStringParameters']['function']=="check-tmp":
            # temporary function to check tmp storage of lambda function
            return check_tmp(event)
        elif event['queryStringParameters']['function']=="download-csv":
            # download csv file from s3 as link for a particular month and 
            # year inputs by returning a download link to the file 
            return download_csv(event)
        elif event['queryStringParameters']['function']=="upload-pdf":
            # added in the billing api code 
            # api to generate bills pdf in s3 when billing api is hit 
            return upload_pdf(event)
        elif event['queryStringParameters']['function']=='download-pdf':
            # download pdf file from s3 as link for a particular month and 
            # yearinputs by returning a download link to the file 
            return download_pdf(event) 
        elif event['queryStringParameters']['function']=="get-light-area":
            # get area name for a particular project where lights needs to be controlled
            return get_light_area(event)
        elif event['queryStringParameters']['function']=='get-light-status':
            # get area light current status
            return get_light_status(event)
        elif event['queryStringParameters']['function']=='set-light-status':
            # set area light current status
            return set_light_status(event)
        elif event['queryStringParameters']['function']=='tickets-count':
            # get count of tickets in each category
            return get_tickets_count(event)
        elif event['queryStringParameters']['function']=='get-inprocess-tickets':
            # get ticket details  in category InProcess
            return get_inprocess_tickets(event)
        elif event['queryStringParameters']['function']=='get-hold-tickets':
            # get get ticket details  in category Hold
            return get_hold_tickets(event)    
        elif event['queryStringParameters']['function']=='scan-device-alerts':
            # scan device alerts table for devices with alerts 
            return scan_device_alerts(event)    
        elif event['queryStringParameters']['function']=='service-alerts-today':
            # service alerts tab function
            return service_alerts_today(event)
        elif event['queryStringParameters']['function']=='service-alerts-last-7-days':
            # service alerts tab function
            return service_alerts_last_7_days(event)  
        elif event['queryStringParameters']['function']=='alerts-by-service':
            # service alerts by service type
            return alerts_by_service(event) 
        elif event['queryStringParameters']['function']=='bill-api-with-minimum-v2':
            # Modified version of api bill-api-with-minimum where everything is listed inside a array instead of dictionary
            # without using the start and end dates parameters and calculates everything for the current month. 
            return bill_api_with_minimum_v2(event)  
        elif event["queryStringParameters"]["function"]=="device-list-v2":
            # webapp solenoid valve tab function 
            return populate_device_list_v2(event)    
        elif event['queryStringParameters']['function']=='bill-api-with-minimum-v3':
            # Modified version of api bill-api-with-minimum where everything is listed inside a array instead of dictionary
            # With start date and end date 
            return bill_api_with_minimum_v3(event)
            

    # Endpoint for post requests   
    elif event['resource']=="/resume" and event['httpMethod']=='POST':
        if event["queryStringParameters"]["service"]=="water-meter":
            return water_meter_update_db(event)
        elif event["queryStringParameters"]["service"]=="sprinklers":
            return sprinkler_update_db(event)        
        elif event["queryStringParameters"]["service"]=="put-item-user_valve":
            # insert new meter details 
            return insert_user_valve(event)
        elif event["queryStringParameters"]["service"]=="put-item-meter-card":
            # function to insert new items in meter card table 
            return insert_meter_card(event)
        elif event["queryStringParameters"]["service"]=="valve-control":
            # webapp solenoid valve tab function
            return user_valve_control(event)
        elif event['queryStringParameters']['service']=='control-all-valve':
            # webapp solenoid valve tab function 
            return control_all_water_meter_valve(event)        
        elif event["queryStringParameters"]["service"]=="update-meter":
            # makes changes in meter card rates and type
            return update_meter_card(event) 
        elif event["queryStringParameters"]["service"]=="put-sprinkler-data":
            # insert new sprinkler details in sprinkler data table
            return insert_sprinkler_data(event)
        elif event["queryStringParameters"]['service']=="update-sprinkler-schedule":
            # webapp sprinkler solenoid valve control tab function
            return sprinkler_modify_schedule(event) 
        elif event["queryStringParameters"]["service"]=="insert-rfid-info":
            # insert flat and vehicle mapping data for rfid service
            return insert_rfid_data(event)
        elif event["queryStringParameters"]["service"]=="insert-rfid-data":
            # insert in out rfid data for rfid service
            return insert_rfid_in_out_data(event) 
        elif event['queryStringParameters']['service']=='insert-aminity-list':
            # insert no of amenities and names for projects
            return insert_amenity_list(event)
        elif event['queryStringParameters']['service']=='insert-aminity-flat-mapping':
            # insert flat and access card maapping for projects
            return insert_amenity_flat_mapping(event)
        elif event['queryStringParameters']['service']=='insert-aminity-flat-mapping':
            # insert flat and access card maapping for projects
            return insert_amenity_flat_mapping(event)            
        elif event['queryStringParameters']['service']=='insert-aminity-data':
            # insert flat and access card maapping for projects
            return insert_amenity_data(event)      
        elif event['queryStringParameters']['service']=="generate-bills":
            # get dates when bill needs to be generated function
            return generate_bills(event) 
        elif event['queryStringParameters']['service']=="modify-billing-date":
            # modify bill generation date for a project
            return modify_billing_date(event)            
        elif event['queryStringParameters']['service']=="set-billing-date":
            # set billing date
            return set_billing_date(event)  
        elif event['queryStringParameters']['service']=="put-lighting-data":
            # insert new ligting data in lighting data table 
            return put_lighting_data(event) 
        elif event['queryStringParameters']['service']=='update-lighting-schedule':
            # update light scheduling data
            return update_lighting_schedule(event) 
        elif event['queryStringParameters']['service']=='raise-ticket':
            # raise ticket from users in mobile app
            return raise_ticket(event)
        elif event['queryStringParameters']['service']=='insert-device-alert-data':
            # insert device for tracking and storing ping status
            # contains devices from services - WM,SP,SL
            return insert_device_alert_data(event) 
        elif event['queryStringParameters']['service']=='update-ping-timestamp':
            # Update ping status for device-alerts
            return update_ping_timestamp(event)
 
    elif event['resource']=="/app" and event['httpMethod']=='GET':
        # Endpoint for get requests for webapp resource == resume 
        if event["queryStringParameters"]["function"]=="water-meter-dashboard":
            # todays , 7 days , month analysis based on limit settings 
            # Consumption dashboard app water meter 
            return water_meter_app_dashboard(event) 
        elif event['queryStringParameters']['function']=='water-meter-reports-app':
            # consumption reports day wise for mobile app users 
            return water_meter_reports_app(event)
        elif event['queryStringParameters']['function']=='water-meter-today-graph':
            # consumption reports day wise for mobile app users 
            return water_meter_today_graph(event)    
        elif event['queryStringParameters']['function']=='water-meter-week-graph':
            # consumption reports day wise for mobile app users 
            return water_meter_week_graph(event)
        elif event['queryStringParameters']['function']=='water-meter-month-graph':
            # consumption reports month wise for mobile app users 
            return water_meter_month_graph(event)
        elif event['queryStringParameters']['function']=='water-meter-last-year-consumption':
            # water meter new page code
            return water_meter_last_year_consumption(event)   
        elif event['queryStringParameters']['function']=='water-meter-consumption-split':
            # water meter app page code
            return water_meter_consumption_split(event)
        elif event['queryStringParameters']['function']=='water-meter-billing-unbilled':
            # water meter app billing unbilled page 
            return water_meter_billing_unbilled(event) 
        elif event['queryStringParameters']['function']=='water-meter-billing-three-months':
            # water meter app billing last 3 months page 
            return water_meter_billing_three_months(event)  
        elif event['queryStringParameters']['function']=='water-meter-billing-graph':
            # water meter app billing page graph in history 
            return water_meter_billing_graph(event)
        elif event['queryStringParameters']['function']=='water-meter-bill-by-month':
            # water meter app billing page by month in history
            return water_meter_bill_by_month(event)        
###################################### MAIN LAMBDA ENDS HERE ############################################           