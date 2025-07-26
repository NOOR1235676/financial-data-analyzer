#!/usr/bin/env python3
"""
Professional Report Generator
Creates styled PDF and Excel reports for financial analysis
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import io
import base64

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.report_style = ParagraphStyle(
            'ReportStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            fontName='Helvetica'
        )
        
    def generate_pdf_report(self, data, output_file="financial_report.pdf"):
        """Generate comprehensive PDF report"""
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontSize=20,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        story.append(Paragraph("Financial Data Analysis Report", title_style))
        story.append(Spacer(1, 12))
        
        # Report metadata
        metadata_style = ParagraphStyle(
            'MetadataStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['Heading1']))
        
        if data:
            bank_trans = data.get('bank_transactions', [])
            ledger_trans = data.get('ledger_transactions', [])
            matches = data.get('matches', [])
            
            total_bank = len(bank_trans)
            total_ledger = len(ledger_trans)
            total_matches = len(matches)
            
            bank_amount = sum(t.amount for t in bank_trans)
            ledger_amount = sum(t.amount for t in ledger_trans)
            matched_amount = sum(match[0].amount for match in matches)
            
            summary_text = f"""
            This report presents a comprehensive analysis of financial transaction data covering 
            {total_bank + total_ledger:,} total transactions with a combined value of 
            ${bank_amount + ledger_amount:,.2f}.<br/><br/>
            
            Key findings:<br/>
            • Total bank transactions: {total_bank:,}<br/>
            • Total ledger transactions: {total_ledger:,}<br/>
            • Successfully matched transactions: {total_matches:,}<br/>
            • Amount successfully reconciled: ${matched_amount:,.2f}<br/>
            • Match rate: {(total_matches / max(total_bank, 1)) * 100:.1f}%<br/>
            """
            
            story.append(Paragraph(summary_text, self.report_style))
        
        story.append(Spacer(1, 20))
        
        # Transaction Summary Table
        story.append(Paragraph("Transaction Summary", self.styles['Heading2']))
        
        if data:
            summary_data = [
                ['Metric', 'Bank Statements', 'Customer Ledger', 'Total'],
                ['Transaction Count', f"{total_bank:,}", f"{total_ledger:,}", f"{total_bank + total_ledger:,}"],
                ['Total Amount', f"${bank_amount:,.2f}", f"${ledger_amount:,.2f}", f"${bank_amount + ledger_amount:,.2f}"],
                ['Matched Transactions', f"{total_matches:,}", f"{total_matches:,}", f"{total_matches:,}"],
                ['Match Rate', f"{(total_matches / max(total_bank, 1)) * 100:.1f}%", f"{(total_matches / max(total_ledger, 1)) * 100:.1f}%", f"{(total_matches / max(total_bank + total_ledger, 1)) * 100:.1f}%"]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
        
        story.append(Spacer(1, 20))
        
        # Reconciliation Details
        if data and data.get('matches'):
            story.append(Paragraph("Top Reconciliation Matches", self.styles['Heading2']))
            
            match_data = [['Bank Date', 'Ledger Date', 'Amount', 'Match Score', 'Description']]
            
            for i, (bank_trans, ledger_trans, score) in enumerate(data['matches'][:10]):  # Top 10 matches
                match_data.append([
                    bank_trans.date.strftime('%Y-%m-%d'),
                    ledger_trans.date.strftime('%Y-%m-%d'),
                    f"${bank_trans.amount:,.2f}",
                    f"{score:.1f}",
                    bank_trans.description[:30] + "..." if len(bank_trans.description) > 30 else bank_trans.description
                ])
            
            match_table = Table(match_data)
            match_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            story.append(match_table)
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph("Financial Data Analysis Tool - Confidential Report", footer_style))
        
        # Build PDF
        doc.build(story)
        return output_file
    
    def generate_excel_report(self, data, output_file="financial_report.xlsx"):
        """Generate comprehensive Excel report with multiple sheets"""
        workbook = xlsxwriter.Workbook(output_file)
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#1f77b4',
            'border': 1,
            'align': 'center'
        })
        
        currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1
        })
        
        date_format = workbook.add_format({
            'num_format': 'yyyy-mm-dd',
            'border': 1
        })
        
        number_format = workbook.add_format({
            'num_format': '#,##0',
            'border': 1
        })
        
        percentage_format = workbook.add_format({
            'num_format': '0.0%',
            'border': 1
        })
        
        # Summary Sheet
        summary_sheet = workbook.add_worksheet('Executive Summary')
        summary_sheet.write('A1', 'Financial Data Analysis Report', workbook.add_format({'bold': True, 'font_size': 16}))
        summary_sheet.write('A2', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        if data:
            bank_trans = data.get('bank_transactions', [])
            ledger_trans = data.get('ledger_transactions', [])
            matches = data.get('matches', [])
            
            # Summary metrics
            row = 4
            summary_sheet.write(row, 0, 'Metric', header_format)
            summary_sheet.write(row, 1, 'Value', header_format)
            
            metrics = [
                ('Total Bank Transactions', len(bank_trans)),
                ('Total Ledger Transactions', len(ledger_trans)),
                ('Total Transactions', len(bank_trans) + len(ledger_trans)),
                ('Matched Transactions', len(matches)),
                ('Match Rate', len(matches) / max(len(bank_trans), 1)),
                ('Total Bank Amount', sum(t.amount for t in bank_trans)),
                ('Total Ledger Amount', sum(t.amount for t in ledger_trans)),
                ('Matched Amount', sum(match[0].amount for match in matches))
            ]
            
            for i, (metric, value) in enumerate(metrics, 1):
                summary_sheet.write(row + i, 0, metric)
                if 'Amount' in metric:
                    summary_sheet.write(row + i, 1, value, currency_format)
                elif 'Rate' in metric:
                    summary_sheet.write(row + i, 1, value, percentage_format)
                else:
                    summary_sheet.write(row + i, 1, value, number_format)
        
        # Bank Transactions Sheet
        if data and data.get('bank_transactions'):
            bank_sheet = workbook.add_worksheet('Bank Transactions')
            
            headers = ['Date', 'Description', 'Amount', 'Type', 'Category', 'Reference']
            for col, header in enumerate(headers):
                bank_sheet.write(0, col, header, header_format)
            
            for row, trans in enumerate(data['bank_transactions'], 1):
                bank_sheet.write(row, 0, trans.date, date_format)
                bank_sheet.write(row, 1, trans.description)
                bank_sheet.write(row, 2, trans.amount, currency_format)
                bank_sheet.write(row, 3, trans.debit_credit)
                bank_sheet.write(row, 4, trans.category)
                bank_sheet.write(row, 5, trans.reference)
        
        # Ledger Transactions Sheet
        if data and data.get('ledger_transactions'):
            ledger_sheet = workbook.add_worksheet('Ledger Transactions')
            
            headers = ['Date', 'Description', 'Amount', 'Type', 'Category', 'Counterparty']
            for col, header in enumerate(headers):
                ledger_sheet.write(0, col, header, header_format)
            
            for row, trans in enumerate(data['ledger_transactions'], 1):
                ledger_sheet.write(row, 0, trans.date, date_format)
                ledger_sheet.write(row, 1, trans.description)
                ledger_sheet.write(row, 2, trans.amount, currency_format)
                ledger_sheet.write(row, 3, trans.debit_credit)
                ledger_sheet.write(row, 4, trans.category)
                ledger_sheet.write(row, 5, trans.counterparty)
        
        # Matches Sheet
        if data and data.get('matches'):
            matches_sheet = workbook.add_worksheet('Reconciliation Matches')
            
            headers = ['Bank Date', 'Ledger Date', 'Bank Amount', 'Ledger Amount', 'Match Score', 
                      'Bank Description', 'Ledger Description', 'Amount Difference']
            for col, header in enumerate(headers):
                matches_sheet.write(0, col, header, header_format)
            
            for row, (bank_trans, ledger_trans, score) in enumerate(data['matches'], 1):
                matches_sheet.write(row, 0, bank_trans.date, date_format)
                matches_sheet.write(row, 1, ledger_trans.date, date_format)
                matches_sheet.write(row, 2, bank_trans.amount, currency_format)
                matches_sheet.write(row, 3, ledger_trans.amount, currency_format)
                matches_sheet.write(row, 4, score, number_format)
                matches_sheet.write(row, 5, bank_trans.description)
                matches_sheet.write(row, 6, ledger_trans.description)
                matches_sheet.write(row, 7, abs(bank_trans.amount - ledger_trans.amount), currency_format)
        
        # Auto-fit columns
        for sheet in workbook.worksheets():
            sheet.autofit()
        
        workbook.close()
        return output_file
    
    def create_chart_images(self, data, output_dir="report_charts"):
        """Create chart images for reports"""
        chart_dir = Path(output_dir)
        chart_dir.mkdir(exist_ok=True)
        
        if not data:
            return []
        
        chart_files = []
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Match analysis pie chart
        if data.get('matches') is not None:
            bank_trans = data.get('bank_transactions', [])
            matches = data.get('matches', [])
            
            matched = len(matches)
            unmatched = len(bank_trans) - matched
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie([matched, unmatched], labels=['Matched', 'Unmatched'], 
                   colors=['#28a745', '#dc3545'], autopct='%1.1f%%', startangle=90)
            ax.set_title('Transaction Matching Analysis', fontsize=14, fontweight='bold')
            
            chart_file = chart_dir / "match_analysis.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            chart_files.append(str(chart_file))
        
        # 2. Category distribution
        all_transactions = data.get('bank_transactions', []) + data.get('ledger_transactions', [])
        if all_transactions:
            categories = {}
            for t in all_transactions:
                cat = t.category if hasattr(t, 'category') and t.category else 'Other'
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(categories.keys(), categories.values(), color='skyblue')
                ax.set_title('Transaction Categories', fontsize=14, fontweight='bold')
                ax.set_xlabel('Category')
                ax.set_ylabel('Number of Transactions')
                plt.xticks(rotation=45, ha='right')
                
                chart_file = chart_dir / "category_distribution.png"
                plt.savefig(chart_file, dpi=300, bbox_inches='tight')
                plt.close()
                chart_files.append(str(chart_file))
        
        return chart_files
