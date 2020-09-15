Neo4j Desktop Key:

```
eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYWxsYmFjayI6IiIsImVtYWlsIjoiZXB1Z2hAb3BlbnNvdXJjZWNvbm5lY3Rpb25zLmNvbSIsImZvcm1hdCI6Impzb24iLCJvcmciOiJPcGVuU291cmNlIENvbm5lY3Rpb25zIiwicHViIjoibmVvNGouY29tIiwicmVnIjoiRXJpYyBQdWdoIiwic3ViIjoibmVvNGotZGVza3RvcCIsImV4cCI6MTYzMDY4NjY4NCwidmVyIjoiKiIsImlzcyI6Im5lbzRqLmNvbSIsIm5iZiI6MTU5OTE1MDY4NCwiaWF0IjoxNTk5MTUwNjg0LCJqdGkiOiIwd1l1TW1WVVIifQ.VYNWjJ2TZhyrTwYaaNA0k2Pi_dyBn3ZSe1gvtFz1gN1Q6QlL9og9F0X3B58QN6Pa6DKysJAuWjDcOLClwdwnPtCdD96MhlUxTJEWEED0mGv-XKcUUKY1vyDAYJ07EMTsQuH42aj35A3qiST65sYl1UbN6X1eWpZdoguMi_lBKiyW76BGE7OL48bTrLe8B_MpHZlmJuj0dXzfOqwyVv1HpLBh6LrOR5hzyFzuQ9wWfyHOIMsDz_00M78Op3B3AKhW2XjevmciafSBna4EBQuD7c_iN65dmTWmTz_jH0wbWtiSHCXTxJ_sPuk5EHRN7J9b4NAnbZYWlZfHv0sFhVkM-w
```




Okay, manually copied into the `/import` directory the subset.csv

Lets Create Business nodes
```
LOAD CSV WITH HEADERS FROM 'file:////subset.csv' AS row
WITH row WHERE row.BusinessName IS NOT NULL
MERGE (b:Business {Label: row.BusinessName, name: row.BusinessName, address: row.Address, city: row.City, state: row.State, zip:row.Zip, jobsRetained:row.JobsRetained});
```

Lets Create NAICS nodes with descriptive names:
```
LOAD CSV WITH HEADERS FROM 'file:////6-digit_2017_Codes.csv' AS row
WITH row WHERE row.`2017_NAICS_Code` IS NOT NULL
MERGE (n:NAICS {code: row.`2017_NAICS_Code`, name:row.`2017_NAICS_Title`});
```



clear data:
```
MATCH ()-[r:NAICS_TYPE_OF]-()
DELETE r;
MATCH ()-[r:LEND_TO]-()
DELETE r;
MATCH (b:Business) DELETE b;
MATCH (n:NAICS) DELETE n;
MATCH (l:Lender) DELETE l;

```

lets create a relationship between a business and a NAICS code:

```
LOAD CSV WITH HEADERS FROM 'file:////subset.csv' AS row
MATCH (b:Business {name: row.BusinessName})
MATCH (n:NAICS {code: row.NAICSCode})
MERGE (b)<-[:NAICS_TYPE_OF]->(n)
RETURN *;
```

Lets Create unique Lenders:
```
LOAD CSV WITH HEADERS FROM 'file:////subset.csv' AS row
WITH row WHERE row.Lender IS NOT NULL
MERGE (l:Lender {name: row.`Lender`});
```

Now lets make a relationship between a business and a lender

```
LOAD CSV WITH HEADERS FROM 'file:////subset.csv' AS row
MATCH (b:Business {name: row.BusinessName})
MATCH (l:Lender {name: row.Lender})
MERGE (b)<-[:LEND_TO]-(l)
RETURN *;
```

The UVA example...  Multiple organizations that are all ACTUALLY part of UVA.

AHTNA is found multiple times.  makes a connection via same Address

AHTNA "faked out" as the "SAME_PARENT_ORG"
