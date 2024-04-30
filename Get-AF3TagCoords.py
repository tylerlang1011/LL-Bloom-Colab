import requests
import keyring

baseUrl = 'https://networkasset-conductor.link-labs.com/networkAsset/'
AUTH = ('tyler.lang@link-labs.com', keyring.get_password("conductor", "tyler.lang@link-labs.com"))

testGroup1 = [
   'C7:01:3F:5C:8E:04',
    'C6:60:FE:7A:25:18',
    'EA:E0:C5:1B:86:3E',
    'CB:60:B3:A1:AD:2D',
    'F9:FB:E0:30:2B:58'
    ]

testGroup2 = [
    "CB:B3:E7:18:EF:E9",
    "D4:4E:96:89:4A:C4",
    "D6:08:ED:C2:92:B0",
    "FB:42:64:E7:60:1C",
    "DF:1D:16:B2:BF:23"
    ]

testGroup3 = [
    "D3:97:C2:DC:48:33",
    "D7:BD:54:1B:E0:AC",
    "DA:83:CF:CE:FE:A7",
    "E4:F8:3C:B6:E8:56",
    "F1:47:72:49:53:17"
    ]

testGroup4 = [
    "FF:FD:D2:0C:20:5B",
    "EB:8A:72:D3:2D:03",
    "E4:24:EC:CC:58:74",
    "DD:C8:EB:A2:EB:A7",
    "D2:E8:C7:24:DD:59",
    ]

testGroupList = [
    testGroup1,
    testGroup2,
    testGroup3,
    testGroup4
    ]
def main(tags):
    data = []
    for tag in tags:
        url = '{}airfinder/v4/tag/{}'.format(baseUrl, tag)
        r = requests.get(url, auth=AUTH).json()
        coords = [float(r['xCoordinate']) / 10, float(r['yCoordinate']) / 10, float(r['zCoordinate']) / 10]
        data.append(coords)
    sumx = 0
    sumy = 0
    sumz = 0
    for set in data:
        sumx = sumx + set[0]
        sumy = sumy + set[1]
        sumz = sumz + set[2]

    length = len(data)
    print(round(sumx/length, 2))
    print(round(sumy/length, 2))
    print(round(sumz/length, 2))
    print('-----------------')
    print(data)


if __name__ == "__main__":
    for group in testGroupList:
        print(str(group))
        main(group)
        print("\n")