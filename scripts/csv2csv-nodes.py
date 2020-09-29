import csv
import json
import sys
import hashlib

def loadNaics(naicsPath) :
    with open(naicsPath) as csv_file:
        naics_reader = csv.DictReader(csv_file, delimiter=',')
        l = 0
        codes={}
        for row in naics_reader:
            if l == 0:
                pass
            else:
                codes[row['NAICS17']]=row["INDEX ITEM DESCRIPTION"].lower()
            l += 1
    return codes

def hash(s):
    return hashlib.md5(s.encode()).hexdigest()



def BN(id, row) :
    bn={}
    bn['id']=str(id)
    bn['BusinessNodeName']=row["BusinessName"]
    bn['type']="BusinessNode"
    bn['address']=row["Address"]
    bn['city']=row["City"]
    bn['state']=row["State"]
    bn['zip']=row["Zip"]
    bn['NAICSNodeId']=row["NAICSCode"]
    bn['LoanRange']=row["LoanRange"]
    bn['RaceEthnicity']=row["RaceEthnicity"]
    bn['Gender']=row["Gender"]
    bn['Veteran']=row["Veteran"]
    bn['NonProfit']=row["NonProfit"]
    bn['JobsReported']=row["JobsReported"]
    bn['DateApproved']=row["DateApproved"]
    bn['Lender']=row["Lender"]
    bn['CD']=row["CD"]
    # print(bn)
    return bn

def NC(row, codes, ncd) :
    nc={}
    nid=row['NAICSCode']
    if not nid in ncd :
        nc['type']="NAICSNode"
        nc['id']=nid
        if nid in codes :
            nc['name']=codes[row['NAICSCode']]
        else :
            nc['name']="No NAICS Label"
        ncd[nid]=""
        return nc
    
if len(sys.argv)!=3:
	print("Need file path/name for NAICS codes and source data")
	sys.exit(1)
	
naicsPath = sys.argv[1]
srcPath = sys.argv[2]

codes=loadNaics(naicsPath)
bes=[]
ncs=[]
ncd={}
bts=[]
btd={}
with open(srcPath) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    l = 1
    for row in csv_reader:
        bes.append(BN(l, row))
        ncs.append(NC(row, codes, ncd))
        l += 1
#    print(json.dumps(bes))
    print(json.dumps(ncs))
#    print(json.dumps(bts))

