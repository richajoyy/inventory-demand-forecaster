import pandas as pd
import numpy as np
import os

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/inventory.csv'))

# ── Calculate Daily Demand (7-day average) ────────────────────────────────────
sales_cols = ['day1_sales', 'day2_sales', 'day3_sales', 'day4_sales',
              'day5_sales', 'day6_sales', 'day7_sales']

df['avg_daily_demand'] = df[sales_cols].mean(axis=1).round(1)
df['demand_std']       = df[sales_cols].std(axis=1).round(1)

# ── Days of Stock Remaining ───────────────────────────────────────────────────
df['days_of_stock'] = (df['current_stock'] / df['avg_daily_demand']).round(1)

# ── Safety Stock (1.5x std dev * lead time) ───────────────────────────────────
df['safety_stock'] = (1.5 * df['demand_std'] * np.sqrt(df['lead_time_days'])).round(0).astype(int)

# ── Reorder Urgency ───────────────────────────────────────────────────────────
def urgency(row):
    if row['current_stock'] <= row['safety_stock']:
        return 'CRITICAL — ORDER NOW'
    elif row['current_stock'] <= row['reorder_point']:
        return 'REORDER SOON'
    elif row['days_of_stock'] <= row['lead_time_days'] + 3:
        return 'MONITOR CLOSELY'
    else:
        return 'OK'

df['status'] = df.apply(urgency, axis=1)

# ── Projected Stockout Date ───────────────────────────────────────────────────
from datetime import date, timedelta
today = date.today()
df['stockout_date'] = df['days_of_stock'].apply(
    lambda d: (today + timedelta(days=d)).strftime('%Y-%m-%d')
)

# ── Print Report ──────────────────────────────────────────────────────────────
print("=" * 70)
print("       INVENTORY DEMAND FORECAST & REORDER REPORT")
print(f"       Generated: {today.strftime('%B %d, %Y')}")
print("=" * 70)

status_order = ['CRITICAL — ORDER NOW', 'REORDER SOON', 'MONITOR CLOSELY', 'OK']
df['status_rank'] = df['status'].apply(lambda s: status_order.index(s))
df_sorted = df.sort_values('status_rank')

for _, row in df_sorted.iterrows():
    icon = '🚨' if 'CRITICAL' in row['status'] else \
           '⚠️ ' if 'REORDER' in row['status'] else \
           '👀' if 'MONITOR' in row['status'] else '✅'
    print(f"\n{icon}  {row['product_name']} ({row['category']})")
    print(f"   Stock: {int(row['current_stock'])} units  |  "
          f"Avg Daily Demand: {row['avg_daily_demand']} units/day  |  "
          f"Days Remaining: {row['days_of_stock']} days")
    print(f"   Safety Stock: {row['safety_stock']} units  |  "
          f"Reorder Point: {int(row['reorder_point'])} units  |  "
          f"Lead Time: {int(row['lead_time_days'])} days")
    print(f"   Projected Stockout: {row['stockout_date']}  |  "
          f"STATUS: {row['status']}")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
for s in status_order:
    count = len(df[df['status'] == s])
    print(f"  {s}: {count} item(s)")

total_critical = len(df[df['status'] == 'CRITICAL — ORDER NOW'])
total_reorder  = len(df[df['status'] == 'REORDER SOON'])
print(f"\n  ➜ {total_critical + total_reorder} item(s) require immediate action")
print("=" * 70)

# ── Save Results ──────────────────────────────────────────────────────────────
out_cols = ['product_id', 'product_name', 'category', 'current_stock',
            'avg_daily_demand', 'days_of_stock', 'safety_stock',
            'reorder_point', 'lead_time_days', 'stockout_date', 'status']

results_path = os.path.join(os.path.dirname(__file__), '../results/reorder_report.csv')
os.makedirs(os.path.dirname(results_path), exist_ok=True)
df_sorted[out_cols].to_csv(results_path, index=False)
print(f"\n  Report saved to: results/reorder_report.csv")
