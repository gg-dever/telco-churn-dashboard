# Night 1

## Findings
- Target: Binary churn classification
- Initial count: 3 numerical cols, majority categorical
- Churn rate: ~26.5%
- Identified data quality issues in TotalCharges and SeniorCitizen

---

# Night 2

## Completed
- TotalCharges object -> numeric conversion
- SeniorCitizen binary -> categorical labels
- Tenure distribution analysis: bimodal at extremes
- Pearson correlation heatmap for numeric features
- Fixed heatmap error: filtered to numeric cols via select_dtypes
- Handled missing values from TotalCharges coercion
- Verified tenure type (Monthly)
- Confirmed final numeric vs categorical split
- Identified top categorical predictors
- Churn indicators visualized with key features

## Additional Completed
- Built final feature list: Contract, InternetService, PaymentMethod, tenure, MonthlyCharges, TotalCharges
- Encoded categoricals with OneHotEncoder in pipeline
- Train/test split with stratification (80/20)
- Trained logistic regression baseline (79% accuracy, 53% recall)
- Applied class weighting to improve recall (80% recall, AUC 0.85)
- Compared Random Forest vs Logistic Regression
- Generated confusion matrices and ROC curves
- Documented all metrics and model performance
- Summarized insights and business recommendations

---

# Night 3

## Completed
- Added hypothesis statements to all model sections (analytical framing)
- Created Service Engagement Model: tested if service features (OnlineSecurity, TechSupport, etc.) improve predictions beyond contract type
- Engineered `Service_Count` feature (counts add-on services per customer: 0-6 range)
- Analyzed service adoption vs churn: inverse correlation confirmed (4+ services = lower churn)
- Built Combined Model (13 features): contract + service features
- Created Services Only Model (7 features): tested services as standalone predictor
- Updated final comparison table: 4 model variants (Contract, Random Forest, Combined, Services Only)
- Key finding: Contract features dominate prediction (80% recall). Services add minimal lift but useful for behavioral segmentation
- Removed hyphens from all model names and descriptive text per style preference

---

# Night 4

## Completed
- **Feature Engineering Phase Complete**: Created all remaining business analysis features
- Engineered `Tenure_Band` (lifecycle segmentation: Trial/New/Renewal/Established/Loyal)
  - Validated churn concentration in first 12 months (60%+ of all churn)
  - Trial period (0 to 3mo) shows highest risk cohort
- Engineered `Revenue_At_Risk` (monthly revenue exposure from churned customers)
  - Month to month contracts: 42% of MRR at risk
  - Two year contracts: 3% of MRR at risk (validates contract conversion strategy)
- Engineered `Revenue_Per_Service` (value density metric)
  - Customers with 0 services: highest $/service, highest churn
  - Service bundling reduces churn via switching costs and ecosystem lock-in
- **Revenue Impact Quantification Complete**
  - Total MRR calculated: $456K across full customer base
  - Churned MRR: $139K per month lost to churn
  - Annual revenue loss: $1.67M
  - Average customer LTV: $1,531 (monthly charge × average tenure)
  - Formal REVENUE IMPACT STATEMENT section added with business context
- **Revenue Impact Visualization Complete**
  - Created single focused bar chart: revenue at risk by contract type
  - Built revenue exposure summary table with risk percentages
  - Key insight: Month to month = 42% risk, Two year = 3% risk
  - Simplified presentation for executive clarity (removed complex segmentation charts)
- **Night 4 Status**: Fully complete per project_guide.md specifications (all deliverables met)
- Dataset fully prepared for business analysis phases (behavioral profiling, risk segmentation, reporting)

---

# Night 5

## Completed
- **Behavioral Profiling Phase Complete**: Built comprehensive profile comparing churned vs retained customers
- **Numerical comparison table created**: Side-by-side stats for MonthlyCharges, tenure, TotalCharges, Service_Count, Revenue_Per_Service
  - Churners average 18 months tenure (vs 38 for retained - half the stay)
  - Churners pay $74/month (vs $61 - spending 21% more)
  - Churners use 1.8 services (vs 2.2 - less engaged)
  - Churners have higher revenue per service ($53 vs $32 - paying more, getting less value)
- **High-churn combination analysis**: Identified risky billing/payment patterns
  - Paperless billing + electronic check = highest churn rate combination
  - Electronic check payers show elevated churn across all billing types
- **Service adoption profiling**: Quantified churn rate by service count
  - 0-2 services: high churn risk
  - 4+ services: significantly lower churn (ecosystem lock-in effect)
- **Monthly charges KDE visualization**: Density plot comparing spending patterns between churned and retained customers
  - Saved to output/charts/monthly_charges_distribution.png
- **Comprehensive CHURNER PROFILE section**: Business-language summary of findings
  - Key insight documented: Not about price, about value perception
  - Higher monthly charges without service engagement = customers feel overcharged
  - Retention strategy identified: Bundle services at current price OR convert to annual contracts
- **Night 5 Status**: Fully complete per project_guide.md specifications

---

# Night 6

## Completed
- **Tenure Cohort Analysis Phase Complete**: Identified when customers leave during lifecycle
- **Tenure band segmentation**: Created 5 lifecycle cohorts (0-3mo, 4-12mo, 13-24mo, 25-48mo, 49-72mo)
  - 0-3 months: Highest churn rate across all cohorts
  - 4-12 months: Elevated churn continues but starts declining
  - 13-24 months: Significant drop - customers past 1 year tend to stay
  - 25+ months: Lowest churn - established customers are sticky
- **Monthly churn rate analysis**: Calculated churn rate at each tenure month with 3-month rolling average
  - Rolling average smooths the pattern to show clear lifecycle trend
  - Churn peaks early and steadily declines with increasing tenure
- **Two-panel lifecycle visualization**: Bar chart (tenure bands) + line chart (rolling monthly rate)
  - Saved to output/charts/tenure_cohort_analysis.png
  - Left panel shows churn by cohort, right panel shows continuous lifecycle view
- **LIFECYCLE INSIGHT section**: Business-language summary with retention strategy
  - Identified root cause: new customer onboarding problem, not long-term loyalty issue
  - **Intervention window defined**: Months 0-12 are critical retention period
  - Retention strategy prioritization:
    - Focus first 90 days on onboarding quality and early value demonstration
    - Target 4-12 month customers with engagement campaigns
    - Don't waste budget on 25+ month customers (already sticky)
    - Convert month-to-month to annual during 3-6 month window
- **Night 6 Status**: Fully complete per project_guide.md specifications

---

# To-Do

### ⚠️ Requires Consideration Before Moving Forward
- [x] **Feature engineering decision**: Currently using 6 features (Contract, InternetService, PaymentMethod, tenure, MonthlyCharges, TotalCharges)
  - Tested adding high-signal categorical features (OnlineSecurity, TechSupport, etc.)
  - Result: Combined model (13 features) matched baseline 80% recall—no meaningful improvement
  - Decision: Keep Contract Model as primary due to simplicity and interpretability
  - Services provide behavioral insights but not predictive lift

- [x] **Missing feature creation**: Project guide recommends engineering these columns:
  - ✅ `Service_Count` (number of add-on services customer has) - COMPLETED
  - ✅ `Tenure_Band` (lifecycle segmentation: 0-3mo, 4-12mo, 13-24mo, 25-48mo, 49-72mo) - COMPLETED
  - ✅ `Revenue_At_Risk` (MonthlyCharges × Churn_Flag for revenue analysis) - COMPLETED
  - ✅ `Revenue_Per_Service` (value density measure) - COMPLETED
  - All features validated with churn analysis—ready for business phases

- [x] **Model selection finalized?**: LogReg (80% recall, 0.85 AUC) chosen for interpretability
  - Contract Model selected over Combined Model (same performance, fewer features)
  - Services Only Model underperforms (61% recall, 0.78 AUC) - confirms contract dominance
  - Random Forest rejected (48% recall, lacks interpretability)
  - Decision: Contract Model (6 features) is final production model

---

## Next Steps - Business Analysis Phase

### Phase 1: Revenue Impact (Night 4 from guide)
- [x] Calculate total MRR (Monthly Recurring Revenue) - $456K
- [x] Quantify revenue lost to churn monthly/annually - $139K/month, $1.67M/year
- [x] Calculate estimated average customer LTV - $1,531
- [x] Break down churned revenue by contract type
- [x] Create revenue at risk visualization - bar chart by contract type
- [x] Build revenue exposure summary with risk percentages - 42% vs 3%
- [x] Write formal REVENUE IMPACT STATEMENT with business context
- **Status**: COMPLETED - Full Night 4 deliverables per project_guide.md specifications

### Phase 2: Behavioral Profiling (Night 5 from guide)
- [x] Build churner vs. retained customer comparison table
- [x] Analyze churn by payment method + billing type combinations
- [x] Visualize monthly charges distribution (churned vs retained)
- [x] Document "typical churner profile" in business language
- **Status**: COMPLETED - Churner profile reveals: 18mo avg tenure (vs 38 for retained), $74/month spending (21% higher), fewer services (1.8 vs 2.2), higher revenue per service ($53 vs $32). Key insight: churners pay more but perceive less value. Paperless billing + electronic check = highest risk combo.

### Phase 3: Lifecycle Analysis (Night 6 from guide)
- [x] Churn rate by tenure band (when do customers leave?)
- [x] Rolling churn rate across months (survival-style view)
- [x] Create lifecycle churn visualization
- [x] Identify "intervention window" where retention efforts would be most effective
- **Status**: COMPLETED - Tenure cohort analysis reveals 0-3 month cohort has highest churn risk (new customer onboarding problem). Churn drops significantly after 12 months. Intervention window: months 0-12 are critical. Rolling average shows churn peaks early and declines with tenure. Key finding: early-stage retention problem, not long-term loyalty issue. Retention strategy should focus on first 90 days and convert month-to-month to annual during 3-6 month window.

### Phase 4: Risk Segmentation (Night 7 from guide)
- [ ] Build rules-based risk scoring system using insights from analysis
- [ ] Assign risk tiers: Low / Moderate / High / Critical
- [ ] Validate framework: does churn rate increase with risk tier?
- [ ] Export high-risk customer list with risk scores
- [ ] Calculate MRR at risk by tier
- **Why this matters**: Actionable deliverable for retention team—actual customer list to contact

### Phase 5: SQL Practice Layer (Night 8 from guide)
- [ ] Create SQLite database from cleaned data
- [ ] Reproduce key findings in SQL (churn by contract, risk tier validation)
- [ ] Write window function queries (rank customers by revenue within risk tier)
- [ ] Include SQL code alongside pandas in notebook
- **Why this matters**: Shows stack versatility, most analyst roles require SQL

### Phase 6: Business Reporting (Night 9 from guide)
- [ ] Create 6-chart visual story: contract churn, charges distribution, tenure bands, risk tiers, revenue waterfall, behavioral factors
- [ ] Build revenue waterfall chart (total MRR → retained → lost)
- [ ] Write mock business report with Executive Summary
- [ ] Frame findings in business language with actionable recommendations
- **Why this matters**: Demonstrates communication skills—analysis that can't be explained is useless

### Phase 7: Documentation & Portfolio (Night 10 from guide)
- [ ] Write comprehensive README with business context, findings, and approach
- [ ] Add "Limitations" section: what data we wish we had
- [ ] Create 2-3 sentence project summary for resume
- [ ] Prepare for interview questions: "Walk me through this analysis"
- [ ] Polish notebook: clear sections, no dead code, executive summary up top

---

# Open Questions for Decision

1. **Scope**: Should we complete full business analysis (Nights 7-10) or keep focused on current depth?
   - Full analysis = risk segmentation framework, SQL layer, polished visuals + business report
   - Current depth = modeling showcase + revenue impact + behavioral profiling + lifecycle timing
   - **Current status**: Nights 1-6 complete (setup, cleaning, churn rates, revenue impact, behavioral profiling, lifecycle analysis). Nights 7-10 would add risk scoring system with customer list, SQL practice layer, visual storytelling, and portfolio documentation.

2. ~~**Feature expansion**: Add high-signal categoricals to model or keep current 6 features?~~ ✅ RESOLVED
   - Tested Combined Model (13 features) vs Contract Model (6 features)
   - Result: Same 80% recall, Contract Model wins for simplicity
   - Decision: Contract Model is final

3. **Time investment**: Full project guide = ~2-3 more nights of 30min sessions (Phases 4-7 remain)
   - Is this the priority project or should we move to next portfolio piece?
   - Strong foundation complete—remaining phases would add actionable risk tiers, SQL versatility demonstration, and executive-ready reporting polish

---

# Summary Status
- ✅ **Modeling Phase**: Complete (Contract Model: 80% recall, 0.85 AUC)
- ✅ **Model Comparison**: 4 variants tested, Contract Model selected
- ✅ **Feature Engineering**: Complete (Service_Count, Tenure_Band, Revenue_At_Risk, Revenue_Per_Service)
- ✅ **Business Features Validated**: Churn patterns confirmed across lifecycle, revenue, and service engagement dimensions
- ✅ **Revenue Impact Analysis**: Complete with full quantification ($139K monthly loss, $1.67M annual exposure, formal REVENUE IMPACT STATEMENT)
- ✅ **Night 4**: Fully complete per project_guide.md specifications (revenue metrics + business framing)
- ✅ **Night 5**: Behavioral profiling complete - churner vs retained comparison, high-churn combinations identified, monthly charges KDE plot, comprehensive churner profile documented
- ✅ **Night 6**: Tenure cohort analysis complete - lifecycle churn patterns identified, intervention window defined (0-12 months critical), two-panel visualization created, retention strategy prioritized
- 🔄 **Business Analysis Phase**: Phases 1-3 complete (Nights 1-6), Phases 4-7 remaining from project guide
- 📊 **Current Output**: Fully documented analysis notebook with hypothesis-driven sections, engineered business metrics, revenue quantification, behavioral profiling, lifecycle intervention windows, and executive ready impact statements
