import csv
import sys
import hashlib
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

def makeNode(id,row,ffld,pdct,tfld) :
    if row[ffld]!= "" :
        frm=row[ffld]
        to=row[tfld] if row[tfld]!= "" else "none"
        print(str(id)+","+frm.lower()+","+pdct+","+to.lower())
        return id+1
    return id
def makeDataNode(id,row,ffld,pdct,val) :
    if row[ffld]!= "" :
        frm=row[ffld]
        print(str(id)+","+frm.lower()+","+pdct+","+val)
        return id+1
    return id

if len(sys.argv)!=3:
	print("Need file path/name for NAICS codes and source data")
	sys.exit(1)
	
naicsPath = sys.argv[1]
srcPath = sys.argv[2]

codes=loadNaics(naicsPath)
print("id,sbj,pdct,obj")
with open(srcPath) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    l = 1
    for row in csv_reader:
        l=makeNode(l,row,"BusinessName","lend","Lender")
        l=makeNode(l,row,"BusinessName","city","City")
        l=makeNode(l,row,"BusinessName","state","State")
        l=makeNode(l,row,"BusinessName","zip","Zip")
        l=makeNode(l,row,"BusinessName","address","Address")
        l=makeNode(l,row,"BusinessName","naics","NAICSCode")
        l=makeNode(l,row,"BusinessName","type","BusinessType")
        l=makeNode(l,row,"BusinessName","race_ethnicity","RaceEthnicity")
        l=makeNode(l,row,"BusinessName","gender","Gender")
        l=makeNode(l,row,"BusinessName","veteran","Veteran")
        l=makeNode(l,row,"BusinessName","nonprofit","NonProfit")
        l=makeNode(l,row,"BusinessName","jobs","JobsReported")
        l=makeDataNode(l,row,"BusinessName","date",datetime.strptime(row["DateApproved"], '%m/%d/%Y').strftime("%Y-%m-%dT%H:%M:%SZ"))
        l=makeNode(l,row,"BusinessName","cd","CD")

