# Telco Customer Churn Analysis - Project Summary

## 📋 Quick Overview
**Project Type:** Customer Analytics & Retention Strategy
**Domain:** Telecommunications
**Timeline:** 2-3 weeks of analysis
**Tools:** Python, Pandas, Scikit-learn, Matplotlib, Seaborn, SQLite

---

## 🎯 Business Problem
Telecom company experiencing **26.5% customer churn rate**, resulting in **$1.67 million annual revenue loss**. Leadership needed to:
- Understand which customers are most likely to churn
- Identify early warning signs
- Prioritize retention efforts effectively

---

## 🔍 My Approach

### 1. **Exploratory Data Analysis**
- Analyzed 7,043 customer records with 21 features
- Fixed data quality issues (TotalCharges type conversion, missing value imputation)
- Identified key patterns: contract type, tenure, service adoption, payment methods

### 2. **Predictive Modeling**
- Built Logistic Regression model with class balancing
- Achieved **80% recall** (catches 4 out of 5 churners)
- **AUC = 0.85** (strong discriminative ability)
- Prioritized recall over precision for retention use case

### 3. **Behavioral Profiling**
- Churned customers pay **21% more monthly** but receive **fewer services**
- Tenure half that of retained customers (18 vs 38 months)
- Identified high-risk payment/billing combinations

### 4. **Risk Segmentation Framework**
- Developed rule-based scoring system (0-11 points)
- Created 4 risk tiers with validated churn separation
- Exported 2,598 high-risk customers for retention outreach

---

## 💡 Key Findings

### Finding #1: Contract Type Dominates Churn Risk
- Month-to-month customers: **42.7% churn rate**
- Two-year contract customers: **2.8% churn rate**
- **15x difference** — primary retention lever identified

### Finding #2: First 12 Months Are Critical
- 0-12 month customers: **47.4% churn rate**
- 13+ month customers: **17.1% churn rate**
- Early-stage retention problem requiring onboarding intervention

### Finding #3: Value Perception Gap
- High-cost (>$65/month) + low-service (<2 add-ons): **57.8% churn rate**
- Premium pricing without sufficient bundling drives dissatisfaction

---

## 📊 Business Impact & Recommendations

### Revenue Exposure Quantified
- **$139,128** monthly recurring revenue lost to churn
- **$1.67M** annual revenue exposure
- Month-to-month contracts represent **47%** of at-risk revenue

### High-Priority Actions
1. **Contract conversion campaigns** for month-to-month customers with Risk Score ≥6
   - Estimated impact: $10-15K monthly revenue preserved

2. **Early lifecycle check-ins** at 60-day mark for new customers
   - Target: 15-20% reduction in early-stage churn

3. **Bundle promotions** for high-cost, low-service customers
   - Dual benefit: retention + upsell opportunity

### Risk Segmentation Output
- **2,598 customers** flagged as High/Critical risk
- **$100,668/month** in at-risk MRR identified
- Actionable customer list delivered for retention team

---

## 🛠️ Technical Highlights

### Data Processing
- Handled missing values with business logic (0 imputation for new customers)
- Created engineered features (Service_Count, Tenure_Bands, Risk_Score)

### Modeling Approach
- Addressed class imbalance using `class_weight='balanced'`
- Compared Logistic Regression vs Random Forest
- Selected interpretable model for stakeholder communication

### Validation
- SQL queries to validate findings
- Risk tier churn rates increase monotonically (5.4% → 62.9%)
- Framework validation confirms predictive accuracy

---

## 📁 Deliverables

1. **Portfolio Notebook** - Streamlined 20-minute analysis walkthrough
2. **Technical Notebook** - Full deep-dive with methodology details
3. **High-Risk Customer List (CSV)** - 2,598 customers prioritized for outreach
4. **Executive Visualizations** - 4 publication-ready charts
5. **Business Recommendations** - Prioritized retention strategies with ROI estimates

---

## 💼 Skills Demonstrated

✅ **Business Analysis** - Translating data insights into revenue impact
✅ **Statistical Modeling** - Logistic regression, class imbalance handling
✅ **Data Visualization** - Publication-quality charts for executive audience
✅ **SQL** - Database queries for validation and production readiness
✅ **Feature Engineering** - Business-relevant metrics and scoring systems
✅ **Communication** - Technical findings → actionable recommendations

---

## 🔗 Links

**GitHub Repository:** [Insert your repo URL]
**Live Notebook (HTML):** [Link to HTML version if hosted]
**LinkedIn:** [Your LinkedIn URL]
**Portfolio:** [Your portfolio website]

---

## ⏱️ Project Stats

- **Dataset Size:** 7,043 customer records, 21 features
- **Lines of Code:** ~850 (portfolio) / ~2,100 (full analysis)
- **Key Metrics Memorized:** 10+ business-critical numbers
- **Visualizations Created:** 8+ charts and graphs
- **Analysis Time:** 2-3 weeks

---

**Questions about this project? Let's discuss how these analytical approaches can solve your business challenges.**

---
*Created: March 2026*
*Status: Complete & Portfolio-Ready*
