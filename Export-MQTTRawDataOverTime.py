import requests
import keyring
import argparse
import json
from datetime import datetime
import pytz


ceProdBaseUrl = 'https://clientedge-conductor.link-labs.com/clientEdge/data/airfinderLocation'


###############################################################################
# set params
###############################################################################

orgId = 'fcfc00a1-5d18-4ed6-98b9-95d77293df29' #Bloom Energy
siteId = '9ad854fe-c449-403c-ba1c-cd1173a13656' #Proof of Concept
username = 'tyler.lang@link-labs.com'
password = keyring.get_password("conductor", "tyler.lang@link-labs.com")
timeBefore = '2024-04-22T15:13:00.000'
timeAfter  = '2024-04-22T11:00:00.000'

###############################################################################
# argparse
###############################################################################

parser = argparse.ArgumentParser(description='__doc__')
parser.add_argument('--siteId', '-s', default=siteId, help='username')
parser.add_argument('--username', '-u', default=username, help='username')
parser.add_argument('--password', '-p', default=password, help='password')
parser.add_argument('--timeBefore', '-tb', default=timeBefore, help='yyyy-mm-ddThh:mm:ss.sss')
parser.add_argument('--timeAfter', '-ta', default=timeAfter, help='yyyy-mm-ddThh:mm:ss.sss')
args = parser.parse_args()

###############################################################################
# main
###############################################################################


def main():
    AUTH = (args.username, args.password)
    pageNumber = 1
    url = ceProdBaseUrl + '/mqtt/{}/{}/{}?page={}'.format(args.siteId, args.timeBefore, args.timeAfter, pageNumber)
    r = requests.get(url, auth=AUTH).json()
    maxPage = r['maxPage']
    print(maxPage)
    output_file = 'mqttHisotry-' + args.siteId + '-start' + args.timeBefore + '-end' + args.timeAfter + '.json'
    clean_output_file = str(output_file).replace(':', '')
    curPage = 0
    with open(clean_output_file, 'w') as f:
        while True:
            curPage = curPage + 1
            url = ceProdBaseUrl + '/mqtt/{}/{}/{}?page={}'.format(args.siteId, args.timeBefore, args.timeAfter, curPage)
            r = requests.get(url, auth=AUTH).json()
            if r is None:
                break
            print(curPage)
            results = r.get('results', [])
            tag_results = []
            for event in results:
                tag_results.append(event)
            json.dump(tag_results, f)
            if curPage == (maxPage + 1):
                break
    f.close()


if __name__ == '__main__':
    main()
