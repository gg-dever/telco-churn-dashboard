# Risk Segmentation Analysis Results

## Summary of Risk Factor Data

### Risk Factor 1: Contract Type
**Month-to-month contract**
- Churn Rate: 42.7%
- Relative Risk: 15.3x (compared to Two year)
- Relative to One Year: 3.8x
- Churned Customers: 1,655 out of 3,875

**One year contract**
- Churn Rate: 11.3%
- Churned Customers: 166 out of 1,473

**Two year contract**
- Churn Rate: 2.8%
- Churned Customers: 48 out of 1,695

---

### Risk Factor 2: Customer Tenure
**Tenure ≤12 months**
- Churn Rate: 47.4%
- Relative Risk: 2.8x
- This segment represents early-stage customers

**Tenure 13+ months**
- Churn Rate: 17.0% (baseline)
- More established customer base

---

### Risk Factor 3: Value Perception
**High Cost Low Value (>$65/month with <2 services)**
- Churn Rate: 57.8%
- Relative Risk: 2.7x
- Indicates pricing-to-engagement imbalance

**Other customers**
- Churn Rate: 21.3% (baseline)

---

### Risk Factor 4: Payment Method
**Electronic check payment**
- Churn Rate: 45.3%
- Relative Risk: 2.6x
- May indicate lower digital engagement

**Other payment methods**
- Churn Rate: 17.4% (baseline)

---

### Risk Factor 5: Service Engagement
**Low Engagement (No TechSupport AND No OnlineSecurity)**
- Churn Rate: 49.0%
- Relative Risk: 3.6x
- Churned Customers: 1,250 out of 2,553

**Other (at least one protective service)**
- Churn Rate: 13.8% (baseline)
- Churned Customers: 619 out of 4,490

---

### Risk Factor 6: Paperless Billing
**Paperless billing**
- Churn Rate: 33.6%
- Relative Risk: 2.1x
- Churned Customers: 1,400 out of 4,171

**Other (paper billing)**
- Churn Rate: 16.3% (baseline)
- Churned Customers: 469 out of 2,872

---

## Risk Factor Comparison

| Risk Factor | Churn Rate | Relative Risk | Current Points |
|-------------|-----------|---------------|----------------|
| Month-to-month contract | 42.7% | 15.3x | 3 |
| Tenure ≤12 months | 47.4% | 2.8x | 2 |
| High charges + few services | 57.8% | 2.7x | 2 |
| Electronic check payment | 45.3% | 2.6x | 1 |
| No tech/security services | 49.0% | **3.6x** | 1 ⚠️ |
| Paperless billing | 33.6% | 2.1x | 1 |

**Key Finding:** Service engagement (3.6x relative risk) is significantly underweighted at 1 point, while factors with lower relative risk (2.7x, 2.8x) receive 2 points.

---

## Recommended Point Adjustments

Based on relative risk ordering:

1. **Month-to-month contract** → 3 points (15.3x - clearly strongest)
2. **No tech/security services** → 2 points (3.6x - second strongest)
3. **Tenure ≤12 months** → 2 points (2.8x)
4. **High charges + few services** → 2 points (2.7x)
5. **Electronic check payment** → 1 point (2.6x - borderline but close to 2-point tier)
6. **Paperless billing** → 1 point (2.1x - weakest signal)

**New Total Maximum Score:** 11 points (instead of 10)

---

## Validation Results (Current Implementation)

### Risk Tier Distribution
- **Low Risk (0-2 points):** 2,973 customers (42.2%)
- **Moderate Risk (3-4 points):** 883 customers (12.5%)
- **High Risk (5-6 points):** 1,688 customers (24.0%)
- **Critical Risk (7-10 points):** 1,499 customers (21.3%)

### Churn Rate by Tier
- **Low Risk:** 6.1% churn rate (181/2,973)
- **Moderate Risk:** 18.6% churn rate (164/883)
- **High Risk:** 35.8% churn rate (604/1,688)
- **Critical Risk:** 61.4% churn rate (920/1,499)

### Revenue at Risk by Tier
- **Low Risk:** $15,607.50 MRR at risk
- **Moderate Risk:** $12,838.55 MRR at risk
- **High Risk:** $43,520.70 MRR at risk
- **Critical Risk:** $67,164.10 MRR at risk

**Total MRR at Risk:** $139,130.85

---

## Framework Performance

✅ **Good tier separation:** Churn rate increases from 6.1% → 18.6% → 35.8% → 61.4%

✅ **Strong predictive power:** 10x difference between Low and Critical risk tiers

✅ **Actionable segments:** High + Critical represent 45.3% of customers but 80% of at-risk revenue
