# Reflection 1 How does this ETL pipeline compare to doing the same task in Excel?
# In Excel I would add a Total column with a formula, filter for orders over $100,
# and copy those rows to a new sheet by hand, and I'd have to redo every step
# whenever the data changed. Python does all of it in one run, works the same on
# 12 rows or a file too big for Excel to open, and the script is a record of exactly
# what was done. Excel is still easier for quickly looking over data, making a fast
# chart, or sharing with someone who doesn't code.
#
# Reflection 2: What business process would benefit from an append-mode log file?
# At a valet stand, every time a car is dropped off or picked up, the system could
# append a line with the time, ticket number, and which attendant handled it.
# Append mode is the right tool because each new entry is added to the end without
# erasing the earlier ones, so if a customer says their car was damaged or a key went
# missing, the manager has the full history of who handled it and when.

import csv
import os
from datetime import datetime


# Exercise 1: Get the file 
print("=== Exercise 1: Get the file ===")
print("data/sales.csv found:", os.path.exists("data/sales.csv"))
with open("data/sales.csv", "r") as f:
    lines = f.readlines()  # every line of the file, as a list
print("Header row:", lines[0].strip())
print("Number of data rows:", len(lines) - 1)  # minus 1 for the header
print()


# Exercise 2: Read and print raw rows 
print(" Exercise 2: Read and print raw rows ")
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # notice the quotes: every value comes in as text (a string)
print()


#  Exercise 3: Skip the header 
print("Exercise 3: Skip the header")
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)  # grab the first row (the column names) and move past it
    print("Header:", header)
    for row in reader:  # the loop now starts at the first data row
        print(row)
print()


# Exercise 4: Compute totals 
print("Exercise 4: Compute totals")
total_revenue = 0
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header
    for row in reader:
        product, price_str, qty_str = row  # split the row into its 3 values
        price = float(price_str)  # text -> decimal number
        qty = int(qty_str)  # text -> whole number
        total = price * qty
        total_revenue += total  # add this order to the running total
        print(f"{product}: {qty} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")
print()


# Exercise 5: Filter and write 
print(" Exercise 5: Filter and write ")
high_value = []  # orders over $100 go in this list
original_count = 0  # counts every order in sales.csv

# Extract + Transform: read each order, work out its total, keep the big ones
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        original_count += 1
        product, price_str, qty_str = row
        price = float(price_str)
        qty = int(qty_str)
        total = price * qty
        if total > 100:
            high_value.append([product, f"{price:.2f}", qty, f"{total:.2f}"])

# Load: write the kept orders to a new CSV
# newline="" stops blank rows from showing up between lines on Windows
with open("data/cleaned.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Qty", "Total"])  # header row
    writer.writerows(high_value)  # all kept orders at once

print(f"Rows in original file: {original_count}")
print(f"Rows written to data/cleaned.csv: {len(high_value)}")
print()


# Exercise 6: csv.DictReader 
print("Exercise 6: csv.DictReader")
dict_total = 0
with open("data/sales.csv", "r") as f:
    reader = csv.DictReader(f)  # uses the header row as the keys, so no next() needed
    for row in reader:
        product = row["product"]
        price = float(row["price"])
        qty = int(row["quantity"])
        total = price * qty
        dict_total += total
        print(f"{product}: {qty} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${dict_total:,.2f}")
print("Same total as Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))
# Use csv.reader for quick jobs on small files whose column order never changes; you grab values by position, like row[1].
# Use csv.DictReader when you want readable code like row["price"] that keeps working even if the columns get rearranged.
print()


# Exercise 7: Sales summary by product 
print("Exercise 7: Sales summary by product")
summary = {}  # {product name: total revenue}
with open("data/sales.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        if product in summary:
            summary[product] += total  # seen it before: add to its running total
        else:
            summary[product] = total  # first time: start its total
for product in sorted(summary):  # sorted() puts the names in A-Z order
    print(f"{product}: ${summary[product]:,.2f}")
print()


# Exercise 8: Append mode log 
print("Exercise 8: Append mode log")
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # current date and time as text
# "a" (append) adds to the end of the file; "w" would erase it every run
with open("data/run_log.txt", "a") as f:
    f.write(f"{now} - Total revenue: ${total_revenue:,.2f}\n")  # \n ends the line

with open("data/run_log.txt", "r") as f:
    entries = f.readlines()
print(f"data/run_log.txt now has {len(entries)} entries:")
for entry in entries:
    print(entry.strip())
