---
title: Telco Churn Analysis Dashboard
emoji: 📊
colorFrom: red
colorTo: orange
sdk: streamlit
sdk_version: 1.29.0
app_file: streamlit_app.py
pinned: false
---

# Telco Customer Churn Analysis Dashboard

An interactive dashboard I built to analyze why a telecom company was losing $1.67M annually to customer churn. The analysis covers 7,000+ customers and identifies specific risk factors and retention opportunities.

## What This Does

I wanted to go beyond just building a model. This dashboard lets you actually explore the data and test scenarios:

**Overview Dashboard** - Start here to see the big picture. The key finding is that month-to-month contracts have 15x higher churn than two-year contracts. There's also a critical window in the first 12 months where nearly half of new customers leave.

**Risk Analyzer** - Filter customers by contract type, tenure, or monthly charges and watch the metrics update in real time. You can export lists of high-risk customers for targeted retention campaigns.

**Churn Predictor** - Enter a customer's details and get an instant risk score. The system breaks down exactly which factors are driving the risk and suggests specific retention strategies.

**ROI Calculator** - Model the financial impact of different retention campaigns. Adjust the assumptions and see how ROI changes across different scenarios.

## Key Findings

The analysis revealed some surprising patterns:
- 26.5% of customers churn annually (much higher than expected)
- Month-to-month contracts are the biggest risk factor by far
- Customers paying high prices for few services churn at 58%
- The first year is make-or-break for retention

I built a predictive model that catches 4 out of 5 customers who will actually churn (80% recall), then created a practical risk scoring system that's easy for business teams to understand and act on.

## How It Works

The dashboard uses a logistic regression model trained on historical customer data. I prioritized recall over precision because missing a churner costs way more than a false alarm. The risk scoring system assigns 0-11 points based on six behavioral factors like contract type, tenure, service engagement, and payment method.

All the code is available on GitHub if you want to dig into the methodology. The analysis includes full exploratory data work, multiple modeling approaches compared, and SQL validation queries for production deployment.

## Technical Details

Built with Python, Streamlit, and Plotly. The dataset has 7,043 customer records with 21 features including demographics, services, contract details, and billing information. I added feature engineering for service counts and value perception metrics that turned out to be strong predictors.

The whole thing runs from a single CSV file and recalculates everything dynamically as you interact with the filters and inputs. I used caching to keep it responsive even with thousands of records.

## Why I Built This

I wanted to demonstrate the full workflow of a data science project: from messy data to business-ready tools. Too many portfolio projects stop at "here's my model accuracy" without showing how stakeholders would actually use the insights. This dashboard is something a retention team could realistically deploy and use to prioritize their outreach.

The project also shows I can translate technical findings into plain language and actionable recommendations. Every insight ties to a specific dollar amount or retention strategy.

## Dataset

Based on the Telco Customer Churn dataset from Kaggle, with additional risk scoring framework I developed.

## More Information

Check out the [GitHub repository](https://github.com/YOUR-USERNAME/telco-churn-analysis) for the full analysis notebooks, documentation, and code. I've also included interview prep materials and a detailed project summary if you want to understand the methodology.
