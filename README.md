# Inventory Weather Dashboard

![Version](https://img.shields.io/badge/version-1.0-blue)
![Category](https://img.shields.io/badge/category-Inventory-green)
![License](https://img.shields.io/badge/license-LGPL-3-orange)
![Type](https://img.shields.io/badge/type-Application-purple)

| | |
|---|---|
| **Name** | Inventory Weather Dashboard |
| **Version** | 1.0 |
| **Category** | Inventory |
| **License** | LGPL-3 |
| **Application** | Yes |

## Description

## Functionality

### Models & Fields

#### Extends `sale.order`

**File:** `models/sale_order.py`

**Inherits:** `sale.order`

**Fields:**

| Field | Type |
|-------|------|
| `razorpay_payment_link_id` | `Char` |
| `payment_link` | `Char` |
| `payment_status` | `Selection` |

**Key Methods:**

- `action_generate_payment()` — Action/workflow method
- `action_send_whatsapp()` — Action/workflow method

#### `weather.dashboard` — Weather Dashboard

**File:** `models/stock_warehouse.py`

**Fields:**

| Field | Type |
|-------|------|
| `name` | `Selection` |
| `weather_info` | `Char` |
| `temperature` | `Float` |
| `description` | `Char` |

### Views & UI

**Form Views:** `stock_warehouse_views.xml`, `weather_dashboard_views.xml`

**Menus:** `stock_warehouse_views.xml`

**Website/Portal Templates:**

- `payment_page_template` (`payment_templates.xml`)

### Security

**Access Rights:** 1 model access rules defined

| Model |
|-------|
| `weather.dashboard` |

### Web Controllers & Routes

| Route | Controller |
|-------|------------|
| `/razorpay/pay/<int:order_id>` | `razorpay_controller.py` |
| `/razorpay/success` | `razorpay_controller.py` |

## Dependencies

| Module | Type |
|--------|------|
| `stock` | Odoo Core |
| `sale` | Odoo Core |
| `website` | Odoo Core |

## File Structure

```
weather/
├── LICENSE
├── README.md
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── razorpay_controller.py
├── models/
│   ├── __init__.py
│   ├── sale_order.py
│   └── stock_warehouse.py
├── security/
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── icon.png
└── views/
    ├── payment_templates.xml
    ├── sale_order_views.xml
    ├── stock_warehouse_views.xml
    └── weather_dashboard_views.xml
```

## Installation

This module is part of the **[odoo-manufacturing-inventory-suite](https://github.com/tejas7287/odoo-manufacturing-inventory-suite)** suite.

1. Place this module in your Odoo addons directory
2. Update the apps list: **Settings** → **Apps** → **Update Apps List**
3. Search for **"Inventory Weather Dashboard"** and click **Install**

## License

LGPL-3
