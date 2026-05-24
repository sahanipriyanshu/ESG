# Data Source Formats

This document outlines the expected ingestion formats for the prototype.

## 1. SAP ERP CSV Export (Scope 1)

Expected headers (German):
- `Buchungsdatum`: Activity Date (YYYY-MM-DD)
- `Werk`: Plant Code (e.g., SAP_BERLIN)
- `Treibstoffart`: Fuel Type (e.g., Diesel, Benzin)
- `Menge`: Quantity
- `Einheit`: Unit (e.g., L, Gallon, KG)

**Suspicious Flags:**
- Negative quantity
- Quantity > 10,000
- Future dates
- Unrecognized units

## 2. Utility Electricity CSV (Scope 2)

Expected headers:
- `Meter ID`: Identifier for the smart meter
- `Billing Start`: Start of billing period (YYYY-MM-DD)
- `Billing End`: End of billing period (YYYY-MM-DD)
- `kWh`: Electricity consumed
- `Tariff`: e.g., Standard, Green

**Suspicious Flags:**
- Negative kWh
- Billing Start date > Billing End date

## 3. Travel Partner API (Scope 3)

Expected JSON payload structure (POST to `/api/ingestion/travel/`):

```json
{
  "organization_id": "uuid",
  "payloads": [
    {
      "type": "flight",
      "date": "2023-04-10",
      "origin": "JFK",
      "destination": "LHR"
    },
    {
      "type": "hotel",
      "date": "2023-04-12",
      "nights": 5
    }
  ]
}
```

**Suspicious Flags:**
- Missing distances requiring estimations.
- Hotel stays > 30 nights.
- Negative distances/nights.
