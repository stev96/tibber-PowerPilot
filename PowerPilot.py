import requests
import json

# Set your Tibber API key and location ID
TIBBER_API_KEY = 'your_tibber_api_key_here'
TIBBER_LOCATION_ID = 'your_tibber_location_id_here'

# Set your Shelly Plug S IP address and credentials
SHELLY_IP_ADDRESS = 'your_shelly_ip_address_here'
SHELLY_USERNAME = 'your_shelly_username_here'
SHELLY_PASSWORD = 'your_shelly_password_here'

# Set your desired on/off prices in euro/kWh
ON_PRICE = 0.12
OFF_PRICE = 0.16

# Get the current Tibber price data
tibber_url = 'https://api.tibber.com/v1-beta/gql'
headers = {'Authorization': 'Bearer ' + TIBBER_API_KEY, 'Content-Type': 'application/json'}
query = '''
{
  viewer {
    homes {
      currentSubscription {
        priceInfo {
          current {
            total
            energy
          }
        }
      }
    }
  }
}
'''
response = requests.post(tibber_url, headers=headers, json={'query': query})
data = json.loads(response.text)
price_data = data['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']['current']
current_price = price_data['total'] / price_data['energy']  # convert to euro/kWh

# Get the Shelly Plug S status and turn it on or off based on the current Tibber price
shelly_url = 'http://' + SHELLY_IP_ADDRESS + '/relay/0'
shelly_response = requests.get(shelly_url, auth=(SHELLY_USERNAME, SHELLY_PASSWORD))
shelly_data = json.loads(shelly_response.text)
shelly_status = shelly_data['ison']

if current_price < ON_PRICE and not shelly_status:
    # Turn on the Shelly Plug S
    requests.post(shelly_url + '?turn=on', auth=(SHELLY_USERNAME, SHELLY_PASSWORD))
elif current_price > OFF_PRICE and shelly_status:
    # Turn off the Shelly Plug S
    requests.post(shelly_url + '?turn=off', auth=(SHELLY_USERNAME, SHELLY_PASSWORD))