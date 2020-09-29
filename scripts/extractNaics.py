import csv
import sys

def loadNaics(nf) :
    with open(nf) as csv_file:
        zip_reader = csv.DictReader(csv_file, delimiter=',')
        l = 0
        naics={}
        for row in zip_reader:
            if l == 0:
                print('NAICS_Code,NAICS_Title')
                pass
            else:
                # print(', '.join(row.values()))
                naics[row['NAICS_Code']]=row['NAICS_Code']+','+row['NAICS_Title'].strip()
            l += 1
    return naics

if len(sys.argv)!=3:
	print("Need file path/name for csv naics codes and csv source data")
	sys.exit(1)

naicsPath = sys.argv[1]
srcPath = sys.argv[2]
naics=loadNaics(naicsPath)
ns={}

with open(srcPath) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    l = 1
    for row in csv_reader:
        if row['NAICSCode'] in naics and not row['NAICSCode'] in ns : 
            ns[row['NAICSCode']]=naics[row['NAICSCode']]
        l += 1
    for row in ns.values() :
        print(row)
