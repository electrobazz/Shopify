name: Test Shopify-Square Integration

on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 * * * *'  # Runs every hour

jobs:
  test-integration:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run integration script
        env:
          SHOPIFY_API_KEY: '2cb48227cfff6b5966e27a3662b37eda'
          SHOPIFY_PASSWORD: 'd5f4a7942cdd30566fd26a81a7acdf03'
          SHOPIFY_STORE_NAME: 'electrobaz-inventory'
          SQUARE_ACCESS_TOKEN: 'EAAAl3gqJik6oNaTHz2KG33MA7rXFIypjdQTGntZTkr-e_h_Nrr7WDJ_TjpWL7-w'
          SQUARE_LOCATION_ID: 'LN3XRDV0R0G4X'
        run: |
          python shopify_square_integration.py
