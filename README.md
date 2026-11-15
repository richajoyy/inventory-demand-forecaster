# Inventory Demand Forecaster

A supply chain tool that analyzes historical sales data to forecast inventory demand, calculate safety stock, and flag items requiring reordering — helping operations teams prevent stockouts before they happen.

## The Problem

Supply chain teams managing dozens of SKUs need to know:
- Which items will run out before the next shipment arrives?
- How much safety stock should we hold given demand variability?
- What needs to be ordered **today** vs. what can wait?

Manual tracking misses critical reorder windows, leading to production stoppages and costly emergency orders.

## The Solution

This tool automates demand forecasting and reorder prioritization across all inventory items, surfacing critical alerts before stockouts occur.

**Key features:**
- Calculates 7-day average daily demand per SKU
- Computes safety stock using statistical demand variability (1.5σ × √lead time)
- Projects stockout dates for every item
- Prioritizes items into 4 urgency tiers: Critical / Reorder Soon / Monitor / OK

## How It Works

**Input:** Inventory CSV with current stock levels, reorder points, lead times, and 7-day sales history

**Analysis:**
1. Calculate average daily demand and standard deviation per item
2. Compute safety stock based on demand variability and supplier lead time
3. Project days of stock remaining and stockout date
4. Assign urgency status based on stock vs. safety stock vs. reorder point

**Output:** Prioritized reorder report sorted by urgency

## Sample Output

```
======================================================================
       INVENTORY DEMAND FORECAST & REORDER REPORT
       Generated: November 15, 2026
======================================================================

🚨  Forklift Batteries (Equipment)
   Stock: 3 units  |  Avg Daily Demand: 1.3 units/day  |  Days Remaining: 2.3 days
   Safety Stock: 5 units  |  Reorder Point: 5 units  |  Lead Time: 14 days
   Projected Stockout: 2026-11-17  |  STATUS: CRITICAL — ORDER NOW

🚨  Air Filter Units (Maintenance)
   Stock: 8 units  |  Avg Daily Demand: 3.4 units/day  |  Days Remaining: 2.4 days
   Safety Stock: 9 units  |  Reorder Point: 15 units  |  Lead Time: 6 days
   Projected Stockout: 2026-11-17  |  STATUS: CRITICAL — ORDER NOW

======================================================================
SUMMARY
======================================================================
  CRITICAL — ORDER NOW: 4 item(s)
  REORDER SOON: 2 item(s)
  MONITOR CLOSELY: 1 item(s)
  OK: 3 item(s)

  ➜ 6 item(s) require immediate action
======================================================================
```

## Business Impact

- **Prevent stockouts:** Early warning system flags critical items days before they run out
- **Reduce emergency orders:** Systematic reorder tracking eliminates reactive purchasing
- **Optimize safety stock:** Statistical calculation right-sizes buffer inventory, reducing carrying costs

## Technical Architecture

```
inventory-forecaster/
├── data/
│   └── inventory.csv          (SKU data: stock levels, sales history, lead times)
├── src/
│   └── forecaster.py          (Demand forecasting and reorder prioritization engine)
├── results/
│   └── reorder_report.csv     (Output: prioritized reorder report)
└── requirements.txt
```

## Installation & Usage

```bash
pip install -r requirements.txt
python src/forecaster.py
```

## Author

Richa JOY 
Supply Chain Management 
https://github.com/richajoyy



