Junior Data Analyst Portfolio Project: Subscription Churn & Revenue Analysis
Project Overview
Dataset: Telco Customer Churn Dataset — free on Kaggle, ~7,000 customer records from a fictional telecommunications company.
Why this dataset is more interesting:
Churn analysis is one of the most universally requested skills in business analytics. Subscription businesses — SaaS, telecoms, streaming, fintech — live and die by retention. This dataset gives you customer demographics, contract types, service usage, billing data, and a churn flag. It's messy enough to be realistic, clean enough to be manageable, and the business questions map directly to decisions real companies make every quarter.

Business Question: "Which customers are most likely to churn, what is it costing the business in lost revenue, and what are the early warning signs we could act on before they leave?"

End Deliverable: A Jupyter notebook structured as a mock internal analyst report — the kind you'd actually present to a retention team or a VP of Customer Success — with quantified revenue impact, behavioral patterns, and actionable recommendations.

Total estimated time: 9–10 nights × 30 minutes

Why This Is Better For Your Portfolio
Superstore StyleThis ProjectDescriptive: "here's what happened"Diagnostic + prescriptive: "here's why and what to do"Common dataset, seen constantlyLess saturated, more sophisticated framingRetail contextSaaS/subscription — where most analyst jobs areBasic aggregationsCohort logic, revenue impact modeling, risk segmentation"Sales went up in Q4""We are losing $X/month and here's the customer profile driving it"

The Business Context You're Stepping Into
Before you write a single line of code, internalize this framing. You are an analyst at a telecom company. The Head of Customer Success has flagged that churn has increased and wants to know:

How bad is it in revenue terms — not just customer count?
Are certain contract types or service bundles correlated with churn?
Is there a customer profile that churns early that we could flag sooner?
Where should retention spend be focused?

You are not building a machine learning model. You are doing the analytical groundwork that would inform that model, or more realistically, inform a business decision right now with what you have.

Project Roadmap
Night 1  → Setup, first look, business framing
Night 2  → Data cleaning + feature engineering
Night 3  → Churn rate baseline (the headline number)
Night 4  → Revenue impact quantification
Night 5  → Behavioral patterns — what do churners look like?
Night 6  → Tenure cohort analysis (when do customers leave?)
Night 7  → Risk segmentation — building a simple framework
Night 8  → SQL practice layer
Night 9  → Polished visuals + mock business report
Night 10 → README, GitHub, reflection

Night-by-Night Guide

🌙 Night 1 — Setup, First Look & Business Framing (~30 min)
Goal: Load the data, understand its structure, and write down your analytical questions before touching anything.
Folder structure:
Copytelco-churn-analysis/
├── data/
│   └── telco_churn.csv
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_report.ipynb
├── output/
│   └── charts/
└── README.md
First look checklist:
pythonCopyimport pandas as pd
import numpy as np

df = pd.read_csv('../data/telco_churn.csv')

# Structural overview
print(df.shape)
print(df.dtypes)
print(df.head(3))
print(df.columns.tolist())

# Missing values
print(df.isnull().sum())

# Target variable distribution — always do this first in churn work
print(df['Churn'].value_counts())
print(df['Churn'].value_counts(normalize=True).round(3))
Tonight's real task — answer these in markdown cells before touching the data further:
Copy1. What does one row represent? (one customer? one contract period?)
2. What is the churn rate at face value?
3. Which columns look like they could explain churn behavior?
4. What columns do you NOT have that you wish you did?
   (e.g., support ticket history, usage volume, NPS score)
   — this becomes a "limitations" section later

💡 Question 4 is not busywork. Articulating what data is missing and why it matters is something junior analysts almost never do, and it immediately signals business maturity to an interviewer.


🌙 Night 2 — Data Cleaning & Feature Engineering (~30 min)
Goal: Fix the data quality issues and create the columns that will power your analysis.
Known issues to handle in this dataset:
pythonCopy# TotalCharges is imported as an object — fix it
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Check what got coerced to NaN
print(df[df['TotalCharges'].isna()][['tenure', 'MonthlyCharges', 'TotalCharges']])
# You'll find ~11 customers with tenure=0 — they just signed up
# Decision: fill with 0 (reasonable) or drop — document your choice
df['TotalCharges'] = df['TotalCharges'].fillna(0)

# Convert churn to binary for math later
df['Churn_Flag'] = (df['Churn'] == 'Yes').astype(int)

# Convert SeniorCitizen to readable labels
df['SeniorCitizen_Label'] = df['SeniorCitizen'].map({0: 'Non-Senior', 1: 'Senior'})
Feature engineering — these are the columns that make your analysis richer:
pythonCopy# Tenure buckets — customers behave differently at different lifecycle stages
df['Tenure_Band'] = pd.cut(df['tenure'],
                            bins=[0, 3, 12, 24, 48, 72],
                            labels=['0-3 months', '4-12 months',
                                    '13-24 months', '25-48 months', '49-72 months'],
                            include_lowest=True)

# Revenue at risk — if this customer churns, what monthly revenue disappears?
# (You'll use this heavily on Night 4)
df['Revenue_At_Risk'] = df['MonthlyCharges'] * df['Churn_Flag']

# Service complexity score — how many add-on services does a customer have?
add_on_services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                   'TechSupport', 'StreamingTV', 'StreamingMovies']

df['Service_Count'] = df[add_on_services].apply(
    lambda row: (row == 'Yes').sum(), axis=1
)

# Average revenue per service (a rough value density measure)
df['Revenue_Per_Service'] = df['MonthlyCharges'] / (df['Service_Count'] + 1)
Save your clean dataset:
pythonCopydf.to_csv('../data/telco_clean.csv', index=False)
print(f"Clean dataset saved: {df.shape[0]} rows, {df.shape[1]} columns")

💡 Document every decision. When you filled those 11 NaN rows with 0, write a markdown cell explaining why. Analysts who can explain their assumptions are trusted. Analysts who can't are a liability.


🌙 Night 3 — Churn Rate Baseline (~30 min)
Goal: Establish the headline numbers — the churn rate cuts that a business cares about.
Think of this as building the first page of an internal report:
pythonCopydf = pd.read_csv('../data/telco_clean.csv')

# --- Overall churn rate ---
overall_churn = df['Churn_Flag'].mean()
print(f"Overall churn rate: {overall_churn:.1%}")

# --- Churn rate by contract type ---
# This is almost always the most important cut in subscription businesses
contract_churn = (df.groupby('Contract')
                    .agg(
                        Customers=('customerID', 'count'),
                        Churned=('Churn_Flag', 'sum'),
                        Churn_Rate=('Churn_Flag', 'mean'),
                        Avg_Monthly_Revenue=('MonthlyCharges', 'mean')
                    )
                    .round(3))
print(contract_churn)

# --- Churn by payment method ---
payment_churn = (df.groupby('PaymentMethod')['Churn_Flag']
                   .agg(['mean', 'count'])
                   .rename(columns={'mean': 'Churn_Rate', 'count': 'Customers'})
                   .sort_values('Churn_Rate', ascending=False))
print(payment_churn)

# --- Churn by internet service type ---
internet_churn = (df.groupby('InternetService')['Churn_Flag']
                    .agg(['mean', 'count'])
                    .rename(columns={'mean': 'Churn_Rate', 'count': 'Customers'})
                    .sort_values('Churn_Rate', ascending=False))
print(internet_churn)
Tonight's win — fill in this template in a markdown cell:
CopyCHURN RATE SUMMARY

Overall:           __% of customers churned

By Contract Type:
  Month-to-month:  __% churn  (n=____)
  One year:        __% churn  (n=____)
  Two year:        __% churn  (n=____)

Headline observation: ________________________________
[Example: "Month-to-month customers churn at 3x the rate of annual contract 
customers, suggesting contract type is the single strongest behavioral signal 
we have."]

💡 This template habit is portfolio gold. Framing numbers in plain language before building visualizations shows you think like an analyst, not just a coder.


🌙 Night 4 — Revenue Impact Quantification (~30 min)
Goal: Translate churn from a percentage into a dollar figure. This is what makes leadership pay attention.
This is the night that separates business analysts from data reporters:
pythonCopy# --- Monthly Recurring Revenue (MRR) at risk ---
total_mrr = df['MonthlyCharges'].sum()
churned_mrr = df[df['Churn_Flag'] == 1]['MonthlyCharges'].sum()
churned_customer_count = df['Churn_Flag'].sum()

print(f"Total Monthly Revenue (MRR):      ${total_mrr:,.0f}")
print(f"Revenue Lost to Churn (monthly):  ${churned_mrr:,.0f}")
print(f"MRR Churn Rate:                   {churned_mrr/total_mrr:.1%}")
print(f"Avg Monthly Revenue per Churner:  ${churned_mrr/churned_customer_count:,.2f}")

# --- Annual revenue loss projection ---
# This is the number that goes in the executive summary
annual_loss = churned_mrr * 12
print(f"\nProjected Annual Revenue Loss:    ${annual_loss:,.0f}")

# --- Lost lifetime value (LTV) estimation ---
# Average tenure of non-churners as a proxy for expected customer life
avg_tenure_retained = df[df['Churn_Flag'] == 0]['tenure'].mean()
avg_monthly_churner = churned_mrr / churned_customer_count

estimated_ltv_lost = churned_customer_count * avg_monthly_churner * avg_tenure_retained
print(f"Estimated Lost LTV (proxy):       ${estimated_ltv_lost:,.0f}")
Revenue breakdown by contract type:
pythonCopyrevenue_by_contract = (df.groupby(['Contract', 'Churn'])
                          .agg(
                              Customer_Count=('customerID', 'count'),
                              Total_Monthly_Revenue=('MonthlyCharges', 'sum'),
                              Avg_Monthly_Revenue=('MonthlyCharges', 'mean')
                          )
                          .round(2))
print(revenue_by_contract)
Tonight's win — write this paragraph in your notebook:
CopyREVENUE IMPACT STATEMENT

The business is losing approximately $[X] per month in recurring 
revenue to churn, or roughly $[Y] annualized. Month-to-month 
contract customers account for [Z]% of churned revenue despite 
being [W]% of the customer base. The average churned customer 
was paying $[amount]/month, suggesting [high/moderate/low]-value 
customers are disproportionately represented in the churned population.

Retaining even [10/20/30]% of churning customers would recover 
approximately $[calculated figure] in annual revenue.

💡 "Retaining X% would recover $Y" is the sentence that gets budgets approved. Business cases are built on quantified upside, not churn percentages. Practice writing this way.


🌙 Night 5 — Behavioral Patterns: What Do Churners Look Like? (~30 min)
Goal: Build a behavioral profile of the churned customer — demographics, services, billing.
pythonCopy# --- Churner vs Retained comparison table ---
# The fastest way to spot meaningful differences

profile_cols = ['MonthlyCharges', 'tenure', 'TotalCharges', 
                'Service_Count', 'Revenue_Per_Service']

churn_profile = (df.groupby('Churn')[profile_cols]
                   .mean()
                   .round(2)
                   .T)

churn_profile.columns = ['Retained', 'Churned']
churn_profile['Difference_%'] = ((churn_profile['Churned'] - churn_profile['Retained'])
                                   / churn_profile['Retained'] * 100).round(1)
print(churn_profile)
Categorical breakdown — find the high-churn combinations:
pythonCopy# Churn rate by paperless billing and payment method
billing_churn = (df.groupby(['PaperlessBilling', 'PaymentMethod'])
                   .agg(
                       Customers=('customerID', 'count'),
                       Churn_Rate=('Churn_Flag', 'mean')
                   )
                   .round(3)
                   .sort_values('Churn_Rate', ascending=False))
print(billing_churn)

# Churn rate by number of services (your engineered feature)
service_churn = (df.groupby('Service_Count')
                   .agg(
                       Customers=('customerID', 'count'),
                       Churn_Rate=('Churn_Flag', 'mean'),
                       Avg_Monthly=('MonthlyCharges', 'mean')
                   )
                   .round(3))
print(service_churn)
Monthly charges distribution — a telling visualization:
pythonCopyimport matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid', palette='muted')

fig, ax = plt.subplots(figsize=(10, 5))
sns.kdeplot(data=df, x='MonthlyCharges', hue='Churn', 
            fill=True, alpha=0.4, ax=ax)
ax.set_title('Monthly Charges Distribution: Churned vs. Retained Customers',
             fontweight='bold')
ax.set_xlabel('Monthly Charges ($)')
ax.set_ylabel('Density')
plt.tight_layout()
plt.savefig('../output/charts/monthly_charges_distribution.png', dpi=150)
plt.show()
Tonight's win — write the churner profile:
CopyCHURNER PROFILE

The typical churned customer:
- Had been a customer for approximately [X] months
- Was paying $[Y]/month (vs. $[Z] for retained customers)
- Was on a month-to-month contract
- Used [fewer/more] add-on services than retained customers
- Was [more/less] likely to be on paperless billing
- Was [more/less] likely to pay by electronic check

Interpretation: [2-3 sentences on what this pattern suggests]

🌙 Night 6 — Tenure Cohort Analysis: When Do Customers Leave? (~30 min)
Goal: Find out at which point in the customer lifecycle churn is highest. This tells you when to intervene.
This is the most technically interesting night of the project:
pythonCopy# --- Churn rate by tenure band ---
tenure_churn = (df.groupby('Tenure_Band', observed=True)
                  .agg(
                      Customers=('customerID', 'count'),
                      Churned=('Churn_Flag', 'sum'),
                      Churn_Rate=('Churn_Flag', 'mean'),
                      Avg_Monthly=('MonthlyCharges', 'mean'),
                      Avg_Services=('Service_Count', 'mean')
                  )
                  .round(3))
print(tenure_churn)

# --- Monthly churn rate (survival-style view) ---
# What % of customers who reached month N have churned by then?
monthly_churn = (df.groupby('tenure')
                   .agg(
                       Total_At_Tenure=('customerID', 'count'),
                       Churned_At_Tenure=('Churn_Flag', 'sum')
                   )
                   .assign(Churn_Rate_At_Tenure=lambda x: 
                           x['Churned_At_Tenure'] / x['Total_At_Tenure'])
                   .reset_index())

# Rolling average to smooth the line
monthly_churn['Churn_Rate_Rolling'] = (monthly_churn['Churn_Rate_At_Tenure']
                                        .rolling(window=3, center=True)
                                        .mean())
Visualize the lifecycle churn pattern:
pythonCopyfig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Churn rate by tenure band (bar)
tenure_churn['Churn_Rate'].plot(kind='bar', ax=axes[0], 
                                 color='#d73027', edgecolor='white')
axes[0].set_title('Churn Rate by Customer Tenure', fontweight='bold')
axes[0].set_ylabel('Churn Rate')
axes[0].set_xlabel('Tenure Band')
axes[0].tick_params(axis='x', rotation=30)

# Add percentage labels
for p in axes[0].patches:
    axes[0].annotate(f'{p.get_height():.1%}',
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='bottom', fontsize=10)

# Right: Rolling churn rate across months (line)
axes[1].plot(monthly_churn['tenure'], 
             monthly_churn['Churn_Rate_Rolling'],
             color='#4575b4', linewidth=2)
axes[1].fill_between(monthly_churn['tenure'],
                      monthly_churn['Churn_Rate_Rolling'],
                      alpha=0.2, color='#4575b4')
axes[1].set_title('Churn Rate Across Customer Lifecycle\n(3-Month Rolling Average)',
                   fontweight='bold')
axes[1].set_xlabel('Tenure (Months)')
axes[1].set_ylabel('Churn Rate')

plt.tight_layout()
plt.savefig('../output/charts/tenure_cohort_analysis.png', dpi=150)
plt.show()
Tonight's win:
CopyLIFECYCLE INSIGHT

Churn is highest in the [0-3 / 4-12 / 13-24] month cohort, 
with [X]% of customers in that window churning.

This suggests the business has a [new customer onboarding problem / 
mid-lifecycle engagement problem / long-term loyalty problem].

The intervention window — the period where a retention campaign 
would have the most impact — appears to be around months [X to Y].

💡 "Intervention window" is a term retention teams actually use. Using domain-appropriate language in your summary shows you understand how this analysis would be used, not just how it was built.


🌙 Night 7 — Risk Segmentation Framework (~30 min)
Goal: Build a simple, rules-based customer risk scoring system. No machine learning required — just logic and business sense.
This is the deliverable that could actually be handed to a customer success team:
pythonCopy# Define risk criteria based on everything you've learned this week
# Each condition gets a risk point — highest score = highest risk

def assign_risk_score(row):
    score = 0
    
    # Contract type is the strongest signal
    if row['Contract'] == 'Month-to-month':
        score += 3
    
    # Early tenure customers churn at higher rates
    if row['tenure'] <= 12:
        score += 2
    
    # High monthly charges without many services = low perceived value
    if row['MonthlyCharges'] > 65 and row['Service_Count'] < 2:
        score += 2
    
    # Electronic check payers churn at significantly higher rates
    if row['PaymentMethod'] == 'Electronic check':
        score += 1
    
    # No tech support or security = lower stickiness
    if row['TechSupport'] == 'No' and row['OnlineSecurity'] == 'No':
        score += 1
    
    # Paperless billing customers churn more
    if row['PaperlessBilling'] == 'Yes':
        score += 1
        
    return score

df['Risk_Score'] = df.apply(assign_risk_score, axis=1)

# Create risk tiers
df['Risk_Tier'] = pd.cut(df['Risk_Score'],
                          bins=[-1, 2, 4, 6, 10],
                          labels=['Low Risk', 'Moderate Risk', 
                                  'High Risk', 'Critical Risk'])
Validate your framework — does it actually predict churn?
pythonCopy# If your scoring is meaningful, churn rate should increase with risk tier
validation = (df.groupby('Risk_Tier', observed=True)
                .agg(
                    Customers=('customerID', 'count'),
                    Actual_Churn_Rate=('Churn_Flag', 'mean'),
                    Total_MRR=('MonthlyCharges', 'sum'),
                    MRR_At_Risk=('Revenue_At_Risk', 'sum')
                )
                .round(3))

print(validation)

# Calculate: what % of total churned revenue does each tier represent?
validation['Pct_of_Churned_Revenue'] = (
    validation['MRR_At_Risk'] / validation['MRR_At_Risk'].sum() * 100
).round(1)

print(validation)
Export the high-risk customer list — this is an actual deliverable:
pythonCopyhigh_risk = (df[df['Risk_Tier'].isin(['High Risk', 'Critical Risk'])]
               [['customerID', 'Contract', 'tenure', 'MonthlyCharges',
                 'Risk_Score', 'Risk_Tier', 'Churn']]
               .sort_values('Risk_Score', ascending=False))

high_risk.to_csv('../output/high_risk_customers.csv', index=False)
print(f"High-risk customers flagged: {len(high_risk)}")
print(f"MRR represented: ${high_risk['MonthlyCharges'].sum():,.0f}")

💡 Exporting a customer list with risk tiers is the kind of output that actually gets used. It bridges the gap between analysis and action — which is the whole point of business analytics.


🌙 Night 8 — SQL Practice Layer (~30 min)
Goal: Reproduce your key findings in SQL to show stack versatility.
pythonCopyimport sqlite3

conn = sqlite3.connect('../data/telco_churn.db')
df.to_sql('customers', conn, if_exists='replace', index=False)
Query 1 — Churn rate by contract type with revenue impact:
sqlCopySELECT 
    Contract,
    COUNT(*) AS Total_Customers,
    SUM(Churn_Flag) AS Churned_Customers,
    ROUND(AVG(CAST(Churn_Flag AS FLOAT)) * 100, 2) AS Churn_Rate_Pct,
    ROUND(SUM(MonthlyCharges), 2) AS Total_MRR,
    ROUND(SUM(CASE WHEN Churn_Flag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS Lost_MRR,
    ROUND(
        SUM(CASE WHEN Churn_Flag = 1 THEN MonthlyCharges ELSE 0 END) 
        / SUM(MonthlyCharges) * 100, 2
    ) AS MRR_Churn_Pct
FROM customers
GROUP BY Contract
ORDER BY Churn_Rate_Pct DESC;
Query 2 — Risk tier performance validation:
sqlCopySELECT
    Risk_Tier,
    COUNT(*) AS Customers,
    ROUND(AVG(CAST(Churn_Flag AS FLOAT)) * 100, 2) AS Churn_Rate_Pct,
    ROUND(SUM(MonthlyCharges), 2) AS Total_MRR,
    ROUND(AVG(MonthlyCharges), 2) AS Avg_Monthly_Charges
FROM customers
GROUP BY Risk_Tier
ORDER BY Churn_Rate_Pct DESC;
Query 3 — Window function: rank customers within each risk tier by revenue:
sqlCopySELECT
    customerID,
    Contract,
    MonthlyCharges,
    Risk_Tier,
    Risk_Score,
    RANK() OVER (
        PARTITION BY Risk_Tier 
        ORDER BY MonthlyCharges DESC
    ) AS Revenue_Rank_In_Tier
FROM customers
WHERE Churn_Flag = 0  -- Only current customers
  AND Risk_Tier IN ('High Risk', 'Critical Risk')
ORDER BY Risk_Tier, Revenue_Rank_In_Tier
LIMIT 20;

💡 Run each query via pd.read_sql_query(query, conn) and save the outputs. You can include the SQL in a separate notebook cell with a comment like # SQL equivalent of the pandas analysis above — showing both versions in the same notebook is a genuinely impressive pattern.


🌙 Night 9 — Polished Visuals & Mock Business Report (~30 min)
Your target: 6 charts that tell a sequential story
#Chart TypeStory It Tells1Grouped barChurn rate by contract type2KDE/distributionMonthly charges: churned vs retained3Bar with labelsChurn rate by tenure band4Stacked bar or heatmapRisk tier × contract type5Waterfall or barRevenue breakdown: total MRR vs lost MRR6Lollipop or dot plotTop behavioral factors associated with churn
Chart 5 — the revenue waterfall (most business-forward visual):
pythonCopyfig, ax = plt.subplots(figsize=(9, 5))

categories = ['Total MRR', 'MRR from\nRetained Customers', 'MRR Lost\nto Churn']
values = [total_mrr, total_mrr - churned_mrr, churned_mrr]
colors = ['#4575b4', '#74add1', '#d73027']

bars = ax.bar(categories, values, color=colors, width=0.5, edgecolor='white')

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 500,
            f'${val:,.0f}', ha='center', va='bottom', fontweight='bold')

ax.set_title('Monthly Recurring Revenue: Retention vs. Churn Impact',
             fontweight='bold', pad=15)
ax.set_ylabel('Monthly Revenue ($)')
ax.set_ylim(0, total_mrr * 1.15)
sns.despine()
plt.tight_layout()
plt.savefig('../output/charts/mrr_waterfall.png', dpi=150)
plt.show()
Your mock business report — the final markdown cell in your notebook:
markdownCopy# Telco Customer Churn Analysis
## Internal Analyst Report | Customer Success Team

---

### Executive Summary

Analysis of 7,043 customer records reveals a churn rate of **[X]%**, 
representing approximately **$[Y]/month** in lost recurring revenue 
or **$[Z] annualized**. The data points to three addressable drivers:
contract structure, early-tenure disengagement, and low service adoption 
among high-paying customers.

---

### Finding 1: Contract Type Is the Dominant Churn Driver

Month-to-month customers churn at **[X]%** — approximately [N]x the 
rate of annual contract customers. This cohort represents **[Y]%** of 
total churned revenue.

**Implication:** A contract conversion campaign targeting month-to-month 
customers showing early risk signals could have an outsized revenue impact.

---

### Finding 2: The First 12 Months Are the Danger Zone

**[X]%** of customers who churn do so within their first 12 months. 
The churn rate for the 0–3 month cohort is **[Y]%**, dropping 
significantly after month 24.

**Implication:** Onboarding quality and early engagement are likely 
causal factors. A 30/60/90-day customer health check program 
is worth modeling.

---

### Finding 3: High Monthly Charges + Low Service Adoption = Churn Risk

Customers paying over $65/month with fewer than 2 add-on services 
churn at **[X]%** — compared to **[Y]%** for customers with 
4+ services at similar price points.

**Implication:** These customers are not experiencing sufficient 
perceived value for their spend. A targeted upsell or bundle 
offer (particularly TechSupport and OnlineSecurity) could improve 
both retention and ARPU simultaneously.

---

### Risk Segmentation Output

A rules-based risk scoring model flagged **[N] customers** as 
High or Critical risk, representing **$[X]/month** in MRR. 
This customer list has been exported for prioritization by the 
retention team. The model correctly identifies customers with 
[Y]x higher actual churn rates than the low-risk population.

---

### Recommendations

| Priority | Action | Target Segment | Est. Revenue Impact |
|---|---|---|---|
| High | Contract conversion offer | M2M customers, Risk Score ≥ 4 | $X–Y/month retained |
| High | Early lifecycle check-in (day 60) | Tenure < 6 months | Reduce early churn by est. Z% |
| Medium | Bundle promotion | High spend, low service adoption | Dual retention + upsell |
| Low | Payment method incentive | Electronic check users | Reduces friction churn |

---

### Limitations & Next Steps

- **No causal data:** We observe correlation, not causation. 
  Support ticket history, NPS scores, and usage logs would strengthen findings.
- **Static snapshot:** This is point-in-time data, not a time series. 
  Longitudinal analysis would validate lifecycle findings.
- **No cost data:** Retention campaign ROI cannot be precisely modeled 
  without customer acquisition cost (CAC) and campaign cost inputs.
- **Recommended next step:** A/B test a contract conversion campaign 
  on a random 20% sample of flagged high-risk customers 
  to establish causal lift before full rollout.

🌙 Night 10 — README, GitHub & Reflection (~30 min)
Your README.md:
markdownCopy# Telco Customer Churn Analysis
### A Business Analytics Portfolio Project

## The Business Problem
A subscription telecom company is experiencing elevated churn. 
This analysis quantifies the revenue impact, identifies behavioral 
patterns in churned customers, and produces an actionable risk 
segmentation framework for the retention team.

## Key Findings
> - **$[X]/month** in MRR is lost to churn — **$[Y] annualized**
> - Month-to-month customers churn at **[N]x** the rate of annual contract holders
> - The highest-risk window is the **first 12 months** of a customer relationship
> - A rules-based risk model flagged **[N] high-risk customers** 
>   representing **$[X]/month** in at-risk revenue

## Tools & Methods
- **Python:** pandas, numpy, matplotlib, seaborn
- **SQL:** SQLite via Python (aggregations, window functions)
- **Techniques:** Cohort analysis, KDE distributions, 
  rules-based risk scoring, revenue impact modeling

## Project Structure
| Notebook | Contents |
|---|---|
| 01_exploration.ipynb | Data loading, first look, business framing |
| 02_analysis.ipynb | Cleaning, feature engineering, core analysis |
| 03_report.ipynb | Polished visuals, risk model, business summary |

## How to Run
1. Clone the repo
2. Download dataset from [Kaggle](link) → place in `/data`
3. `pip install -r requirements.txt`
4. Run notebooks in order

## Dataset
[Telco Customer Churn — IBM Sample Dataset via Kaggle](link)

Interview Talking Points
When someone asks you about this project, say this:

"I analyzed subscription churn data to quantify the revenue impact and find actionable patterns. The headline finding was that the business was losing roughly $X per month — but the more interesting insight was that customers on month-to-month contracts with fewer than two add-on services were churning at more than three times the rate of annual contract customers paying similar amounts. That suggested a perceived value problem, not just a price problem. I built a simple risk scoring model that flagged the highest-risk current customers, and I framed recommendations around a contract conversion campaign and an early-lifecycle check-in program. I also mapped out what additional data — support tickets, usage logs, NPS — would be needed to move from correlation to actual causal analysis."

That answer shows: business framing, technical execution, a clear insight, a deliverable, and intellectual honesty about limitations. That is what good analysts do.

Quick Reference Checklist
Copy✅ Night 1  — Data loaded, business questions written down
✅ Night 2  — Cleaned, TotalCharges fixed, features engineered
✅ Night 3  — Churn rate baseline cuts (contract, payment, internet)
✅ Night 4  — Revenue impact quantified in dollar terms
✅ Night 5  — Churner behavioral profile built
✅ Night 6  — Tenure cohort analysis + lifecycle chart
✅ Night 7  — Risk scoring model built and validated
✅ Night 8  — SQL queries written (3 minimum, window function included)
✅ Night 9  — 6 polished charts + full mock business report
✅ Night 10 — README done, pushed to GitHubAdd to Conversation