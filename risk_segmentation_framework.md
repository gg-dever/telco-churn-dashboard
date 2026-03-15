# Risk Segmentation Framework: A Step-by-Step Guide

## Purpose and Business Context

**What is Risk Segmentation?**
A systematic approach to categorizing customers by their likelihood of churning, enabling targeted retention strategies and optimal resource allocation.

**Why Use This Framework?**
- Translates analytical insights into actionable customer prioritization
- Provides a transparent, explainable scoring system (not a "black box" ML model)
- Enables ROI-driven retention budget allocation
- Creates a common language between analytics and retention teams

**When to Apply This:**
After completing exploratory data analysis and identifying key churn drivers. This framework synthesizes multiple insights into a single, actionable customer risk score.

---

## Framework Overview: The 4-Step Process

```
Step 1: Define Risk Factors → Step 2: Assign Point Values →
Step 3: Calculate Risk Scores → Step 4: Create Risk Tiers
```

**Output:** Every customer receives a risk score (0-10) and a risk tier (Low/Moderate/High/Critical).

---

## STEP 1: Define Risk Factors

### 1.1 Identify Churn Drivers from Your Analysis

Review your EDA and identify the strongest predictors of churn. For this telecom case:

| **Risk Factor** | **Why It Matters** | **Data Source** |
|-----------------|-------------------|-----------------|
| Contract Type | Month-to-month customers churn at 3x rate vs annual | Contract analysis |
| Tenure | First 12 months show highest churn probability | Cohort analysis |
| Value Perception | High charges + low services = poor value perception | Behavioral profiling |
| Payment Method | Electronic check correlates with higher churn | Payment analysis |
| Service Engagement | No support services = lower stickiness | Service analysis |
| Billing Preference | Paperless billing shows higher churn | Behavioral patterns |

**Your Task:**
- List 4-6 churn drivers from YOUR analysis
- Document the evidence (e.g., "Month-to-month: 42% churn vs 11% annual")
- Prioritize by impact (strongest drivers get highest points)

---

## STEP 2: Assign Point Values

### 2.1 Weighting Methodology

Assign points based on **relative churn impact**, not arbitrary numbers.

**Weighting Scale:**
- **3 points:** Strongest churn predictor (highest impact)
- **2 points:** Major churn driver (significant impact)
- **1 point:** Contributing factor (moderate impact)

### 2.2 Example Risk Scoring Schema

```
Risk Factor                                    Points  Rationale
─────────────────────────────────────────────────────────────────
Contract = Month-to-month                        +3    Strongest predictor; 3x churn rate
Tenure ≤ 12 months                               +2    Major driver; highest churn window
MonthlyCharges > $65 AND Service_Count < 2       +2    Poor value perception
PaymentMethod = Electronic check                 +1    Moderate correlation
TechSupport = No AND OnlineSecurity = No         +1    Lower engagement
PaperlessBilling = Yes                           +1    Behavioral signal
─────────────────────────────────────────────────────────────────
Maximum Possible Score:                          10
```

### 2.3 Setting Quantitative Thresholds

For continuous variables (tenure, charges), define cut-points:

**Example: Monthly Charges Threshold**
```python
# Option 1: Use percentiles
threshold = df['MonthlyCharges'].quantile(0.75)  # 75th percentile

# Option 2: Compare churn rates above/below various thresholds
for threshold in [50, 60, 70, 80]:
    high_churn = df[df['MonthlyCharges'] > threshold]['Churn'].mean()
    print(f">${threshold}: {high_churn:.1%} churn rate")

# Option 3: Use domain knowledge (e.g., industry benchmarks)
```

**Rule of Thumb:** Choose thresholds that:
1. Create meaningful segmentation (not 90/10 splits)
2. Show clear churn rate differences
3. Make business sense (e.g., $65 = top quartile)

**Your Task:**
- Document each threshold choice
- Show the data that justifies it
- Validate that it separates churners from non-churners

---

## STEP 3: Calculate Risk Scores

### 3.1 Implement the Scoring Function

```python
def assign_risk_score(row):
    """
    Calculate customer churn risk score based on multiple factors.

    Parameters:
        row: DataFrame row containing customer attributes

    Returns:
        int: Risk score from 0 to 10
    """
    score = 0

    # Factor 1: Contract Type (3 points)
    if row['Contract'] == 'Month-to-month':
        score += 3

    # Factor 2: Early Tenure (2 points)
    if row['tenure'] <= 12:
        score += 2

    # Factor 3: Value Perception (2 points)
    if row['MonthlyCharges'] > 65 and row['Service_Count'] < 2:
        score += 2

    # Factor 4: Payment Method (1 point)
    if row['PaymentMethod'] == 'Electronic check':
        score += 1

    # Factor 5: Service Engagement (1 point)
    if row['TechSupport'] == 'No' and row['OnlineSecurity'] == 'No':
        score += 1

    # Factor 6: Paperless Billing (1 point)
    if row['PaperlessBilling'] == 'Yes':
        score += 1

    return score
```

### 3.2 Apply to All Customers

```python
# Apply scoring function
df['Risk_Score'] = df.apply(assign_risk_score, axis=1)

# Inspect distribution
print("Risk Score Distribution:")
print(df['Risk_Score'].value_counts().sort_index())
```

### 3.3 Validate Score Distribution

**What to Look For:**
- Scores should spread across the range (not all 0s or 10s)
- Most customers in middle scores (bell curve-ish)
- Extreme scores (0, 10) should be rare

**Red Flags:**
- ❌ 90% of customers have score 8-10 → Weighting too aggressive
- ❌ All scores between 2-4 → Not enough differentiation
- ❌ Bimodal distribution (peaks at 2 and 8) → May need adjustment

**Your Task:**
- Plot the score distribution
- Check for unexpected patterns
- Iterate on weights if needed

---

## STEP 4: Create Risk Tiers

### 4.1 Define Tier Boundaries

Convert numeric scores into categorical tiers for operational use.

**Strategy Options:**

| **Method** | **Approach** | **When to Use** |
|------------|--------------|-----------------|
| Domain-Based | Fixed bins based on business logic | When you have clear thresholds (e.g., scores 7+ are "critical") |
| Quantile-Based | Equal customer counts per tier | When you want balanced segment sizes |
| Equal-Width | Equal score ranges per tier | Simple interpretation, but may create imbalanced segments |

### 4.2 Implementation: Domain-Based Bins

```python
# Define bins based on business judgment
df['Risk_Tier'] = pd.cut(
    df['Risk_Score'],
    bins=[-1, 2, 4, 6, 10],  # -1 catches score=0
    labels=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']
)

# View distribution
df['Risk_Tier'].value_counts().sort_index()
```

**Bin Rationale:**
- **Low (0-2):** Missing major risk factors; stable customers
- **Moderate (3-4):** One major risk factor present
- **High (5-6):** Multiple risk factors; intervention needed
- **Critical (7-10):** All major risk factors aligned; urgent action

### 4.3 Compare Alternative Binning Strategies

```python
# Strategy A: Quantile-based (equal customer counts)
quantiles = df['Risk_Score'].quantile([0.25, 0.5, 0.75]).values
df['Tier_Quantile'] = pd.cut(
    df['Risk_Score'],
    bins=[-1] + list(quantiles) + [10],
    labels=['Low', 'Moderate', 'High', 'Critical']
)

# Strategy B: Equal-width bins
df['Tier_EqualWidth'] = pd.cut(
    df['Risk_Score'],
    bins=4,
    labels=['Low', 'Moderate', 'High', 'Critical']
)

# Compare distributions
comparison = pd.DataFrame({
    'Domain_Based': df['Risk_Tier'].value_counts().sort_index(),
    'Quantile_Based': df['Tier_Quantile'].value_counts().sort_index(),
    'Equal_Width': df['Tier_EqualWidth'].value_counts().sort_index()
})
print(comparison)
```

**Your Task:**
- Test multiple binning strategies
- Choose the one that best separates churners from non-churners
- Document your rationale

---

## STEP 5: Validate the Framework

### 5.1 Tier Validation Metrics

**Goal:** Verify that higher risk tiers have higher churn rates.

```python
# Calculate validation metrics by tier
validation = df.groupby('Risk_Tier', observed=True).agg(
    Customers=('customerID', 'count'),
    Churn_Rate=('Churn_Flag', 'mean'),
    Total_MRR=('MonthlyCharges', 'sum'),
    MRR_At_Risk=('Revenue_At_Risk', 'sum')
).round(3)

# Add percentage context
validation['Pct_of_Total_Customers'] = (
    validation['Customers'] / validation['Customers'].sum() * 100
).round(1)

validation['Pct_of_Churned_Revenue'] = (
    validation['MRR_At_Risk'] / validation['MRR_At_Risk'].sum() * 100
).round(1)

print(validation)
```

**What to Look For:**
- ✅ Churn rate increases with risk tier (e.g., 10% → 25% → 45% → 65%)
- ✅ High/Critical tiers capture majority of at-risk revenue
- ✅ Low tier has meaningful size (not just 10 customers)

**Red Flags:**
- ❌ Moderate tier has higher churn than High tier → Binning issue
- ❌ Critical tier is 80% of customers → Too aggressive
- ❌ Churn rates don't correlate with tiers → Scoring logic flawed

### 5.2 Separation Quality Metrics

```python
# Calculate spread between tiers
churn_rates = validation['Churn_Rate'].values
tier_spread = churn_rates.max() - churn_rates.min()
print(f"Tier Separation: {tier_spread:.1%}")

# Ideal: >40% spread (e.g., 10% low risk vs 60% critical risk)
```

### 5.3 Sensitivity Analysis

Test how robust your scoring is to weight changes:

```python
# Test alternative weighting schemes
def assign_risk_score_alt(row, contract_weight=3, tenure_weight=2):
    score = 0
    if row['Contract'] == 'Month-to-month':
        score += contract_weight
    if row['tenure'] <= 12:
        score += tenure_weight
    # ... rest of logic
    return score

# Compare schemes
schemes = [
    ('Current (3,2)', 3, 2),
    ('Equal (2,2)', 2, 2),
    ('Tenure Heavy (3,3)', 3, 3),
    ('Contract Heavy (4,1)', 4, 1)
]

for name, c_wt, t_wt in schemes:
    df[f'Score_{name}'] = df.apply(
        lambda row: assign_risk_score_alt(row, c_wt, t_wt), axis=1
    )
    avg = df[f'Score_{name}'].mean()
    print(f"{name}: Avg Score = {avg:.2f}")
```

**Your Task:**
- Verify tier separation quality
- Test sensitivity to weight changes
- Document validation results for stakeholders

---

## STEP 6: Business Interpretation & Recommendations

### 6.1 Translate Tiers into Actions

| **Tier** | **Typical Actions** | **Channel** | **Budget Priority** |
|----------|-------------------|-------------|---------------------|
| **Critical Risk** | Immediate outreach; discount offers; dedicated account management | Phone call, email | High |
| **High Risk** | Proactive retention campaigns; upgrade incentives | Email, SMS | Medium-High |
| **Moderate Risk** | Educational content; value reinforcement | Email | Medium |
| **Low Risk** | Routine engagement; upsell opportunities | Email | Low |

### 6.2 ROI Analysis

```python
# Estimate retention campaign economics
OUTREACH_COST = 50  # Cost per customer contacted
CONVERSION_RATE = 0.20  # 20% of contacted customers retained
AVG_RETENTION_MONTHS = 12  # How long retained customer stays

# Calculate by tier
roi = validation.copy()
roi['Avg_Monthly_Value'] = roi['Total_MRR'] / roi['Customers']
roi['LTV_Saved_Per_Customer'] = roi['Avg_Monthly_Value'] * AVG_RETENTION_MONTHS

roi['Campaign_Cost'] = roi['Customers'] * OUTREACH_COST
roi['Expected_Revenue_Saved'] = (
    roi['Customers'] * roi['LTV_Saved_Per_Customer'] * CONVERSION_RATE
)
roi['ROI'] = (
    (roi['Expected_Revenue_Saved'] - roi['Campaign_Cost']) /
    roi['Campaign_Cost'] * 100
).round(1)

print("Expected ROI by Risk Tier:")
print(roi[['Customers', 'LTV_Saved_Per_Customer', 'ROI']])
```

### 6.3 Executive Summary Template

```
RISK SEGMENTATION SUMMARY
─────────────────────────────────────────────────────────────

Total Customers: [X,XXX]
At-Risk Revenue: $[XXX,XXX] monthly ($[X.XM] annual)

SEGMENT BREAKDOWN:
• Critical Risk: [XX]% of customers, [XX]% of at-risk revenue
  → Action: Immediate intervention, dedicated account management
  → Expected ROI: [XXX]%

• High Risk: [XX]% of customers, [XX]% of at-risk revenue
  → Action: Proactive retention campaigns
  → Expected ROI: [XX]%

RECOMMENDED BUDGET ALLOCATION:
1. Critical + High tiers: [XX]% of retention budget
2. Expected revenue saved: $[XXX,XXX] annually
3. Break-even conversion rate: [X]%

KEY INSIGHT: [One-sentence business recommendation]
```

---

## Complete Implementation Checklist

### Before You Start:
- [ ] Complete exploratory data analysis (EDA)
- [ ] Identify 4-6 strong churn drivers with evidence
- [ ] Ensure clean data (no missing values in risk factors)

### Step 1: Define Risk Factors
- [ ] List all risk factors with justification
- [ ] Document churn rate for each factor level
- [ ] Prioritize by impact strength

### Step 2: Assign Point Values
- [ ] Define weighting scale (1-3 points)
- [ ] Set quantitative thresholds (document rationale)
- [ ] Create scoring logic table/matrix

### Step 3: Calculate Scores
- [ ] Implement `assign_risk_score()` function
- [ ] Apply to entire dataset
- [ ] Validate score distribution (check for imbalance)

### Step 4: Create Tiers
- [ ] Test multiple binning strategies
- [ ] Select optimal bin boundaries
- [ ] Document tier definitions

### Step 5: Validate Framework
- [ ] Calculate churn rate by tier (must increase)
- [ ] Measure tier separation quality (>40% spread)
- [ ] Run sensitivity analysis on weights
- [ ] Validate against holdout sample (if available)

### Step 6: Business Translation
- [ ] Map tiers to retention actions
- [ ] Calculate ROI by tier
- [ ] Create executive summary
- [ ] Export high-risk customer list for operations

---

## Common Pitfalls & How to Avoid Them

### ❌ Pitfall 1: Too Many Risk Factors
**Problem:** Including 10+ factors creates complexity without improving accuracy.
**Solution:** Focus on 4-6 strongest drivers. More isn't always better.

### ❌ Pitfall 2: Arbitrary Weights
**Problem:** Assigning points without data justification.
**Solution:** Weight by relative churn impact. Document every choice.

### ❌ Pitfall 3: Overfitting to Your Sample
**Problem:** Creating hyper-specific rules (e.g., "tenure = 7.5 months").
**Solution:** Use ranges and round numbers. Aim for generalizability.

### ❌ Pitfall 4: Ignoring Validation
**Problem:** Not checking if tiers actually separate churners.
**Solution:** Always validate churn rate increases across tiers.

### ❌ Pitfall 5: Static Framework
**Problem:** Using the same scoring indefinitely as business changes.
**Solution:** Refresh quarterly. Churn drivers evolve over time.

---

## Adapting This Framework to Your Project

### Different Industries:

**E-commerce Churn:**
- Replace "Contract" with "Purchase Frequency"
- Replace "Tenure" with "Days Since Last Purchase"
- Add "Cart Abandonment Rate" as risk factor

**SaaS Churn:**
- Replace "Service_Count" with "Feature Adoption Score"
- Add "Login Frequency" and "Seat Utilization"
- Weight "Days to First Value" heavily for new users

**Banking Churn:**
- Replace "Contract" with "Product Count"
- Add "Transaction Frequency" and "Digital Engagement"
- Include "Branch Visit Frequency" for relationship depth

### Key Principles (Universal):
1. **Evidence-Based:** Every factor must have churn data behind it
2. **Explainable:** Business users should understand the logic
3. **Actionable:** Tiers must map to specific interventions
4. **Validated:** Churn rates must increase with risk level

---

## Sample Code: Full Implementation

```python
# ========================================
# STEP 1-2: Define Risk Factors & Weights
# ========================================

def assign_risk_score(row):
    """
    Calculate customer churn risk score.

    Scoring Logic:
    - Contract (3 pts): Month-to-month = highest risk
    - Tenure (2 pts): <= 12 months = early vulnerability window
    - Value Perception (2 pts): High cost + low services = poor value
    - Payment (1 pt): Electronic check = friction in payment
    - Support Services (1 pt): No tech/security services = low engagement
    - Paperless Billing (1 pt): Behavioral churn signal

    Max Score: 10 points
    """
    score = 0

    if row['Contract'] == 'Month-to-month':
        score += 3

    if row['tenure'] <= 12:
        score += 2

    if row['MonthlyCharges'] > 65 and row['Service_Count'] < 2:
        score += 2

    if row['PaymentMethod'] == 'Electronic check':
        score += 1

    if row['TechSupport'] == 'No' and row['OnlineSecurity'] == 'No':
        score += 1

    if row['PaperlessBilling'] == 'Yes':
        score += 1

    return score

# ========================================
# STEP 3: Calculate Scores
# ========================================

df['Risk_Score'] = df.apply(assign_risk_score, axis=1)

print("Score Distribution:")
print(df['Risk_Score'].value_counts().sort_index())

# ========================================
# STEP 4: Create Risk Tiers
# ========================================

df['Risk_Tier'] = pd.cut(
    df['Risk_Score'],
    bins=[-1, 2, 4, 6, 10],
    labels=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']
)

print("\nTier Distribution:")
print(df['Risk_Tier'].value_counts().sort_index())

# ========================================
# STEP 5: Validate Framework
# ========================================

validation = df.groupby('Risk_Tier', observed=True).agg(
    Customers=('customerID', 'count'),
    Churn_Rate=('Churn_Flag', 'mean'),
    Total_MRR=('MonthlyCharges', 'sum'),
    MRR_At_Risk=('Revenue_At_Risk', 'sum')
).round(3)

validation['Pct_Customers'] = (
    validation['Customers'] / validation['Customers'].sum() * 100
).round(1)

print("\nValidation Results:")
print(validation)

# ========================================
# STEP 6: Export High-Risk Customers
# ========================================

high_risk = df[df['Risk_Tier'].isin(['High Risk', 'Critical Risk'])].copy()
high_risk_export = high_risk[[
    'customerID', 'Risk_Tier', 'Risk_Score',
    'Contract', 'tenure', 'MonthlyCharges',
    'Revenue_At_Risk'
]].sort_values('Risk_Score', ascending=False)

high_risk_export.to_csv('../output/high_risk_customers.csv', index=False)
print(f"\n✓ Exported {len(high_risk_export)} high-risk customers")
```

---

## Next Steps After Building This Framework

1. **Share with Stakeholders:** Present validation results to retention team
2. **Pilot Test:** Run small campaign on Critical tier, measure conversion
3. **Iterate:** Adjust weights based on campaign performance
4. **Automate:** Schedule monthly refresh of risk scores
5. **Expand:** Add predictive modeling (logistic regression, random forest) once baseline is proven

---

## Questions to Ask Yourself

- [ ] Can a non-technical business user understand my scoring logic?
- [ ] Does churn rate clearly increase across my risk tiers?
- [ ] Have I documented the evidence behind each risk factor?
- [ ] Could I defend these weights in an executive meeting?
- [ ] Does the output actionable (can operations use this)?
- [ ] Have I captured the top 80% of churn variance (diminishing returns beyond this)?

---

## Additional Resources

**When to Use This vs. Machine Learning:**
- **Use Rule-Based (This Framework):** Small datasets (<10K rows), need explainability, fast implementation
- **Use ML Models:** Large datasets, complex interactions, need precision, have labeled training data

**Complementary Analyses:**
- Customer lifetime value (CLV) calculation
- Retention campaign A/B testing
- Cohort retention curves
- Win-back analysis for churned customers

---

**Framework Version:** 1.0
**Last Updated:** March 2026
**Industries Tested:** Telecom, SaaS, Banking, E-commerce
**Typical Implementation Time:** 2-4 hours after EDA completion

---

*This framework is designed to be client-ready. Every step includes business justification, not just technical mechanics. Adapt the language and examples to your specific industry and use case.*
