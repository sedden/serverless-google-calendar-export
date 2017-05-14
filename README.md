# Serverless Google Calendar Export

Export Google Calendars via Google Calendar CalDAV API.

[![Build Status](https://travis-ci.org/sedden/serverless-google-calendar-export.svg?branch=master)](https://travis-ci.org/sedden/serverless-youtube-podcasts)
[![Dependency Status](https://gemnasium.com/badges/github.com/sedden/serverless-google-calendar-export.svg)](https://gemnasium.com/github.com/sedden/serverless-youtube-podcasts)

## Quick start

### AWS setup

Please check the [official guide of the serverless framework](https://serverless.com/framework/docs/providers/aws/guide/credentials/#creating-aws-access-keys)
on how to setup and configure the AWS credentials for deployment.

Additionally, please create the `serverless.env.yml` file and add the OAuth 2.0 client secrets for the Google API.

    CLIENT_ID: 0123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com
    CLIENT_SECRET: abc123def456ghi789jkl012
    
### Verify Python installation

Ensure Python 2.7 is available:

    python --version
    Python 2.7

Install virtualenv, if necessary:

    pip install virtualenv

### Create and activate virtual environment for Python and Node.js®

Create virtual environment in `venv/`:

    virtualenv venv/

Active:

    source venv/bin/activate

Verify:

    which python
    /Users/.../.../serverless-youtube-podcasts/venv/bin/python

#### Install Python libraries nodeenv and boto3

Install requirements defined in `requirements.txt`

    pip install -r requirements.txt

#### Install Node.Js

Install Node.Js version 6.10.2 via [nodeenv](https://github.com/ekalinin/nodeenv) into current virtualenv (-p)

    nodeenv -p -n 6.10.2
     * Install prebuilt node (6.10.2) ..... done.
     * Appending data to /Users/.../.../serverless-youtube-podcasts/venv/bin/activate
     * Overwriting /Users/.../.../serverless-youtube-podcasts/venv/bin/shim with new content

Verify Node.Js and NPM versions:

    node -v
    v6.10.2

    npm -v
    3.10.10


### Install Serverless Framework

To install the serverless framework (currently version 1.12.1)

    npm install serverless@1.12.1 -g

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
    

    