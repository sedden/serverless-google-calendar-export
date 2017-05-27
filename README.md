# Serverless Google Calendar Export

Export Google Calendars via Google Calendar CalDAV API.

[![Build Status](https://travis-ci.org/sedden/serverless-google-calendar-export.svg?branch=master)](https://travis-ci.org/sedden/serverless-google-calendar-export)
[![Dependency Status](https://gemnasium.com/badges/github.com/sedden/serverless-google-calendar-export.svg)](https://gemnasium.com/github.com/sedden/serverless-google-calendar-export)

## Quick start

### AWS setup

Please check the [official guide of the serverless framework](https://serverless.com/framework/docs/providers/aws/guide/credentials/#creating-aws-access-keys)
on how to setup and configure the AWS credentials for deployment.

Additionally, please create the `serverless.env.yml` file and add the OAuth 2.0 client secrets for the Google API.

    CLIENT_ID: 0123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com
    CLIENT_SECRET: abc123def456ghi789jkl012
    
### Verify Python installation

Ensure Python 3.6 is available:

    python --version
    Python 3.6.1

Install virtualenv, if necessary:

    pip install virtualenv

### Create and activate virtual environment for Python and Node.js®

Create virtual environment in `venv/`:

    virtualenv venv/

Active:

    source venv/bin/activate

Verify:

    which python
    /Users/.../.../serverless-google-calendar-export/venv/bin/python

#### Install Python libraries nodeenv and boto3

Install requirements defined in `requirements.txt`

    pip install -r requirements.txt

#### Install Node.Js

Install Node.Js version 6.10.2 via [nodeenv](https://github.com/ekalinin/nodeenv) into current virtualenv (-p)

    nodeenv -p -n 6.10.2
     * Install prebuilt node (6.10.2) ..... done.
     * Appending data to /Users/.../.../serverless-google-calendar-export/venv/bin/activate
     * Overwriting /Users/.../.../serverless-google-calendar-export/venv/bin/shim with new content

Verify Node.Js and NPM versions:

    node -v
    v6.10.2

    npm -v
    3.10.10


### Install Serverless Framework

To install the serverless framework (currently version 1.14.0)

    npm install serverless@1.14.0 -g

Change to `serverless-google-calendar-export/` directory and install plugins:

    cd serverless-google-calendar-export/
    npm install --save


## Deploy

Choose AWS profile:

    export AWS_PROFILE=serverless
    export AWS_REGION=eu-west-1

Deploy:

    sls deploy

    Serverless: Installing required Python packages...
    Serverless: Linking required Python packages...
    Serverless: Packaging service...
    Serverless: Unlinking required Python packages...
    Serverless: Uploading CloudFormation file to S3...
    Serverless: Uploading artifacts...
    Serverless: Uploading service .zip file to S3 (2.25 MB)...
    Serverless: Updating Stack...
    Serverless: Checking Stack update progress...
    ..............
    Serverless: Stack update finished...
    Service Information
    service: serverless-google-calendar-export
    stage: dev
    region: eu-west-1
    api keys:
      None
    endpoints:
      GET - https://---.execute-api.eu-west-1.amazonaws.com/dev/calendars/{id}
    functions:
      export_calendar: serverless-google-calendar-export-dev-export_calendar
    Serverless: Removing old service versions...


## Test

Install required python dependencies (populates `.requirements/` directory)

    sls requirements install

### Initial OAuth 2.0 key exchange 

Beside a client ID and the client secret, a refresh token and an access token are
required to use the Google Calendar API. This is how to obtain those tokens.

Please open this URL to grant read-only access to you Google Calendar

    https://accounts.google.com/o/oauth2/v2/auth?
     scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&
     access_type=offline&
     include_granted_scopes=true&
     redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&
     response_type=code&
     client_id=client_id

where the `client_id` needs to be replaced with the OAuth 2.0 client ID.
  
After approving the access request in the browser window, the authorization code will be passed via query parameter:

    http://localhost/callback?code=4/Q8r8X02b-pNtDfMwJbRn7cUshuq8

To complete the step, this authorization code needs to be exchanged for the refresh and access token
 
    http -f POST https://www.googleapis.com/oauth2/v4/token \
     code='4/Q8r8X02b-pNtDfMwJbRn7cUshuq8' \
     client_id='client_id' \
     client_secret='client_secret' \
     redirect_uri='http%3A%2F%2Flocalhost%2Fcallback' \
     grant_type='authorization_code'

where `client_id` and `client_secret` needs to be replaced with the OAuth 2.0 client credentials.
     
The response will contain the `access_token` and `refresh_token`:

    {
      "access_token":"2CoY.mo0oopheeteiwee0queeth2nee1jir3ooguchaedeitheiKo7uchoo2Shaezu6OoQuoojah2eX4iec3wahXahv1eeghoh4Op9geichae9kahy8wah9aew7veefa1",
      "expires_in":3987,
      "token_type":"Bearer",
      "refresh_token":"1/OokoluaNieS2Tayo8oh-Eec8lahn4zushi8joe8aeyu"
    }
    
Those tokens are required for the next step.

### Export calendar

A calendar can be exported by adding a new item like this

    {
      "id": "6a40ae66-d00f-43f0-9ca2-be4e1022003d",
      "cal_id": "example%40gmail.com",
      "access_token": "2CoY.mo0oopheeteiwee0queeth2nee1jir3ooguchaedeitheiKo7uchoo2Shaezu6OoQuoojah2eX4iec3wahXahv1eeghoh4Op9geichae9kahy8wah9aew7veefa1",
      "refresh_token": "1/OokoluaNieS2Tayo8oh-Eec8lahn4zushi8joe8aeyu",
      "token_expiry": "2017-05-14T23:00:53Z"
    }
    
into the DynamoDB calendars table, where

 * `id` is a random UUID,
 * `cal_id` is the ID of the Google Calendar to export,
 * `access_token` needs to be copied from previous step,
 * `refresh_token` needs to be copied from previous step,
 * `token_expiry` doesn't need to be changed (will be updated automatically).
 
Afterwards, the calendar can be retrieved via its UUID:
 
    http https://---.execute-api.eu-west-1.amazonaws.com/dev/calendars/6a40ae66-d00f-43f0-9ca2-be4e1022003d
 
    BEGIN:VCALENDAR
    PRODID:-//Google Inc//Google Calendar 70.9054//EN
    VERSION:2.0
    CALSCALE:GREGORIAN
    ...
    ...
    ...
    END:VCALENDAR
