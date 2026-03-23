# Interview Talking Points - Telco Churn Project

## 🎤 The 2-Minute Project Walkthrough

**Opening (15 seconds):**
"This project analyzes customer churn for a telecom company losing $1.67 million annually. My goal was to identify which customers are most likely to leave and provide actionable retention strategies."

**Approach (45 seconds):**
"I started with exploratory analysis of 7,000+ customer records, fixed data quality issues, and discovered three key patterns: contract type is the dominant predictor, the first 12 months are critical for retention, and there's a value perception gap where high-paying customers with few services churn at nearly 60%.

I built a logistic regression model achieving 80% recall—meaning we catch 4 out of 5 customers who will actually churn. I prioritized recall over precision because missing a churner costs more than a false alarm."

**Impact (30 seconds):**
"The output is a risk segmentation framework that scores every customer 0-11 points and identifies 2,598 high-risk customers representing over $100K in monthly revenue exposure. I provided a prioritized customer list to the retention team with specific recommendations like contract conversion campaigns and early lifecycle check-ins."

**Close (15 seconds):**
"The analysis is fully reproducible, includes SQL validation for production deployment, and I built an interactive Streamlit dashboard deployed to the cloud where stakeholders can explore the data, score new customers, and calculate retention campaign ROI."

---

## 📊 Key Numbers to Memorize

**Revenue Impact:**
- 26.5% baseline churn rate
- $139,128 lost per month
- $1.67 million annual revenue exposure
- $100K+ monthly revenue at risk from high-risk segment

**Churn Drivers:**
- Month-to-month: 42.7% churn vs Two-year: 2.8% churn (15x difference)
- First year: 47.4% churn vs 13+ months: 17.1% churn
- High cost + low service: 57.8% churn rate

**Model Performance:**
- 80% recall (catches 4 of 5 churners)
- AUC = 0.85 (strong discrimination)
- 2,598 high-risk customers identified

**Dataset:**
- 7,043 customer records
- 21 features
- 4 risk tiers created

---

## 💬 Common Interview Questions & Answers

### Q: "Walk me through this project"
**Answer:**
"I analyzed telecom customer churn to help a retention team prioritize outreach. The data showed a 26.5% churn rate costing $1.67M annually. I used exploratory analysis to identify contract type as the strongest predictor—month-to-month customers churn 15 times more than two-year contracts. I built a logistic regression model with 80% recall, then created a rule-based risk scoring system that's easy for business teams to understand. The output was a list of 2,598 high-risk customers and specific recommendations like targeting month-to-month customers in their first year with contract conversion offers."

---

### Q: "What was your biggest challenge?"
**Answer:**
"Class imbalance and the recall-precision trade-off. The dataset had 3:1 more non-churners, so a naive model would just predict everyone stays. I addressed this with class balancing and explicitly optimized for recall because the business cost of missing a churner—losing their lifetime value—far exceeds the cost of a false positive, which is just a wasted retention offer. I validated this worked by comparing to Random Forest, which underperformed on recall even with tuning."

**Alternative answer (data quality):**
"Missing values in TotalCharges. Rather than just dropping rows, I investigated and found they were all new customers with zero tenure who hadn't been charged yet. Importantly, they all had 0% churn. Dropping them would have introduced survivor bias, so I imputed with zero to preserve this behaviorally distinct cohort."

---

### Q: "Why did you choose Logistic Regression over Random Forest?"
**Answer:**
"Two reasons: performance and interpretability. Logistic Regression achieved 80% recall compared to Random Forest's 48% even after hyperparameter tuning. But equally important, I needed to explain the model to business stakeholders. With logistic regression, I can say 'month-to-month contracts increase churn risk by X amount'—you can't do that with a black-box ensemble. For a retention team that needs to trust and act on these predictions, interpretability matters as much as accuracy."

---

### Q: "How would you deploy this in production?"
**Answer:**
"I'd set it up as a weekly batch scoring job. The model would score all active customers, flag anyone moving into High or Critical risk tiers, and output a prioritized CSV that automatically emails to the retention team. I included SQL queries in the analysis showing how to implement the risk logic directly in the database, so it could run without Python if needed.

For monitoring, I'd track score distribution drift and tier churn rates weekly. If the Critical tier drops below 50% actual churn, the model needs retraining. I'd also add a feedback loop where the retention team logs outreach outcomes so we can measure campaign effectiveness and refine the scoring over time."

---

### Q: "What would you do differently with more time or data?"
**Answer:**
"Three things: First, add behavioral data like support ticket volume, usage metrics, and NPS scores—these would likely improve the model and reveal churn causes beyond just contract terms.

Second, I'd do true cohort analysis with time-series data. My tenure analysis is cross-sectional, which approximates lifecycle patterns but isn't a true survival curve. Following actual cohorts over time would validate the early-stage churn finding and help optimize intervention timing.

Third, I'd experiment with gradient boosting models like XGBoost. They might capture interaction effects better than logistic regression, though I'd need to use SHAP values to maintain interpretability for stakeholders."

---

### Q: "Tell me about your data cleaning process"
**Answer:**
"I started with data type validation and found TotalCharges was imported as object instead of numeric. I converted it with error handling, which revealed 11 missing values. Rather than impute with mean or drop them, I investigated—turns out all were customers with zero tenure who hadn't been charged yet. The key insight was they all showed 0% churn, so they're behaviorally different from the average. I imputed with zero to preserve this distinct new customer cohort, which would have been lost if I'd done automatic imputation."

---

### Q: "How did you validate your risk segmentation framework?"
**Answer:**
"Multiple ways. First, I verified churn rates increase monotonically across risk tiers: Low (5.4%) → Moderate (21.6%) → High (40.9%) → Critical (62.9%). That 12x spread from Low to Critical shows the tiers truly separate risk levels.

Second, I used SQL to replicate the scoring logic, ensuring it could run in a production database. Third, I compared the rule-based scores to the logistic regression predictions—they correlated strongly, confirming the hand-crafted rules captured the model's signal.

Finally, I spot-checked individual high-risk customers to ensure the scores made business sense—customers flagged as Critical consistently had month-to-month contracts, low tenure, and poor service engagement."

---

### Q: "What's the business value of your recommendation?"
**Answer:**
"I estimated that a contract conversion campaign targeting the 1,200 month-to-month customers in High or Critical risk tiers, with even 10% conversion to one-year contracts, would preserve $10-15K in monthly recurring revenue—that's $120-180K annually. This assumes converted customers drop from 42% to 11% churn rate.

For the early lifecycle check-ins, if we reduce first-year churn from 47% to 40%—a conservative 15% relative improvement—applied to the ~2,000 new customers annually, that's preserving 140 customers at roughly $60 average monthly value, or about $100K annually.

These are conservative estimates that don't account for secondary benefits like upsell opportunities or referral value from satisfied customers."

---

### Q: "How do you communicate technical findings to non-technical stakeholders?"
**Answer:**
"I built two outputs: a technical notebook with full methodology for the data science team, and a portfolio notebook focused on business impact for executives. In the executive version, I lead with revenue loss—$1.67 million—not model accuracy.

For visualizations, I used simple bar charts and risk tier colors (green/yellow/orange/red) that are intuitive. I translated every technical concept: 'recall' became 'catches 4 out of 5 churners,' 'AUC = 0.85' became 'strong ability to rank customers by risk.'

I always tie findings to actions: not just 'month-to-month contracts are risky' but 'target these 1,200 customers with contract conversion offers to preserve $120K+ annually.'"

---

### Q: "What's one insight from this project that surprised you?"
**Answer:**
"The value perception gap. I expected contract type and tenure to matter, but I didn't anticipate that customers paying $65+ per month with fewer than 2 services would churn at 58%—one of the highest rates in the dataset. This revealed an opportunity to turn retention into upsell: bundle additional services like TechSupport or OnlineSecurity at the same price point, increasing both perceived value and switching costs. It's a rare case where the retention strategy also drives revenue growth."

---

## 🎯 Technical Deep-Dive Questions

### Q: "Explain your preprocessing pipeline"
**Answer:**
"I used scikit-learn's ColumnTransformer to handle numerical and categorical features separately. Numerical features (tenure, MonthlyCharges, TotalCharges) went through StandardScaler for normalization. Categorical features (Contract, InternetService, PaymentMethod) used OneHotEncoder with drop='first' to avoid multicollinearity.

I wrapped this in a Pipeline with the logistic regression model so the entire workflow—preprocessing + training—happens in one fit() call. This prevents data leakage because the StandardScaler only fits on training data, then transforms test data, never seeing it during parameter learning."

---

### Q: "How did you handle class imbalance?"
**Answer:**
"I used class_weight='balanced' in logistic regression, which automatically adjusts the loss function to penalize misclassified minority class examples more heavily. Mathematically, it sets weights inversely proportional to class frequencies, so the model treats one churner as being worth 3x as much as one non-churner in the loss calculation.

I also experimented with threshold tuning (lowering from 0.5 to 0.35) and compared to SMOTE, but class weighting gave the best recall without overfitting. It's cleaner than resampling because you're not artificially creating data."

---

### Q: "Walk me through your feature selection process"
**Answer:**
"I started with chi-square tests for categorical features to identify statistical significance with churn. Contract, InternetService, and PaymentMethod showed the strongest signals (chi-square > 500). For numerical features, I checked correlation to avoid multicollinearity—tenure and TotalCharges were 0.83 correlated but I kept both because they represent different concepts: loyalty duration vs cumulative value.

I avoided kitchen-sink approaches and selected six features that balanced predictive power with interpretability. Later I tested adding service engagement features, which improved AUC by only 0.01, so I kept the simpler model for the final deployment."

---

## 🛠️ Tools & Technical Stack Questions

### Q: "Why did you choose these tools?"
**Answer:**
"Python because it's the industry standard for data science with excellent libraries. Pandas for data manipulation, Scikit-learn for modeling—both are production-ready and well-documented. Matplotlib and Seaborn for visualizations that can export to publication quality.

I used SQLite to demonstrate production deployment thinking—showing the logic can run in a database without Python. This matters because not all companies have data science infrastructure, but everyone has a database.

Jupyter notebooks for reproducibility and storytelling—stakeholders can see the entire analysis flow, not just results."

---

## 🧠 Behavior & Fit Questions

### Q: "What did you learn from this project?"
**Answer:**
"The importance of balancing statistical rigor with business pragmatism. I could have built a more complex neural network, but the business needed something they could understand and implement next week. The rule-based risk scoring framework is less sophisticated than a black-box model but infinitely more actionable.

I also learned that churn analysis is as much about operational implementation as modeling accuracy. The best model is useless if the retention team doesn't trust it or can't act on it."

---

### Q: "How do you prioritize when you have competing approaches?"
**Answer:**
"I use a decision matrix: business impact vs implementation effort. For this project, contract conversion campaigns scored high on both—clear ROI and easy to execute. Service bundle upsells scored medium on impact but higher on complexity because it requires product team coordination.

I present all options ranked by expected value, but flag quick wins separately. The contract campaigns could start immediately while service bundling gets planned for Q2."

---

### Q: "Why did you build an interactive dashboard for this project?"
**Answer:**
"I wanted to demonstrate deployment skills beyond static analysis. The Jupyter notebook is great for technical review, but stakeholders often want to explore the data themselves—test different scenarios, filter customer segments, or calculate ROI for their specific campaign parameters.

I built it with Streamlit because it's Python-native and deploys easily to the cloud. The dashboard has four sections: an executive overview with key metrics, a risk analyzer where you can filter customers by any combination of risk tier or characteristics, a churn predictor where you can input customer details and get instant risk scores, and an ROI calculator for modeling retention campaigns.

It's hosted on Streamlit Cloud, so anyone with the link can use it without installing anything. This also shows I understand the full data science workflow: analysis → insights → deployment → stakeholder enablement."

---

### Q: "Walk me through the technical implementation of your dashboard"
**Answer:**
"I used Streamlit for the framework and Plotly for interactive visualizations. I structured it as a multi-page app with sidebar navigation.

For performance, I cached the data loading function with `@st.cache_data` so the CSV only loads once, not on every interaction. The risk scoring logic is identical to what's in my notebook—I abstracted it into reusable functions so there's no code duplication.

The ROI calculator was interesting to build because I needed to make financial projections dynamic. Users can adjust churn reduction expectations and cost per customer, and it recalculates net benefit, ROI, and even generates a sensitivity analysis showing how ROI changes across different churn reduction scenarios.

I deployed it to Streamlit Cloud which handles the containerization automatically. The `requirements.txt` explicitly pins versions to ensure reproducibility."

---

## 📋 Questions to Ask the Interviewer

1. "How does your team currently identify at-risk customers? Is it rule-based, model-based, or reactive?"

2. "What's the typical timeline from analysis to implementation for retention campaigns here?"

3. "Do you have access to behavioral data like support tickets or usage metrics, or primarily transactional data like I worked with?"

4. "How do you balance interpretability vs accuracy when deploying models to business teams?"

5. "What tools does your data science team use for collaboration and model deployment?"

---

## ✅ Pre-Interview Checklist

- [ ] Review this document 24 hours before interview
- [ ] Know all key numbers by heart (no looking)
- [ ] Practice 2-minute walkthrough out loud (time yourself)
- [ ] Have notebook open and ready to share screen
- [ ] Prepare one question about their specific retention challenges
- [ ] Review GitHub commits to discuss your development process
- [ ] Test HTML export link works if you're sharing it

---

**Remember:** Confidence comes from preparation. You built this entire project—you know it better than anyone. Frame everything through business impact, stay concise, and let your enthusiasm for solving real problems come through.

Good luck! 🚀
