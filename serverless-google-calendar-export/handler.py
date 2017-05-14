import os
import boto3
import requests

from datetime import datetime, timedelta

DT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

DYNAMODB = boto3.resource('dynamodb')

def export_calendar(event, context):
    '''
    Export calendar via HTTP. 
    
    :param event: 
    :param context: 
    :return: 
    '''

    # retrieve calendar item from DynamoDB
    calendar_id = event['pathParameters']['id']
    item = get_item(calendar_id)

    # check prerequisites
    access_token = item.get('access_token', '')
    token_expiry = item.get('token_expiry', '')
    refresh_token = item.get('refresh_token', '')
    if not access_token or not token_expiry or not refresh_token:
        response = {
            'statusCode': 400,
            'body': 'Bad request'
        }
        return response

    # refresh access token
    item = refresh_access_token(item)

    # fetch calendar
    try:
        cal_id = item.get('cal_id', '')
        r_headers = {'Authorization': 'Bearer ' + item.get('access_token', '')}
        r = requests.get('https://apidata.googleusercontent.com/caldav/v2/' + cal_id + '/events',  headers = r_headers)

        # raise error for bad request
        r.raise_for_status()

        # create response
        response = {
            'statusCode': 200,
            'body': r.text,
            'headers': {
                'Content-Type' : r.headers['Content-Type'],
                'ETag' : r.headers['ETag']
            }
        }
        return response

    except:
        response = {
            'statusCode': 400
        }
        return response


def get_item(calendar_id):
    '''
    Retrieve calendar item from DynamoDB.
    
    :param calendar_id: calendar UUID.
    :return: calendar item.
    '''

    table = DYNAMODB.Table(os.environ['CALENDARS_TABLE'])
    result = table.get_item(Key={'id': calendar_id})
    item = result['Item']
    return item


def refresh_access_token(item):
    '''
    Refresh access token if required.
    
    :param item: calendar item.
    :return: updated calendar item with valid access token.
    '''

    expiry = datetime.strptime(item.get('token_expiry', ''), DT_FORMAT)
    if expiry < datetime.now():

        # refresh token
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': item.get('refresh_token', ''),
            'grant_type': 'refresh_token',
        }
        r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
        r_json = r.json()

        # calculate token expiry
        access_token_ = r_json['access_token']
        token_expiry = datetime.now() + timedelta(0, int(r_json['expires_in']))
        token_expiry_ = datetime.strftime(token_expiry, DT_FORMAT)

        # update access token and token expiry
        table = DYNAMODB.Table(os.environ['CALENDARS_TABLE'])
        item = table.update_item(Key={'id': item.get('id', '')},
                                 UpdateExpression='SET token_expiry = :e, access_token = :a',
                                 ExpressionAttributeValues={':e': token_expiry_, ':a': access_token_},
                                 ReturnValues="UPDATED_NEW")

    return item