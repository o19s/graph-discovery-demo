import csv
import json

def loadNaics() :
    with open('2017_NAICS_Index_File.csv') as csv_file:
        naics_reader = csv.DictReader(csv_file, delimiter=',')
        l = 0
        codes={}
        for row in naics_reader:
            if l == 0:
                # print(f'Column names are {", ".join(row)}')
                pass
            else:
                codes[row['NAICS17']]=row["INDEX ITEM DESCRIPTION"]
                # print(f'\t{l}. {json.dumps(bn)}')
            l += 1
    # print(codes)
    return codes


def BN(id, row) :
    bn={}
    bn['id']=str(id)
    bn['BusinessNodeName']=row["BusinessName"]
    bn['type']="BusinessNode"
    bn['address']=row["Address"]
    bn['city']=row["City"]
    bn['state']=row["State"]
    bn['zip']=row["Zip"]
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
    # print(nc)

def BT(row,btd) :
    id=hash(row['BusinessType'])
    if not 
    bt={}
    bt['id']=id
    bt['type']="BusinessTypeNode"
    bt['name']=row['BusinessType']
    

codes=loadNaics()
bes=[]
ncs=[]
ncd={}
bts=[]
btd={}
with open('small-sample.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    l = 1
    for row in csv_reader:
        bes.append(BN(l, row))
        ncs.append(NC(row, codes, ncd))
        bts.append(BT(row, btd))
        l += 1
    print(json.dumps(bes))
    print(json.dumps(ncs))
    print(json.dumps(bts))
    print(f'Processed {l} lines.')

