import csv
import sys

def loadZips(zf) :
    with open(zf) as csv_file:
        zip_reader = csv.DictReader(csv_file, delimiter=',')
        l = 0
        zips={}
        for row in zip_reader:
            if l == 0:
                print(','.join(row.keys()))
                pass
            else:
                # print(', '.join(row.values()))
                zips[row['zip']]=','.join(row.values())
            l += 1
    return zips

if len(sys.argv)!=3:
	print("Need file path/name for csv zip codes and csv source data")
	sys.exit(1)

zipPath = sys.argv[1]
srcPath = sys.argv[2]
zips=loadZips(zipPath)
zs={}

with open(srcPath) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    l = 1
    for row in csv_reader:
        if row['Zip'] in zips and not row['Zip'] in zs : 
            zs[row['Zip']]=zips[row['Zip']]
        l += 1
    for row in zs.values() :
        print(row)
