import requests
import json
import time
import os

# Shopify API credentials
SHOPIFY_API_KEY = '2cb48227cfff6b5966e27a3662b37eda'
SHOPIFY_PASSWORD = 'd5f4a7942cdd30566fd26a81a7acdf03'
SHOPIFY_STORE_NAME = 'electrobaz-inventory'

# Square API credentials
SQUARE_ACCESS_TOKEN = 'EAAAl3gqJik6oNaTHz2KG33MA7rXFIypjdQTGntZTkr-e_h_Nrr7WDJ_TjpWL7-w'
SQUARE_LOCATION_ID = 'LN3XRDV0R0G4X'

# Headers for Shopify API requests
shopify_headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_PASSWORD
}

# Headers for Square API requests
square_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SQUARE_ACCESS_TOKEN}"
}

# Function to fetch inventory from Shopify
def fetch_shopify_inventory():
    url = f"https://{SHOPIFY_STORE_NAME}.myshopify.com/admin/api/2021-01/inventory_levels.json"
    response = requests.get(url, headers=shopify_headers)
    inventory_data = response.json()
    return inventory_data

# Function to update inventory in Square
def update_square_inventory(shopify_inventory):
    for item in shopify_inventory['inventory_levels']:
        square_item_id = get_square_item_id(item['sku'])
        if square_item_id:
            url = f"https://connect.squareup.com/v2/inventory/adjustment"
            payload = {
                "idempotency_key": str(time.time()),
                "reference_id": item['inventory_item_id'],
                "from_state": "IN_STOCK",
                "to_state": "IN_STOCK",
                "location_id": SQUARE_LOCATION_ID,
                "catalog_object_id": square_item_id,
                "quantity": str(item['available'])
            }
            response = requests.post(url, headers=square_headers, data=json.dumps(payload))
            if response.status_code != 200:
                print(f"Error updating Square inventory for SKU {item['sku']}: {response.text}")

# Function to get Square item ID by SKU
def get_square_item_id(sku):
    url = f"https://connect.squareup.com/v2/catalog/list"
    response = requests.get(url, headers=square_headers)
    items = response.json().get('objects', [])
    for item in items:
        if item.get('item_data', {}).get('sku') == sku:
            return item['id']
    return None

# Main function to sync inventory
def sync_inventory():
    shopify_inventory = fetch_shopify_inventory()
    update_square_inventory(shopify_inventory)

# Run the sync process
if __name__ == "__main__":
    sync_inventory()
