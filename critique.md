Notebook Critique: Telco Churn Analysis

Overall Assessment
This is a strong first portfolio project — genuinely strong, not "strong for a beginner." You went considerably further than the brief called for, and the majority of that additional work was justified and well-executed. The core analytical thinking is sound, the business framing is consistent throughout, and the executive report at the end reads like something a real analyst would hand to a manager. You should be proud of this as a portfolio piece.
That said, there are meaningful things to fix before you show this to anyone, and some patterns worth correcting now before they become habits. The critique below is structured from most to least important.

What You Did Well (Genuinely)
Before the critique, it's worth being specific about what actually landed.
The executive report (Cell 161) is the best section of the notebook. The three-finding structure, the plain-English implications under each finding, and the limitations section with specific data gaps — that's analyst-level writing. Most junior candidates either don't write this section at all or write a bullet list of chart summaries. You wrote an actual analytical memo.
The risk segmentation framework is a legitimate differentiator. A rule-based scoring system with transparent weights, a clear rationale for each factor, and a validation step showing churn rates actually increase with risk tier — this is the kind of thing that gets discussed in interviews. The fact that you validated it rather than just presenting it shows good instincts.
The churner profile section (Cell 96) is exactly right. Specific numbers, comparative framing (vs. retained customers), and a plain-English interpretation that ends with a business insight rather than a data observation. The "it's not just about price — it's about value perception" line is strong.
Data cleaning documentation is good. You found the TotalCharges issue, explained the business decision you made, and noted the implication (the 11 missing rows are all zero-churn new customers — dropping them would introduce bias). That's the right way to document a cleaning decision.

Issues to Fix
1. The pip install output should not be in the final notebook
Severity: High — fix before showing anyone
Cell 3 displays the full pip install output including your local file path:
Copy/Users/gagepiercegaubert/Desktop/career_projects/da_project_1/
This is a personal detail in a public portfolio artifact, and it signals the notebook wasn't cleaned before submission. In a professional setting, sharing internal paths is a minor information security issue. In a portfolio context, it signals carelessness.
Fix: Either move your imports to a clean cell with no output, or use a try/except import block that installs silently if needed. Run Kernel → Restart & Run All on your final version and clear this output before publishing.

2. The rolling churn rate calculation has a methodological problem
Severity: High — affects the validity of a key finding
Cell 103 shows a "survival view" with churn rates like:
Copytenure=1: 61.99% churn rate
tenure=2: 51.68% churn rate
These numbers are almost certainly not what you think they are. What this calculation is actually measuring is: of all customers who happen to have tenure=1 in this cross-sectional snapshot, what proportion churned? That is not the same as a survival curve.
A genuine survival curve would follow a cohort of customers who started at month 0 and track what percentage were still active at each subsequent month. Your dataset doesn't have that longitudinal structure — it's a snapshot. Customers with tenure=1 in this dataset are not the same people who were at tenure=1 six years ago.
The practical problem: A 62% "churn rate" at month 1 will raise an immediate red flag with any experienced analyst who reviews this notebook. It will look like you don't understand the difference between cross-sectional and longitudinal data.
Fix options (pick one):

Remove the rolling churn rate chart entirely. The tenure band chart (left panel of Cell 105) is valid and makes the same point more defensibly.
Keep it but relabel it explicitly: "Churn rate among customers whose current tenure is X months — note this is cross-sectional, not a cohort survival curve."
Add a markdown cell acknowledging the limitation: "A true survival analysis would require cohort data tracking individual customers over time. This cross-sectional view approximates the pattern but overstates early-tenure churn rates due to selection effects."

The third option is actually the strongest from an interview perspective — it shows you understand the limitation rather than being unaware of it.

3. The Random Forest comparison is incomplete and slightly misleading
Severity: Medium — affects model section credibility
Cell 64 shows:
CopyModel              Recall   AUC
Logistic Regression  0.80   0.84
Random Forest        0.48   0.80
And Cell 65 concludes: "Winner: Logistic Regression."
The problem is that you applied class weighting to Logistic Regression but apparently not to Random Forest, or you tuned the LR threshold but didn't apply the same optimization to RF. This is an apples-to-oranges comparison. Random Forest with class_weight='balanced' would almost certainly perform differently than what's shown here.
This matters because a reviewer might ask: "Did you tune the Random Forest the same way?" If the answer is no, the comparison doesn't support the conclusion.
Fix: Either apply the same class weighting to both models before comparing, or add a brief note: "Random Forest was evaluated at default threshold for comparison. Applying class_weight='balanced' to RF is a reasonable next step — the comparison here demonstrates LR's interpretability advantage rather than a definitively superior AUC."
The interpretability argument you make is valid and strong. You don't need a flawed performance comparison to support it.

4. The markdown writing oscillates between two registers that don't belong in the same document
Severity: Medium — affects professional presentation
Some of your analysis is written in clean, direct business language:

"It's not just about price — it's about value perception. Higher monthly charges with fewer services means customers feel like they're overpaying."

Other sections are written in a noticeably different register that reads like academic hedging:

"Observable differences in churn rates between automated payment methods (electronic check, credit card) and manual methods (mailed check, bank transfer) may reflect customer engagement levels or demographic indicators. Modern payment adoption could serve as a proxy for digital literacy or customer lifecycle stage, potentially identifying higher-risk retention segments."

The second style has three problems. First, it says "observable differences" and then doesn't state what those differences actually are — a reader has to go find the chart. Second, it stacks hedging language ("may reflect," "could serve as a proxy," "potentially identifying") in a way that reads as uncertain. Third, it introduces terms like "digital literacy" and "demographic indicators" without any data to support them. You're speculating in formal language, which is worse than speculating plainly.
Compare those two sections. The first one is confident, specific, and plainly written. The second one could be deleted without losing any information.
A rough test: read each markdown cell and ask "did I state a number?" If you wrote several sentences of interpretation without citing a specific finding, you're probably hedging. Either state the number or delete the sentences.
The cells most affected: 31, 32, 34, 126. The cells that get this right: 96, 106, 113, 161.

5. The service count churn rate at 0 services needs explanation
Severity: Medium — a genuine analytical gap
Cell 93 shows:
CopyService_Count    Churn_Rate
0                0.214
1                0.458
Customers with zero services churn at 21% — lower than customers with 1 service (46%). That's counterintuitive and probably not what most readers would expect. You note in Cell 83 that "customers with 0 services show highest revenue per service and highest churn" — but the table directly above that shows 0-service customers at 21% churn, which contradicts the statement.
What's likely happening: the 0-service group probably includes customers with no internet service at all, who have simpler, cheaper plans and fewer reasons to leave. The 1-service group may be customers who have internet but haven't bundled anything — paying more but getting less.
Fix: Add a breakdown of what "0 services" actually looks like:
pythonCopy# Who are the 0-service customers?
print(df[df['Service_Count'] == 0]['InternetService'].value_counts())
print(df[df['Service_Count'] == 0]['Contract'].value_counts())
Then explain what you find. If the 0-service group is mostly no-internet customers on stable plans, say that. The current presentation leaves an unexplained anomaly in your data that a reviewer will notice.

6. The LTV calculation and the "3.9M" figure need a caveat
Severity: Low-Medium — affects the revenue impact section
Cell 113 states:

"With 1,869 customers churning, the total lifetime value at risk is approximately $3.9M."

This is calculated as churned customers × average LTV, where average LTV is average monthly charge × average tenure. The problem is that these customers have already churned — their lifetime value was already realized. What's actually at risk is the future revenue they would have generated if they had stayed, which requires an assumption about how long they would have continued subscribing.
The $3.9M figure is defensible if you frame it clearly as: "The LTV gap between churned and retained customers, applied to the churned population, suggests $3.9M in potential value that was not fully realized." But as written, it implies $3.9M in recoverable future revenue, which overstates the case.
Fix: Add one sentence: "Note: this figure represents the LTV differential between churned and retained customers applied to the churned cohort — it is not a projection of recoverable future revenue, but an approximation of unrealized customer value."
This is a minor thing but it's the kind of detail that signals financial literacy.

7. Missing value flag column left in categorical list
Severity: Low — minor but noticeable
Cell 27 and 28 list missing_TotalCharges as a categorical column, and Cell 42 recommends dropping it ("Safe to Drop"). Good call. But it's worth confirming you actually dropped it from your modeling pipeline and didn't just note it as droppable. If it appears in any model feature lists, it would be a data leakage flag (the missingness is directly related to tenure=0, which is already in the model).

Structural Observations (Not Errors, But Worth Knowing)
The notebook is long. At 160+ cells, this is a research document more than a portfolio artifact. That's fine for a GitHub repo where someone is reading deeply, but if you're showing this in an interview or linking it on your resume, consider creating a second notebook called executive_summary.ipynb that contains only: the business context, the 5 key charts, the executive report, and the risk tier output. Reviewers who spend 10 minutes with your work should hit your best material in the first half.
The predictive modeling section is well done but slightly out of place in a "business analyst" framing. The logistic regression, ROC curve, and model comparison work is good — it shows Python competence and methodological awareness. But the executive report at the end wisely positions the risk scoring framework as the deliverable, not the ML model. That's the right call for a business analyst role. If you're applying to data scientist positions, lean into the modeling section. If you're applying to BA/analyst roles, the rule-based scoring framework with validated tiers is a stronger lead.
The SQL section is underutilized. Query 3 (window function) is the best of the three and should be first. Queries 1 and 2 reproduce things already shown in pandas — they demonstrate SQL syntax but not SQL thinking. A stronger SQL section would show something that's genuinely easier to do in SQL than pandas, or would frame the queries as production artifacts ("this is the query that would run in your data warehouse every Monday to update the risk scores"). The takeaway note in Cell 150 is good — it just needs the queries to match its ambition.

Priority Fix List
Copy🔴 BEFORE PUBLISHING
   1. Remove pip install output (Cell 3) — exposes file path, signals carelessness
   2. Add caveat to rolling churn rate chart — or remove it

🟡 BEFORE INTERVIEWS
   3. Fix Random Forest comparison — apply same tuning or caveat the comparison
   4. Audit hedging language in Cells 31, 32, 34, 126 — write like Cell 96 instead
   5. Explain the 0-service churn rate anomaly — it's a genuine analytical gap

🟢 NICE TO HAVE
   6. Add one sentence LTV caveat in Cell 113
   7. Confirm missing_TotalCharges was dropped from all models
   8. Create a shorter executive_summary.ipynb for quick sharing

The Summary Verdict
The analytical judgment here is good. You correctly identified the most important findings, you validated your segmentation framework, you wrote a business memo that a non-technical reader could act on, and you pushed further than the brief required in ways that mostly paid off.
The issues are mostly about precision — one methodological problem with the survival curve, one inconsistency in the writing register, one underexamined anomaly in the service count data. None of these suggest a gap in understanding. They suggest a notebook that needed one more careful read-through before publication.
Fix the items in the red category, clean up the two or three hedging-heavy markdown cells, and this is a notebook you can show with confidence. The executive report alone would get you past most junior BA screening conversations.
