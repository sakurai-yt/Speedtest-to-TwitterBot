#!/usr/bin/python
#coding: utf-8
import os
import sys
import csv
import datetime
import time
import twitter
import random
import json
sys.path.append('/usr/lib/python2.7/site-packages')
from requests_oauthlib import OAuth1Session

def test():

        #run speedtest-cli
        print 'Server Selected'
        srvNum = random.randint(2,11)
        a = os.popen("python /root/speedtest/speedtest-cli --list").read()
        line = a.split('\n')
        print a
        tarSrv = line[srvNum]
        serverID = tarSrv.split(')')[0]
        serverName = tarSrv.split(')')[1]

        print 'running test'

        spdcmd = "python /root/speedtest/speedtest-cli --server %s --simple" %serverID
        print spdcmd

        b = os.popen(spdcmd).read()
        print 'ran'
        #split the 3 line result (ping,down,up)
        lines = b.split('\n')
        print b
        ts = time.time()
        date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        tm = time.strftime('%H%M%S')
        #if speedtest could not connect set the speeds to 0
        if "Cannot" in b:
                p = 100
                d = 0
                u = 0
        #extract the values for ping down and up values
        else:
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
        print date,p, d, u
                #save the data to file for local network plotting
        out_file = open('/root/speedtest/data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((ts*1000,p,d,u))
        out_file.close()

        #connect to twitter
        consumer_key=""
        consumer_secret=""
        access_token=""
        access_token_secret=""

        payload = {"text":   "Speedtest by Ookla RESULT. Server:" + serverName + ") Download:" + str(int(eval(d))) + "Mbps. Upload:" + str(int(eval(u))) + "Mbps. Ping:" + str(int(eval(p))) +"ms. Date:" + date +" Source: AWS"}

# Make the request
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

# Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
        return

if __name__ == '__main__':
        test()
        print 'completed'