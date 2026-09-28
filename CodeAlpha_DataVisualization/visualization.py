"""
DATA VISUALIZATION PROJECT
CodeAlpha Data Analytics Internship - Task 3

This script creates professional visualizations from a dataset,
demonstrating various chart types and design principles.
"""

# ============================================
# 1. IMPORT LIBRARIES
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set style for better-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

print("=" * 60)
print(" DATA VISUALIZATION PROJECT")
print("=" * 60)

# ============================================
# 2. CREATE DATASET
# ============================================

print("\n Creating dataset...")

# Create a realistic sales dataset
np.random.seed(42)

# Generate 200 records
n = 200

data = {
    'Order_ID': range(1001, 1001 + n),
    'Month': np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], n),
    'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Food',
                                           'Books', 'Home', 'Sports'], n),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], n),
    'Sales': np.random.randint(100, 5000, n),
    'Quantity': np.random.randint(1, 20, n),
    'Profit': np.random.randint(-500, 1500, n),
    'Customer_Age': np.random.randint(18, 70, n),
    'Rating': np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.1, 0.2, 0.4, 0.25])
}

df = pd.DataFrame(data)

# Add some calculated columns
df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
df['Revenue_per_Unit'] = (df['Sales'] / df['Quantity']).round(2)

# Save dataset to CSV
df.to_csv("sales_data.csv", index=False)
print(f" Dataset created with {len(df)} records")
print(f" Columns: {list(df.columns)}")

# Display first few rows
print("\n First 5 rows of data:")
print(df.head())

# ============================================
# 3. DATA OVERVIEW
# ============================================

print("\n" + "=" * 60)
print(" DATA OVERVIEW")
print("=" * 60)
print(df.describe())

# ============================================
# 4. CREATE VISUALIZATIONS
# ============================================

print("\n Creating visualizations...")

# --------------------------------------------
# CHART 1: BAR CHART - Sales by Product Category
# --------------------------------------------
print("   Creating Chart 1: Bar Chart...")

fig, ax = plt.subplots(figsize=(10, 6))
category_sales = df.groupby('Product_Category')['Sales'].sum().sort_values(ascending=True)

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
bars = ax.barh(category_sales.index, category_sales.values, color=colors)

# Add value labels on bars
for bar, value in zip(bars, category_sales.values):
    ax.text(value + 500, bar.get_y() + bar.get_height()/2,
            f'${value:,.0f}', va='center', fontsize=11, fontweight='bold')

ax.set_title('Total Sales by Product Category', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Total Sales ($)', fontsize=12)
ax.set_ylabel('Product Category', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart1_bar_sales_by_category.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 1 saved!")

# --------------------------------------------
# CHART 2: LINE CHART - Monthly Sales Trend
# --------------------------------------------
print("   Creating Chart 2: Line Chart...")

# Order months correctly
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

monthly_sales = df.groupby('Month')['Sales'].sum().reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_sales.index, monthly_sales.values,
        marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
ax.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.3, color='#2E86AB')

# Add value labels
for i, (month, value) in enumerate(zip(monthly_sales.index, monthly_sales.values)):
    ax.annotate(f'${value:,.0f}', (month, value),
                textcoords="offset points", xytext=(0, 10),
                ha='center', fontsize=9, fontweight='bold')

ax.set_title('Monthly Sales Trend', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Total Sales ($)', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('chart2_line_monthly_sales.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 2 saved!")

# --------------------------------------------
# CHART 3: PIE CHART - Sales Distribution by Region
# --------------------------------------------
print("   Creating Chart 3: Pie Chart...")

region_sales = df.groupby('Region')['Sales'].sum()

fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
explode = (0.05, 0.05, 0.05, 0.05)

wedges, texts, autotexts = ax.pie(
    region_sales.values,
    labels=region_sales.index,
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    shadow=True,
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)

ax.set_title('Sales Distribution by Region', fontsize=16, fontweight='bold', pad=20)

# Add legend
ax.legend(wedges, [f'{r}: ${v:,.0f}' for r, v in zip(region_sales.index, region_sales.values)],
          title="Regions", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.tight_layout()
plt.savefig('chart3_pie_region_sales.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 3 saved!")

# --------------------------------------------
# CHART 4: SCATTER PLOT - Sales vs Profit
# --------------------------------------------
print("   Creating Chart 4: Scatter Plot...")

fig, ax = plt.subplots(figsize=(12, 7))

scatter = ax.scatter(df['Sales'], df['Profit'],
                     c=df['Rating'], cmap='viridis',
                     s=df['Quantity']*10, alpha=0.6,
                     edgecolors='white', linewidth=0.5)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Customer Rating', fontsize=12)

ax.set_title('Sales vs Profit (Size = Quantity, Color = Rating)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Sales ($)', fontsize=12)
ax.set_ylabel('Profit ($)', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('chart4_scatter_sales_profit.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 4 saved!")

# --------------------------------------------
# CHART 5: HEATMAP - Correlation Matrix
# --------------------------------------------
print("   Creating Chart 5: Heatmap...")

# Select numerical columns
numerical_cols = ['Sales', 'Quantity', 'Profit', 'Customer_Age', 'Rating', 'Profit_Margin']
correlation = df[numerical_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=1, fmt='.2f',
            cbar_kws={'shrink': 0.8}, ax=ax,
            annot_kws={'fontsize': 11, 'fontweight': 'bold'})

ax.set_title('Correlation Heatmap of Numerical Variables',
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('chart5_heatmap_correlation.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 5 saved!")

# --------------------------------------------
# CHART 6: BOX PLOT - Sales by Category and Region
# --------------------------------------------
print("   Creating Chart 6: Box Plot...")

fig, ax = plt.subplots(figsize=(14, 7))

sns.boxplot(data=df, x='Product_Category', y='Sales', hue='Region',
            palette='Set2', ax=ax, linewidth=1.5)

ax.set_title('Sales Distribution by Product Category and Region',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Product Category', fontsize=12)
ax.set_ylabel('Sales ($)', fontsize=12)
ax.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart6_boxplot_category_region.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 6 saved!")

# --------------------------------------------
# CHART 7: DASHBOARD - Combined View
# --------------------------------------------
print("   Creating Chart 7: Dashboard...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Sales Analytics Dashboard', fontsize=20, fontweight='bold', y=1.02)

# Subplot 1: Bar Chart
category_sales = df.groupby('Product_Category')['Sales'].sum().sort_values()
axes[0, 0].barh(category_sales.index, category_sales.values, color='#4ECDC4')
axes[0, 0].set_title('Sales by Category', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Sales ($)')

# Subplot 2: Pie Chart
region_sales = df.groupby('Region')['Sales'].sum()
axes[0, 1].pie(region_sales.values, labels=region_sales.index,
               autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
axes[0, 1].set_title('Sales by Region', fontsize=14, fontweight='bold')

# Subplot 3: Line Chart
monthly_sales = df.groupby('Month')['Sales'].sum().reindex(month_order)
axes[1, 0].plot(monthly_sales.index, monthly_sales.values,
                marker='o', color='#2E86AB', linewidth=2)
axes[1, 0].set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Sales ($)')
axes[1, 0].tick_params(axis='x', rotation=45)

# Subplot 4: Histogram
axes[1, 1].hist(df['Sales'], bins=20, color='#96CEB4', edgecolor='white')
axes[1, 1].set_title('Sales Distribution', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Sales ($)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('chart7_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Chart 7 saved!")

# ============================================
# 5. INTERACTIVE CHART WITH PLOTLY
# ============================================

print("\n Creating interactive Plotly chart...")

# Interactive scatter plot
fig = px.scatter(df, x='Sales', y='Profit',
                 color='Product_Category',
                 size='Quantity',
                 hover_data=['Region', 'Rating', 'Customer_Age'],
                 title='Interactive Sales vs Profit Analysis',
                 labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)'})

fig.update_layout(
    title_font_size=20,
    title_font_family="Arial",
    template='plotly_white',
    height=600
)

fig.write_html("interactive_chart.html")
print("   Interactive chart saved as 'interactive_chart.html'")

# ============================================
# 6. KEY INSIGHTS
# ============================================

print("\n" + "=" * 60)
print(" KEY INSIGHTS FROM VISUALIZATIONS")
print("=" * 60)

# Top category
top_category = df.groupby('Product_Category')['Sales'].sum().idxmax()
top_category_sales = df.groupby('Product_Category')['Sales'].sum().max()
print(f"\n Top Selling Category: {top_category} (${top_category_sales:,.0f})")

# Top region
top_region = df.groupby('Region')['Sales'].sum().idxmax()
top_region_sales = df.groupby('Region')['Sales'].sum().max()
print(f" Top Region: {top_region} (${top_region_sales:,.0f})")

# Best month
best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()
print(f" Best Month: {best_month} (${best_month_sales:,.0f})")

# Average rating
avg_rating = df['Rating'].mean()
print(f" Average Rating: {avg_rating:.2f}/5.00")

# Profit analysis
total_profit = df['Profit'].sum()
total_sales = df['Sales'].sum()
profit_margin = (total_profit / total_sales * 100)
print(f" Total Profit: ${total_profit:,.0f}")
print(f" Overall Profit Margin: {profit_margin:.1f}%")

# ============================================
# 7. SUMMARY
# ============================================

print("\n" + "=" * 60)
print(" PROJECT COMPLETE!")
print("=" * 60)
print("\n Files generated:")
print("  1. sales_data.csv")
print("  2. chart1_bar_sales_by_category.png")
print("  3. chart2_line_monthly_sales.png")
print("  4. chart3_pie_region_sales.png")
print("  5. chart4_scatter_sales_profit.png")
print("  6. chart5_heatmap_correlation.png")
print("  7. chart6_boxplot_category_region.png")
print("  8. chart7_dashboard.png")
print("  9. interactive_chart.html")
print(" All visualizations created successfully!")