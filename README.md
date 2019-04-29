<p align="center">
  <img src="static/logo.png" width="250"/>
</p>

<h3 align="center">Real-Time Nationwide T-Mobile Inventory Tracker</h3>

## About

During the T-Mobile C2C Hackathon in March 2019, 2 friends and I created a customer service bot for T-Mobile that was able to look up real-time product inventory using a Private API used in the T-Mobile online store.  While creating the project, we noticed that if you called the API endpoint directly it would return actual inventory counts for items in the store, and by slightly modifying the POST request you could view results for multiple stores with a single API call.

TMobAll is an attempt to use this API endpoint to gather live inventory information for every T-Mobile store in the United States.

## API Endpoint

### Authentication

T-Mobile requires a Bearer Token to access the API.  To generate this token, there is a script that uses Selenium to check the inventory on a single item and it extracts the Bearer Token using a MITM Proxy.

You can call this Bearer Token generator script using the following code:

```python
import search

token = search.generate_token()
print("Your Bearer Token is: {}".format(token))
```

### API Endpoint

```python
import requests

api_endpoint = 'https://core.saas.api.t-mobile.com/supplychain/inventoryavailability/v1/inventory/search/inventory-details-view'

headers = {
    'Origin': 'https://www.t-mobile.com',
    'Authorization': 'Bearer {{ BEARER_TOKEN }}',
    'interactionid': 'getInventoryAvailabilityByProductAndLocation',
    'channelid': 'web',
    'timestamp': '2019-04-18T14:28:47.941Z',
    'Connection': 'keep-alive',
    'applicationid': 'frontend',
    'Pragma': 'no-cache',
    'activityid': 'Can_Be_Anything',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json;charset=UTF-8',
}

data = '{"products":["610214659972"],"locations":["7674","9010","4139"]}'

response = requests.post(api_endpoint, headers=headers, data=data)
print response.json()
```

### Expected Response

```javascript
{
    "status": "SUCCESS", 
    "errors": null, 
    "result": {
        "inventoryAvailabilityList": [
            {
                "displayMode": "Status", 
                "storeId": "7674", 
                "storeParticipation": "true", 
                "skuDetails": [
                    {
                        "skuId": "610214659972", 
                        "availabilityStatus": 101, 
                        "skuParticipation": "true", 
                        "quantity": {
                            "availableQuantity": 4
                        }
                    }
                ]
            }, 
            {
                "displayMode": "Status", 
                "storeId": "4139", 
                "storeParticipation": "true", 
                "skuDetails": [
                    {
                        "skuId": "610214659972", 
                        "availabilityStatus": 101, 
                        "skuParticipation": "true", 
                        "quantity": {
                            "availableQuantity": 1
                        }
                    }
                ]
            }, 
            {
                "displayMode": "Status", 
                "storeId": "9010", 
                "storeParticipation": "true", 
                "skuDetails": [
                    {
                        "skuId": "610214659972", 
                        "availabilityStatus": 101, 
                        "skuParticipation": "true", 
                        "quantity": {
                            "availableQuantity": 0
                        }
                    }
                ]
            }
        ]
    }, 
    "statusCode": "200"
}
```
