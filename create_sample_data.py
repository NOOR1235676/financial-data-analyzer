#!/usr/bin/env python3
"""
Script to create sample financial data files for the Financial Data Parser project
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_bank_data():
    """Create sample bank statement data"""
    
    # Generate sample dates over the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        # Add some randomness to dates (not every day)
        if random.random() > 0.3:  # 70% chance of transaction on any given day
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Sample transaction descriptions
    descriptions = [
        "ATM Withdrawal - Main Street",
        "Direct Deposit - Salary",
        "Online Transfer - Savings",
        "Debit Card Purchase - Grocery Store",
        "ACH Payment - Utilities", 
        "Check Deposit",
        "Wire Transfer - Investment",
        "Monthly Fee - Service Charge",
        "Interest Payment",
        "Overdraft Fee",
        "Mobile Payment - Coffee Shop",
        "Online Purchase - E-commerce",
        "Rent Payment - Property Management",
        "Insurance Premium - Auto",
        "Tax Refund Deposit",
        "Credit Card Payment",
        "Dividend Payment",
        "Foreign Exchange Transaction",
        "Loan Payment - Personal",
        "Subscription Fee - Software"
    ]
    
    # Generate transactions
    transactions = []
    balance = 5000.00  # Starting balance
    
    for date in sorted(dates):
        num_transactions = random.randint(1, 4)  # 1-4 transactions per day
        
        for _ in range(num_transactions):
            description = random.choice(descriptions)
            
            # Generate amount based on transaction type
            if "Deposit" in description or "Salary" in description:
                amount = round(random.uniform(500, 3000), 2)
            elif "Fee" in description:
                amount = -round(random.uniform(5, 50), 2)
            elif "ATM" in description:
                amount = -round(random.uniform(20, 200), 2)
            elif "Purchase" in description or "Payment" in description:
                amount = -round(random.uniform(10, 500), 2)
            else:
                amount = round(random.uniform(-300, 300), 2)
            
            balance += amount
            
            transactions.append({
                'Date': date.strftime('%m/%d/%Y'),
                'Description': description,
                'Amount': f"${abs(amount):,.2f}" if amount >= 0 else f"(${abs(amount):,.2f})",
                'Balance': f"${balance:,.2f}",
                'Transaction_Type': 'Credit' if amount >= 0 else 'Debit',
                'Reference': f"REF{random.randint(100000, 999999)}"
            })
    
    return pd.DataFrame(transactions)

def create_sample_ledger_data():
    """Create sample customer ledger data"""
    
    # Generate sample customers
    customers = [
        "ABC Corporation", "XYZ Inc", "Smith & Associates", 
        "Johnson Company", "Tech Solutions Ltd", "Global Industries",
        "Local Services", "Premium Products", "Express Logistics",
        "Creative Agency", "Financial Advisors", "Retail Chain"
    ]
    
    # Generate ledger entries
    entries = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    for _ in range(500):  # Generate 500 ledger entries
        customer = random.choice(customers)
        
        # Random date within range
        random_days = random.randint(0, 180)
        entry_date = start_date + timedelta(days=random_days)
        
        # Entry types
        entry_types = ['Invoice', 'Payment', 'Credit Note', 'Adjustment', 'Interest']
        entry_type = random.choice(entry_types)
        
        # Generate amount based on entry type
        if entry_type == 'Invoice':
            amount = round(random.uniform(100, 5000), 2)
        elif entry_type == 'Payment':
            amount = -round(random.uniform(100, 5000), 2)
        elif entry_type == 'Credit Note':
            amount = -round(random.uniform(50, 1000), 2)
        else:
            amount = round(random.uniform(-500, 500), 2)
        
        entries.append({
            'Posting Date': entry_date.strftime('%Y-%m-%d'),
            'Customer Name': customer,
            'Document No': f"DOC{random.randint(10000, 99999)}",
            'Description': f"{entry_type} - {customer}",
            'Amount': amount,
            'Amount_Formatted': f"€{abs(amount):,.2f}" if amount >= 0 else f"(€{abs(amount):,.2f})",
            'Currency': 'EUR',
            'Due Date': (entry_date + timedelta(days=30)).strftime('%Y-%m-%d'),
            'Customer No': f"CUST{random.randint(1000, 9999)}",
            'Entry Type': entry_type
        })
    
    return pd.DataFrame(entries)

def create_additional_formats_data():
    """Create data with various formats to test parsing capabilities"""
    
    # Test different amount formats
    amount_formats = [
        "$1,234.56", "€1.234,56", "₹1,23,456.78", "(2,500.00)", 
        "1234.56-", "1.5K", "2.3M", "£500.75", "¥100,000"
    ]
    
    # Test different date formats  
    date_formats = [
        "12/31/2023", "31/12/2023", "2023-12-31", "Dec-23", 
        "Q4 2023", "March 2024", "44927", "2024/03/15"
    ]
    
    test_data = []
    for i in range(len(amount_formats)):
        test_data.append({
            'ID': i + 1,
            'Amount_Original': amount_formats[i],
            'Date_Original': date_formats[i % len(date_formats)],
            'Category': random.choice(['Revenue', 'Expense', 'Asset', 'Liability']),
            'Notes': f"Test entry {i + 1} with various formats"
        })
    
    return pd.DataFrame(test_data)

def main():
    """Create all sample data files"""
    
    print("🏦 Creating Financial Data Parser Sample Files...")
    
    # Create bank statement data
    print("📊 Generating bank statement data...")
    bank_data = create_sample_bank_data()
    
    # Create customer ledger data  
    print("📋 Generating customer ledger data...")
    ledger_data = create_sample_ledger_data()
    
    # Create format test data
    print("🔧 Generating format test data...")
    format_test_data = create_additional_formats_data()
    
    # Save to Excel files
    print("💾 Saving files...")
    
    # Bank statement file
    with pd.ExcelWriter('data/sample/KH_Bank.xlsx', engine='openpyxl') as writer:
        bank_data.to_excel(writer, sheet_name='Bank_Statement', index=False)
        
        # Add a summary sheet
        summary_data = pd.DataFrame([
            {'Metric': 'Total Transactions', 'Value': len(bank_data)},
            {'Metric': 'Date Range', 'Value': f"{bank_data['Date'].min()} to {bank_data['Date'].max()}"},
            {'Metric': 'Account Number', 'Value': 'ACC-123456789'},
            {'Metric': 'Account Name', 'Value': 'KH Business Account'},
            {'Metric': 'Currency', 'Value': 'USD'}
        ])
        summary_data.to_excel(writer, sheet_name='Account_Info', index=False)
    
    # Customer ledger file
    with pd.ExcelWriter('data/sample/Customer_Ledger_Entries_FULL.xlsx', engine='openpyxl') as writer:
        ledger_data.to_excel(writer, sheet_name='Customer_Entries', index=False)
        
        # Add customer summary
        customer_summary = ledger_data.groupby('Customer Name').agg({
            'Amount': ['count', 'sum', 'mean']
        }).round(2)
        customer_summary.to_excel(writer, sheet_name='Customer_Summary')
        
        # Add format test data
        format_test_data.to_excel(writer, sheet_name='Format_Tests', index=False)
    
    print("✅ Sample files created successfully:")
    print("   📁 data/sample/KH_Bank.xlsx")
    print("   📁 data/sample/Customer_Ledger_Entries_FULL.xlsx")
    print("\n📈 File Statistics:")
    print(f"   🏦 Bank transactions: {len(bank_data)}")
    print(f"   📋 Ledger entries: {len(ledger_data)}")
    print(f"   🔧 Format test cases: {len(format_test_data)}")
    
    print("\n🎯 Files are ready for testing the Financial Data Parser!")

if __name__ == "__main__":
    main()
