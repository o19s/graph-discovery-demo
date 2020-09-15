import csv
import json
import hashlib
import sys
from datetime import datetime

def hash(s):
    return hashlib.md5(s.encode()).hexdigest()

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

def BN(id, row, ncid, btid, reid, stid, zpid) :
    bn={}
    bn['id']=str(id)
    bn['name']=row["BusinessName"].lower()
    bn['type']="BusinessNode"
    bn['address']=row["Address"].lower()
    bn['city']=row["City"].lower()
    bn['state']=row["State"].upper()
    bn['zip']=row["Zip"]
    bn['loan_range']=row["LoanRange"]
    bn['gender']=row["Gender"].lower()
    bn['veteran']=row["Veteran"].lower()
    bn['non_profit']=row["NonProfit"].lower()
    bn['jobs_reported']=row["JobsReported"]
    bn['date_approved']=datetime.strptime(row["DateApproved"], '%m/%d/%Y').strftime("%Y-%m-%dT%H:%M:%SZ")
    bn['lender']=row["Lender"].lower()
    bn['CD']=row["CD"].lower()

    bn['NAICSNodeId']=ncid
    bn['BusinessTypeNodeId']=btid
    bn['RaceEthnicityId']=reid
    bn['StateNodeId']=stid
    bn['ZipNodeId']=zpid
    return bn
def NIN(id,tp,dct) :
    return not tp+"~"+id in dct
def ADD(id,tp,dct) :
    dct[tp+"~"+id]=""
def NC(row, codes, ja, dct) :
    nc={}
    tp="NAICSNode"
    id=row['NAICSCode']
    if id=="" :
        id="xx"
    if NIN(id,tp,dct) :
        nc['type']=tp
        nc['id']=id
        if id in codes :
            nc['name']=codes[row['NAICSCode']]
        else :
            nc['name']="No NAICS Label"
        ADD(id,tp,dct)
        ja.append(nc)
    return id

def makeNode(ja,id,row,ffld,pdct,tfld) :
    if row[ffld]!= "" :
        frm=row[ffld]
        to=row[tfld] if row[tfld]!= "" else "none"
        zt={}
        zt['id']=id
        zt["sbj"]=frm.lower()
        zt['pdct']=pdct
        zt['obj']=to.lower()
        ja.append(zt)
        return id+1
    return id
def makeDataNode(ja,id,row,ffld,pdct,val) :
    if row[ffld]!= "" :
        frm=row[ffld]
        zt={}
        zt['id']=id
        zt["sbj"]=frm.lower()
        zt['pdct']=pdct
        zt['obj']=val
        ja.append(zt)
        return id+1
    return id

if len(sys.argv)!=3:
	print("Need file path/name for NAICS codes and source data")
	sys.exit(1)
	
naicsPath = sys.argv[1]
srcPath = sys.argv[2]

codes=loadNaics(naicsPath)
jo=[]
with open(srcPath) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    l = 1
    for row in csv_reader:
        l=makeNode(jo,l,row,"BusinessName","lend","Lender")
        l=makeNode(jo,l,row,"BusinessName","city","City")
        l=makeNode(jo,l,row,"BusinessName","state","State")
        l=makeNode(jo,l,row,"BusinessName","zip","Zip")
        l=makeNode(jo,l,row,"BusinessName","address","Address")
        l=makeNode(jo,l,row,"BusinessName","naics","NAICSCode")
        l=makeNode(jo,l,row,"BusinessName","type","BusinessType")
        l=makeNode(jo,l,row,"BusinessName","race_ethnicity","RaceEthnicity")
        l=makeNode(jo,l,row,"BusinessName","gender","Gender")
        l=makeNode(jo,l,row,"BusinessName","veteran","Veteran")
        l=makeNode(jo,l,row,"BusinessName","nonprofit","NonProfit")
        l=makeNode(jo,l,row,"BusinessName","jobs","JobsReported")
        l=makeDataNode(jo,l,row,"BusinessName","date",datetime.strptime(row["DateApproved"], '%m/%d/%Y').strftime("%Y-%m-%dT%H:%M:%SZ"))
        l=makeNode(jo,l,row,"BusinessName","cd","CD")
    print(json.dumps(jo))

