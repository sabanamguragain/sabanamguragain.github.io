

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import sys

# Set professional style
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.grid'] = True
matplotlib.rcParams['grid.alpha'] = 0.3
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.right'] = False

# File paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, 'data', 'Nepal_Macroeconomic_Data_2024_25.xlsx')
OUTPUT_FILE = os.path.join(PROJECT_DIR, 'output', 'Nepal_Economic_Dashboard_2024_25.png')

# Color scheme
COLORS = {
    'primary': '#2E5AAC',
    'secondary': '#1B6B6B',
    'accent': '#E8913A',
    'alert': '#C44536',
    'purple': '#7B68A6',
    'light_bg': '#F0F4F8',
    'dark_bg': '#1B3A5C',
    'highlight': '#F5B041'
}


def load_data(filepath):
    """Load all sheets from the Excel data file."""
    if not os.path.exists(filepath):
        print(f"Error: Data file not found at {filepath}")
        sys.exit(1)
    
    data = {}
    xl = pd.ExcelFile(filepath)
    for sheet in xl.sheet_names:
        data[sheet] = pd.read_excel(filepath, sheet_name=sheet)
    print(f"Loaded {len(data)} sheets: {list(data.keys())}")
    return data


def create_dashboard(data, output_path):
    """Create the comprehensive economic dashboard with proper spacing."""
    
    gdp = data['GDP_Indicators']
    price = data['Price_Indices']
    external = data['External_Sector']
    govt = data['Government_Finance']
    capital = data['Capital_Market']
    
    years = gdp['Fiscal Year'].tolist()
    
    # Increased height for better vertical spacing (was 30, now 38)
    fig = plt.figure(figsize=(22, 38))
    fig.patch.set_facecolor('#FAFBFC')
    
    # Title at the very top, well above all charts
    fig.text(0.5, 0.993, 'NEPAL ECONOMIC INDICATORS DASHBOARD',
             fontsize=26, fontweight='bold', color='#1B3A5C', ha='center', va='top')
    fig.text(0.5, 0.985, 'Based on Annual Data 2024/25 | Nepal Rastra Bank',
             fontsize=14, color='#5A6B7A', ha='center', va='top')
    
    # Top boundary of chart area
    TOP = 0.965  # Below title
    
    # Chart dimensions
    CHART_H = 0.072   # Height of each chart panel
    GAP = 0.022       # Vertical gap between rows
    LEFT_X = 0.06     # Left column x position
    RIGHT_X = 0.54    # Right column x position
    COL_W = 0.42      # Width of each chart
    
    # Row positions (top edge of each row)
    # Row 1: GDP Growth + Nominal GDP
    r1_y = TOP - CHART_H  # 0.893
    # Row 2: CPI + Trade
    r2_y = r1_y - GAP - CHART_H  # 0.799
    # Row 3: Remittances + Forex
    r3_y = r2_y - GAP - CHART_H  # 0.705
    # Row 4: Govt Finance + Debt
    r4_y = r3_y - GAP - CHART_H  # 0.611
    # Row 5: Interest Rates + NEPSE
    r5_y = r4_y - GAP - CHART_H  # 0.517
    
    # ===== PANEL 1: Real GDP Growth =====
    ax1 = fig.add_axes([LEFT_X, r1_y, COL_W, CHART_H])
    ax1.set_facecolor(COLORS['light_bg'])
    bars = ax1.bar(years, gdp['Real GDP Growth (%)'], color=COLORS['primary'], 
                   width=0.6, edgecolor='white', linewidth=1.5)
    for bar, val in zip(bars, gdp['Real GDP Growth (%)']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, 
                f'{val:.1f}%', ha='center', va='bottom', fontsize=10, 
                fontweight='bold', color=COLORS['primary'])
    ax1.set_title('Real GDP Growth Rate (%)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax1.set_ylim(0, 7)
    ax1.tick_params(axis='x', labelsize=9)
    ax1.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 2: Nominal GDP =====
    ax2 = fig.add_axes([RIGHT_X, r1_y, COL_W, CHART_H])
    ax2.set_facecolor(COLORS['light_bg'])
    ax2.plot(years, gdp['Nominal GDP (Rs. Billion)'], marker='o', color=COLORS['secondary'], 
            linewidth=2.5, markersize=8)
    ax2.fill_between(range(len(years)), gdp['Nominal GDP (Rs. Billion)'], alpha=0.15, color=COLORS['secondary'])
    for i, val in enumerate(gdp['Nominal GDP (Rs. Billion)']):
        ax2.text(i, val + 80, f'{val:,.0f}', ha='center', fontsize=9, 
                fontweight='bold', color=COLORS['secondary'])
    ax2.set_title('Nominal GDP at Current Prices (Rs. Billion)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax2.tick_params(axis='x', labelsize=9)
    ax2.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 3: CPI Inflation =====
    ax3 = fig.add_axes([LEFT_X, r2_y, COL_W, CHART_H])
    ax3.set_facecolor(COLORS['light_bg'])
    x = np.arange(len(years))
    w = 0.25
    ax3.bar(x - w, price['Overall CPI Inflation (%)'], w, label='Overall CPI', color=COLORS['primary'])
    ax3.bar(x, price['Food & Beverage CPI (%)'], w, label='Food CPI', color=COLORS['accent'])
    ax3.bar(x + w, price['Non-Food CPI (%)'], w, label='Non-food CPI', color=COLORS['alert'])
    ax3.set_xticks(x)
    ax3.set_xticklabels(years, fontsize=9)
    ax3.set_title('Consumer Price Inflation (Year-on-Year %)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax3.legend(fontsize=7.5, loc='upper right')
    ax3.grid(axis='y', alpha=0.3)
    ax3.axhline(y=0, color='black', linewidth=0.5)
    
    # ===== PANEL 4: Foreign Trade =====
    ax4 = fig.add_axes([RIGHT_X, r2_y, COL_W, CHART_H])
    ax4.set_facecolor(COLORS['light_bg'])
    w2 = 0.35
    ax4.bar(x - w2/2, external['Exports (Rs. Billion)'], w2, label='Exports', color=COLORS['secondary'])
    ax4.bar(x + w2/2, external['Imports (Rs. Billion)'], w2, label='Imports', color=COLORS['alert'])
    ax4.set_xticks(x)
    ax4.set_xticklabels(years, fontsize=9)
    ax4.set_title('Foreign Trade (Rs. Billion)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax4.legend(fontsize=7.5)
    ax4.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 5: Remittances =====
    ax5 = fig.add_axes([LEFT_X, r3_y, COL_W, CHART_H])
    ax5.set_facecolor(COLORS['light_bg'])
    ax5.bar(years, external['Workers Remittances (Rs. Billion)'], color=COLORS['purple'], 
            width=0.6, edgecolor='white', linewidth=1.5)
    for i, val in enumerate(external['Workers Remittances (Rs. Billion)']):
        ax5.text(i, val + 25, f'{val:,.0f}', ha='center', fontsize=9, 
                fontweight='bold', color=COLORS['purple'])
    ax5.set_title("Workers' Remittances (Rs. Billion)", fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax5.tick_params(axis='x', labelsize=9)
    ax5.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 6: Forex Reserves =====
    ax6 = fig.add_axes([RIGHT_X, r3_y, COL_W, CHART_H])
    ax6.set_facecolor(COLORS['light_bg'])
    ax6.plot(years, external['Forex Reserves (USD Million)'], marker='s', 
            color=COLORS['primary'], linewidth=2.5, markersize=8)
    ax6.fill_between(range(len(years)), external['Forex Reserves (USD Million)'], 
                    alpha=0.15, color=COLORS['primary'])
    for i, val in enumerate(external['Forex Reserves (USD Million)']):
        ax6.text(i, val + 250, f'${val:,.0f}M', ha='center', fontsize=9, 
                fontweight='bold', color=COLORS['primary'])
    ax6.set_title('Gross Foreign Exchange Reserves (USD Million)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax6.tick_params(axis='x', labelsize=9)
    ax6.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 7: Revenue & Expenditure =====
    ax7 = fig.add_axes([LEFT_X, r4_y, COL_W, CHART_H])
    ax7.set_facecolor(COLORS['light_bg'])
    ax7.bar(x - w2/2, govt['Revenue Growth (%)'], w2, label='Revenue Growth', color=COLORS['secondary'])
    ax7.bar(x + w2/2, govt['Expenditure Growth (%)'], w2, label='Expenditure Growth', color=COLORS['accent'])
    ax7.set_xticks(x)
    ax7.set_xticklabels(years, fontsize=9)
    ax7.set_title('Government Revenue & Expenditure Growth (%)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax7.legend(fontsize=7.5)
    ax7.grid(axis='y', alpha=0.3)
    ax7.axhline(y=0, color='black', linewidth=0.5)
    
    # ===== PANEL 8: Government Debt =====
    ax8 = fig.add_axes([RIGHT_X, r4_y, COL_W, CHART_H])
    ax8.set_facecolor(COLORS['light_bg'])
    ax8.plot(years, govt['Domestic Debt (Rs. Billion)'], marker='o', color=COLORS['primary'], 
            linewidth=2, label='Domestic Debt')
    ax8.plot(years, govt['External Debt (Rs. Billion)'], marker='s', color=COLORS['alert'], 
            linewidth=2, label='External Debt')
    ax8.set_xticks(range(len(years)))
    ax8.set_xticklabels(years, fontsize=9)
    ax8.set_title('Government Debt (Rs. Billion)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax8.legend(fontsize=7.5)
    ax8.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 9: Interest Rates =====
    ax9 = fig.add_axes([LEFT_X, r5_y, COL_W, CHART_H])
    ax9.set_facecolor(COLORS['light_bg'])
    ax9.plot(years, govt['91-Day T-Bill Rate (%)'], marker='o', color=COLORS['secondary'], 
            linewidth=2, label='91-day T-Bills')
    ax9.plot(years, govt['364-Day T-Bill Rate (%)'], marker='s', color=COLORS['accent'], 
            linewidth=2, label='364-day T-Bills')
    ax9.plot(years, govt['Weighted Avg Lending Rate (%)'], marker='^', color=COLORS['alert'], 
            linewidth=2, label='Lending Rate')
    ax9.set_title('Key Interest Rates (%)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax9.legend(fontsize=7.5)
    ax9.tick_params(axis='x', labelsize=9)
    ax9.grid(axis='y', alpha=0.3)
    
    # ===== PANEL 10: NEPSE Index =====
    ax10 = fig.add_axes([RIGHT_X, r5_y, COL_W, CHART_H])
    ax10.set_facecolor(COLORS['light_bg'])
    ax10.bar(years, capital['NEPSE Index (Closing)'], color=COLORS['purple'], 
             width=0.6, edgecolor='white', linewidth=1.5)
    for i, val in enumerate(capital['NEPSE Index (Closing)']):
        ax10.text(i, val + 40, f'{val:.0f}', ha='center', fontsize=9, 
                 fontweight='bold', color=COLORS['purple'])
    ax10.set_title('NEPSE Index (Closing)', fontsize=12, fontweight='bold', color='#2C3E50', pad=8)
    ax10.tick_params(axis='x', labelsize=9)
    ax10.grid(axis='y', alpha=0.3)
    
    # ===== KEY HIGHLIGHTS PANEL (using fig.text with figure coordinates) =====
    hl_y = r5_y - GAP - 0.14  # Bottom of panel
    hl_h = 0.14               # Height of panel
    hl_top = hl_y + hl_h      # Top of panel
    
    # Draw background rectangle using add_axes
    ax11 = fig.add_axes([LEFT_X, hl_y, 0.90, hl_h])
    ax11.set_facecolor(COLORS['dark_bg'])
    ax11.set_xlim(0, 10)
    ax11.set_ylim(0, 10)
    for spine in ax11.spines.values():
        spine.set_visible(False)
    ax11.set_xticks([])
    ax11.set_yticks([])
    
    highlights = [
        ('GDP Growth', '4.61%', '2024/25'),
        ('CPI Inflation', '2.20%', 'Lowest in 5 yrs'),
        ('Forex Reserves', '$19.5B', 'Record High'),
        ('Remittances', 'Rs.1,723B', '+19.2% YoY'),
        ('Trade Deficit', 'Rs.1,527B', 'Improving'),
        ('NEPSE Index', '2,795', '+24.7% YoY')
    ]
    
    # Convert axes coords to figure coords for fig.text
    # Panel spans from LEFT_X to LEFT_X+0.90 horizontally
    # and from hl_y to hl_y+hl_h vertically
    panel_left = LEFT_X
    panel_width = 0.90
    panel_bottom = hl_y
    panel_height = hl_h
    
    # Title
    fig.text(panel_left + panel_width/2, panel_bottom + panel_height * 0.85,
             'KEY HIGHLIGHTS FY 2024/25', fontsize=14, fontweight='bold', 
             color=COLORS['highlight'], ha='center', va='center')
    
    for i, (label, value, note) in enumerate(highlights):
        x_pos = panel_left + panel_width * (0.083 + i * 0.153)
        # Value - large and bold
        fig.text(x_pos, panel_bottom + panel_height * 0.52, value,
                fontsize=17, fontweight='bold', color='white', ha='center', va='center')
        # Label - medium
        fig.text(x_pos, panel_bottom + panel_height * 0.28, label,
                fontsize=10, color='#A8C8E8', ha='center', va='center')
        # Note - small
        fig.text(x_pos, panel_bottom + panel_height * 0.10, note,
                fontsize=8.5, color='#7BA3C9', ha='center', va='center')
    
    # ===== GDP COMPOSITION PANEL =====
    bottom_y = hl_y - GAP - 0.14  # Below highlights
    ax12 = fig.add_axes([LEFT_X, bottom_y, 0.43, 0.15])
    ax12.set_facecolor(COLORS['light_bg'])
    sectors = ['Agriculture', 'Manufacturing', 'Construction', 'Wholesale/Retail', 
               'Transport', 'Education', 'Public Admin', 'Others']
    gdp_share = [25.2, 4.4, 4.6, 12.8, 6.3, 6.9, 7.7, 32.1]
    colors_pie = ['#2E5AAC', '#1B6B6B', '#E8913A', '#C44536', '#7B68A6', '#4A90D9', '#3DAA9F', '#95A5A6']
    wedges, texts, autotexts = ax12.pie(gdp_share, labels=sectors, autopct='%1.1f%%', 
                                        colors=colors_pie, startangle=90, textprops={'fontsize': 8})
    for autotext in autotexts:
        autotext.set_fontsize(7)
        autotext.set_fontweight('bold')
    ax12.set_title('GDP by Sector (2024/25) - Current Prices', fontsize=12, fontweight='bold', 
                  color='#2C3E50', pad=12)
    
    # ===== PER CAPITA INDICATORS =====
    ax13 = fig.add_axes([RIGHT_X, bottom_y, 0.42, 0.15])
    ax13.set_facecolor(COLORS['light_bg'])
    indicators = ['Per Capita\nGDP (NRs.)', 'Per Capita\nGNI (NRs.)', 'Per Capita\nGNDI (NRs.)']
    values_2024 = [192031, 195183, 248033]
    values_2025 = [203538, 206424, 263959]
    x = np.arange(3)
    w = 0.3
    bars1 = ax13.bar(x - w/2, values_2024, w, label='2023/24', color=COLORS['primary'], alpha=0.8)
    bars2 = ax13.bar(x + w/2, values_2025, w, label='2024/25', color=COLORS['secondary'])
    for bar, val in zip(bars2, values_2025):
        ax13.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000, f'{val:,.0f}', 
                 ha='center', fontsize=9, fontweight='bold', color=COLORS['secondary'])
    ax13.set_xticks(x)
    ax13.set_xticklabels(indicators, fontsize=9)
    ax13.set_title('Per Capita Income Indicators (NRs.)', fontsize=12, fontweight='bold', color='#2C3E50', pad=10)
    ax13.legend(fontsize=9)
    ax13.grid(axis='y', alpha=0.3)
    
    # Footer - positioned at the bottom with proper spacing
    fig.text(0.5, 0.008, 'Data Source: Nepal Rastra Bank | Economic Research Department | Statistical Tables 2024/25',
             ha='center', fontsize=10, color='#7F8C8D', style='italic')
    fig.text(0.5, 0.003, 'Dashboard Prepared by Sabnam Guragain | December 2024',
             ha='center', fontsize=10, color='#7F8C8D', style='italic')
    
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#FAFBFC', edgecolor='none',
                pad_inches=0.3)
    plt.close()
    print(f"Dashboard saved successfully to: {output_path}")


def main():
    print("=" * 60)
    print("NEPAL ECONOMIC INDICATORS DASHBOARD GENERATOR")
    print("=" * 60)
    print(f"Data source: {DATA_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("-" * 60)
    
    data = load_data(DATA_FILE)
    create_dashboard(data, OUTPUT_FILE)
    
    print("=" * 60)
    print("Dashboard generation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
