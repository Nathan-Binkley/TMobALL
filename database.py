import boto3
import json
try:
	from keys import *
except:
	ACCESS_KEY = raw_input("ACCESS KEY: ")
	SECRET_KEY = raw_input("SECRET KEY: ")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)



dynamodb = session.resource("dynamodb")

table = dynamodb.Table("allInventory")

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)

def get_id_name():
    try:
        # Gets the newest ID name from the DB
        dynamodb = session.resource("dynamodb")
        table = dynamodb.Table("allInventory")
        #print(table.creation_date_time)
        response = table.scan()
        #print response["Items"]
        return max([x['id'] for x in response["Items"]]) + 1
    except:
        return 0

def updateTable(idVal):
    #for key, val in .iteritems():
    x = json.load(open(idVal + ".json"))
    for key, val in x.iteritems():
        g = {}
        g['key'] =  str(hash("{}_{}".format(idVal, key)))
        g['itemNum'] = str(key)
        for k, v in val.iteritems():
            g[k] = v
        table.put_item(
           Item=g
        )
        print("WRITE")


#response = table.scan()
#print response["Items"]
#print response['Item']
