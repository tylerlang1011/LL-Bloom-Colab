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
mac = 'E4:F8:3C:B6:E8:56'

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
    print(url)
    maxPage = r['maxPage']
    print(maxPage)
    output_file = 'tagMqttHisotry-' + args.siteId + '-start' + args.timeBefore + '-end' + args.timeAfter + '.json'
    clean_output_file = str(output_file).replace(':', '')
    curPage = 0
    print(clean_output_file)
    writer = []

    with open(clean_output_file, 'w') as f:
        while True:
            curPage = curPage + 1
            url = ceProdBaseUrl + '/mqtt/{}/{}/{}?page={}'.format(args.siteId, args.timeBefore, args.timeAfter,
                                                                  curPage)
            r = requests.get(url, auth=AUTH).json()
            if r is None:
                break
            print(curPage)
            results = r.get('results', [])

#            for event in results:
#                print(event)

            for i in results:
                cleanData = {}
                tag_results= []
                cleanMac = mac.lower().replace(':', '')
                if '/tag/' in i['topic']:
                    est = pytz.timezone('US/Eastern')
                    utc = pytz.utc
                    utc_datetime = utc.localize(datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%S.%fZ"))
                    est_datetime = utc_datetime.astimezone(est)
                    time = est_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    if i['payload'].get('location_x', False):
                        # Area	Time	Zone	Category	Group	Name
                        if i['payload']['asset_category']:
                            category = i['payload']['asset_category']
                        else:
                            category = 'None'

                        if i['payload']['asset_group']:
                            group = i['payload']['asset_group']
                        else:
                            group = 'None'

                        cleanData = {
                            'SKE': i['payload']['asset_name'],
                            'Category': category,
                            'Group': group,
                            'Time': time,
                            'X': i['payload']['location_x'],
                            'Y': i['payload']['location_y'],
                            'Z': i['payload']['location_z'],
                            'Zone': i['payload']['zone_name']
                        }

                        print(cleanData)
                        for value in cleanData.values():
                            writer.append(str(value) + ',')
                        writer.append('\n')
                        #print(cleanData)
                        tag_results.append(cleanData)



            json.dump(tag_results, f)

            if curPage == (maxPage + 1):
                break
    f.close()
    write_file = 'tagMqttHisotry-' + args.siteId + '-start' + args.timeBefore + '-end' + args.timeAfter + '.csv'
    write_file = str(write_file).replace(':', '')
    with open(write_file, 'w') as w:
        w.writelines('SKE,Category, Group, Time, X, Y, Z, Zone\n')
        for line in writer:
            w.writelines(line)


if __name__ == '__main__':
    main()
