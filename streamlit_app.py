"""
Telco Customer Churn Analysis Dashboard
Interactive Streamlit application for customer churn risk analysis and prediction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Telco Churn Analysis",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Business Blue Theme
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-blue: #1f4788;
        --accent-blue: #4A90E2;
        --dark-blue: #0D47A1;
        --light-blue: #E3F2FD;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid var(--primary-blue);
    }
    
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(31, 71, 136, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--primary-blue);
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--primary-blue);
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: var(--dark-blue);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: var(--light-blue);
    }
    
    /* Links */
    a {
        color: var(--accent-blue);
    }
    
    a:hover {
        color: var(--dark-blue);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and prepare the telco churn dataset"""
    df = pd.read_csv('data/telco_churn.csv')
    
    # Data cleaning
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    df['Churn_Flag'] = (df['Churn'] == 'Yes').astype(int)
    
    # Feature engineering
    service_features = ['OnlineSecurity', 'TechSupport', 'OnlineBackup',
                       'DeviceProtection', 'StreamingTV', 'StreamingMovies']
    df['Service_Count'] = df[service_features].apply(lambda row: (row == 'Yes').sum(), axis=1)
    
    return df

# Risk scoring function
def calculate_risk_score(row):
    """Calculate churn risk score (0-11 points)"""
    score = 0
    
    # Contract type (3 points)
    if row['Contract'] == 'Month-to-month':
        score += 3
    
    # Service engagement (2 points)
    if row['TechSupport'] == 'No' and row['OnlineSecurity'] == 'No':
        score += 2
    
    # Tenure (2 points)
    if row['tenure'] <= 12:
        score += 2
    
    # Value perception (2 points)
    if row['MonthlyCharges'] > 65 and row['Service_Count'] < 2:
        score += 2
    
    # Payment method (1 point)
    if row['PaymentMethod'] == 'Electronic check':
        score += 1
    
    # Paperless billing (1 point)
    if row['PaperlessBilling'] == 'Yes':
        score += 1
    
    return score

def get_risk_tier(score):
    """Convert risk score to tier"""
    if score <= 2:
        return 'Low Risk'
    elif score <= 5:
        return 'Moderate Risk'
    elif score <= 7:
        return 'High Risk'
    else:
        return 'Critical Risk'

# Load data
df = load_data()

# Calculate risk scores if not already done
if 'Risk_Score' not in df.columns:
    df['Risk_Score'] = df.apply(calculate_risk_score, axis=1)
    df['Risk_Tier'] = df['Risk_Score'].apply(get_risk_tier)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Risk Analyzer", "Churn Predictor", "Business Impact"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About This Dashboard
Interactive analysis of telecom customer churn identifying **$1.67M annual revenue exposure**.

**Key Insights:**
- 26.5% baseline churn rate
- Month-to-month contracts: 15x higher risk
- 2,598 high-risk customers identified

[View on GitHub](https://github.com/YOUR-USERNAME/telco-churn-analysis)
""")

# =======================
# PAGE 1: OVERVIEW
# =======================
if page == "Overview":
    st.title("Telco Customer Churn Analysis")
    st.markdown("### Executive Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = len(df)
    churned_customers = df['Churn_Flag'].sum()
    churn_rate = (churned_customers / total_customers * 100)
    monthly_revenue_loss = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()
    annual_revenue_loss = monthly_revenue_loss * 12
    
    with col1:
        st.metric(
            "Total Customers",
            f"{total_customers:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Churn Rate",
            f"{churn_rate:.1f}%",
            delta=f"-{churned_customers} customers",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Monthly Revenue Loss",
            f"${monthly_revenue_loss:,.0f}",
            delta=None
        )
    
    with col4:
        st.metric(
            "Annual Revenue Exposure",
            f"${annual_revenue_loss:,.0f}",
            delta=None
        )
    
    st.markdown("---")
    
    # Two-column layout for visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Churn Rate by Contract Type")
        
        contract_churn = df.groupby('Contract').agg({
            'Churn_Flag': ['sum', 'count', 'mean']
        }).round(4)
        contract_churn.columns = ['Churned', 'Total', 'Churn_Rate']
        contract_churn['Churn_Rate_%'] = (contract_churn['Churn_Rate'] * 100).round(1)
        contract_churn = contract_churn.reset_index()
        
        fig = px.bar(
            contract_churn,
            x='Contract',
            y='Churn_Rate_%',
            text='Churn_Rate_%',
            color='Churn_Rate_%',
            color_continuous_scale='Blues',
            labels={'Churn_Rate_%': 'Churn Rate (%)'}
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("Month-to-month contracts show **15x higher churn** than two-year contracts")
    
    with col2:
        st.markdown("#### Risk Tier Distribution")
        
        risk_dist = df['Risk_Tier'].value_counts().reset_index()
        risk_dist.columns = ['Risk_Tier', 'Count']
        risk_order = ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']
        risk_dist['Risk_Tier'] = pd.Categorical(risk_dist['Risk_Tier'], categories=risk_order, ordered=True)
        risk_dist = risk_dist.sort_values('Risk_Tier')
        
        colors = {'Low Risk': '#91bfdb', 'Moderate Risk': '#4A90E2', 
                 'High Risk': '#1f4788', 'Critical Risk': '#0D47A1'}
        
        fig = px.pie(
            risk_dist,
            values='Count',
            names='Risk_Tier',
            color='Risk_Tier',
            color_discrete_map=colors,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        high_risk_count = df[df['Risk_Tier'].isin(['High Risk', 'Critical Risk'])].shape[0]
        st.warning(f"**{high_risk_count:,} customers** in High/Critical risk tiers")
    
    st.markdown("---")
    
    # Tenure Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Churn Rate by Tenure")
        
        df['Tenure_Band'] = pd.cut(
            df['tenure'],
            bins=[0, 3, 12, 24, 48, 72],
            labels=['0-3 mo', '4-12 mo', '13-24 mo', '25-48 mo', '49-72 mo']
        )
        
        tenure_churn = df.groupby('Tenure_Band', observed=True)['Churn_Flag'].agg(['sum', 'count', 'mean'])
        tenure_churn['Churn_Rate_%'] = (tenure_churn['mean'] * 100).round(1)
        tenure_churn = tenure_churn.reset_index()
        
        fig = px.bar(
            tenure_churn,
            x='Tenure_Band',
            y='Churn_Rate_%',
            text='Churn_Rate_%',
            color='Churn_Rate_%',
            color_continuous_scale='Blues'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Monthly Charges Distribution")
        
        fig = go.Figure()
        
        for churn_status in ['No', 'Yes']:
            data = df[df['Churn'] == churn_status]['MonthlyCharges']
            fig.add_trace(go.Histogram(
                x=data,
                name=f"Churn: {churn_status}",
                opacity=0.6,
                nbinsx=30
            ))
        
        fig.update_layout(
            barmode='overlay',
            height=400,
            xaxis_title="Monthly Charges ($)",
            yaxis_title="Customer Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Key Findings
    st.markdown("---")
    st.markdown("### Key Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1. Contract Type is Primary Driver**
        - Month-to-month: 42.7% churn
        - Two-year: 2.8% churn
        - 15x difference in risk
        """)
    
    with col2:
        st.markdown("""
        **2. First 12 Months Critical**
        - 0-12 months: 47.4% churn
        - 13+ months: 17.1% churn
        - Early intervention essential
        """)
    
    with col3:
        st.markdown("""
        **3. Value Perception Gap**
        - High cost + low services: 57.8% churn
        - Bundle opportunity
        - Retention + upsell potential
        """)

# =======================
# PAGE 2: RISK ANALYZER
# =======================
elif page == "Risk Analyzer":
    st.title("Customer Risk Analyzer")
    st.markdown("### Filter and analyze customers by risk profile")
    
    # Filters in sidebar
    st.sidebar.markdown("### Filters")
    
    risk_tiers = st.sidebar.multiselect(
        "Risk Tier",
        options=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
        default=['High Risk', 'Critical Risk']
    )
    
    contracts = st.sidebar.multiselect(
        "Contract Type",
        options=df['Contract'].unique(),
        default=df['Contract'].unique()
    )
    
    tenure_range = st.sidebar.slider(
        "Tenure (months)",
        min_value=int(df['tenure'].min()),
        max_value=int(df['tenure'].max()),
        value=(0, 72)
    )
    
    charges_range = st.sidebar.slider(
        "Monthly Charges ($)",
        min_value=float(df['MonthlyCharges'].min()),
        max_value=float(df['MonthlyCharges'].max()),
        value=(float(df['MonthlyCharges'].min()), float(df['MonthlyCharges'].max()))
    )
    
    # Apply filters
    filtered_df = df[
        (df['Risk_Tier'].isin(risk_tiers)) &
        (df['Contract'].isin(contracts)) &
        (df['tenure'].between(tenure_range[0], tenure_range[1])) &
        (df['MonthlyCharges'].between(charges_range[0], charges_range[1]))
    ]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filtered Customers", f"{len(filtered_df):,}")
    
    with col2:
        avg_risk = filtered_df['Risk_Score'].mean()
        st.metric("Avg Risk Score", f"{avg_risk:.1f}")
    
    with col3:
        filtered_churn_rate = (filtered_df['Churn_Flag'].mean() * 100)
        st.metric("Churn Rate", f"{filtered_churn_rate:.1f}%")
    
    with col4:
        revenue_at_risk = filtered_df[filtered_df['Churn'] == 'Yes']['MonthlyCharges'].sum()
        st.metric("Monthly Revenue at Risk", f"${revenue_at_risk:,.0f}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Risk Score Distribution")
        fig = px.histogram(
            filtered_df,
            x='Risk_Score',
            nbins=12,
            color='Risk_Tier',
            color_discrete_map={
                'Low Risk': '#91bfdb',
                'Moderate Risk': '#4A90E2',
                'High Risk': '#1f4788',
                'Critical Risk': '#0D47A1'
            }
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Actual Churn Rate by Risk Tier")
        
        validation = filtered_df.groupby('Risk_Tier', observed=True)['Churn_Flag'].agg(['count', 'mean'])
        validation['Churn_Rate_%'] = (validation['mean'] * 100).round(1)
        validation = validation.reset_index()
        
        fig = px.bar(
            validation,
            x='Risk_Tier',
            y='Churn_Rate_%',
            text='Churn_Rate_%',
            color='Churn_Rate_%',
            color_continuous_scale='Blues'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer table
    st.markdown("---")
    st.markdown("#### Filtered Customer List")
    
    # Prepare display dataframe
    display_cols = ['customerID', 'Risk_Tier', 'Risk_Score', 'Contract', 'tenure', 
                   'MonthlyCharges', 'Service_Count', 'Churn']
    
    display_df = filtered_df[display_cols].sort_values('Risk_Score', ascending=False)
    
    st.dataframe(
        display_df.head(100),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Customers (CSV)",
        data=csv,
        file_name="filtered_high_risk_customers.csv",
        mime="text/csv"
    )

# =======================
# PAGE 3: CHURN PREDICTOR
# =======================
elif page == "Churn Predictor":
    st.title("Customer Churn Predictor")
    st.markdown("### Enter customer details to predict churn risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Contract & Account Details")
        
        contract = st.selectbox("Contract Type", df['Contract'].unique())
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=70.0)
        payment_method = st.selectbox("Payment Method", df['PaymentMethod'].unique())
        paperless_billing = st.selectbox("Paperless Billing", ['Yes', 'No'])
        
    with col2:
        st.markdown("#### Services")
        
        internet_service = st.selectbox("Internet Service", df['InternetService'].unique())
        online_security = st.selectbox("Online Security", ['Yes', 'No', 'No internet service'])
        tech_support = st.selectbox("Tech Support", ['Yes', 'No', 'No internet service'])
        online_backup = st.selectbox("Online Backup", ['Yes', 'No', 'No internet service'])
        device_protection = st.selectbox("Device Protection", ['Yes', 'No', 'No internet service'])
        streaming_tv = st.selectbox("Streaming TV", ['Yes', 'No', 'No internet service'])
        streaming_movies = st.selectbox("Streaming Movies", ['Yes', 'No', 'No internet service'])
    
    # Calculate service count
    service_features = [online_security, tech_support, online_backup, 
                       device_protection, streaming_tv, streaming_movies]
    service_count = sum(1 for s in service_features if s == 'Yes')
    
    # Create customer profile
    customer = {
        'Contract': contract,
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'PaymentMethod': payment_method,
        'PaperlessBilling': paperless_billing,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'TechSupport': tech_support,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Service_Count': service_count
    }
    
    # Calculate risk score
    risk_score = calculate_risk_score(pd.Series(customer))
    risk_tier = get_risk_tier(risk_score)
    
    # Predict button
    if st.button("Predict Churn Risk", type="primary"):
        st.markdown("---")
        st.markdown("### Prediction Results")
        
        # Display risk score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Risk Score", f"{risk_score}/11")
        
        with col2:
            color_indicator = {'Low Risk': '[LOW]', 'Moderate Risk': '[MODERATE]', 
                    'High Risk': '[HIGH]', 'Critical Risk': '[CRITICAL]'}
            st.metric("Risk Tier", f"{color_indicator[risk_tier]} {risk_tier}")
        
        with col3:
            # Estimated churn probability based on historical data
            tier_churn_rates = {
                'Low Risk': 5.4,
                'Moderate Risk': 21.6,
                'High Risk': 40.9,
                'Critical Risk': 62.9
            }
            churn_prob = tier_churn_rates[risk_tier]
            st.metric("Estimated Churn Probability", f"{churn_prob}%")
        
        # Risk factors breakdown
        st.markdown("#### Risk Factors Breakdown")
        
        factors = []
        
        if contract == 'Month-to-month':
            factors.append("[-] Month-to-month contract (+3 points)")
        else:
            factors.append("[+] Long-term contract (0 points)")
        
        if tech_support == 'No' and online_security == 'No':
            factors.append("[-] No protective services (+2 points)")
        else:
            factors.append("[+] Has protective services (0 points)")
        
        if tenure <= 12:
            factors.append("[-] Early tenure (<= 12 months) (+2 points)")
        else:
            factors.append("[+] Established customer (0 points)")
        
        if monthly_charges > 65 and service_count < 2:
            factors.append("[-] High cost, low value perception (+2 points)")
        else:
            factors.append("[+] Good value perception (0 points)")
        
        if payment_method == 'Electronic check':
            factors.append("[-] Electronic check payment (+1 point)")
        else:
            factors.append("[+] Automatic payment method (0 points)")
        
        if paperless_billing == 'Yes':
            factors.append("[!] Paperless billing (+1 point)")
        else:
            factors.append("[+] Paper billing (0 points)")
        
        for factor in factors:
            st.markdown(f"- {factor}")
        
        # Recommendations
        st.markdown("---")
        st.markdown("#### Retention Recommendations")
        
        if risk_tier in ['High Risk', 'Critical Risk']:
            st.error("**IMMEDIATE ACTION REQUIRED**")
            recommendations = []
            
            if contract == 'Month-to-month':
                recommendations.append("**Priority**: Offer contract upgrade with incentive (e.g., 15% discount on 1-year contract)")
            
            if tenure <= 12:
                recommendations.append("**Outreach**: Schedule customer success check-in within 7 days")
            
            if service_count < 2:
                recommendations.append("**Bundle Offer**: Present service bundle package at discounted rate")
            
            if monthly_charges > 65 and service_count < 2:
                recommendations.append("**Value Adjustment**: Review pricing vs services, consider loyalty discount")
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        
        elif risk_tier == 'Moderate Risk':
            st.warning("**MONITORING RECOMMENDED**")
            st.markdown("""
            - Include in quarterly engagement campaign
            - Send loyalty rewards/upsell offers
            - Monitor usage patterns for changes
            - Track payment behavior closely
            """)
        
        else:
            st.success("**LOW RISK - MAINTAIN SATISFACTION**")
            st.markdown("""
            - Continue standard service
            - Consider for upsell opportunities
            - Request feedback/referrals
            - Include in positive case studies
            """)

# =======================
# PAGE 4: BUSINESS IMPACT
# =======================
elif page == "Business Impact":
    st.title("Business Impact Calculator")
    st.markdown("### Quantify retention campaign ROI")
    
    # Campaign parameters
    st.markdown("#### Campaign Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_tier = st.multiselect(
            "Target Risk Tiers",
            ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
            default=['High Risk', 'Critical Risk']
        )
    
    with col2:
        expected_reduction = st.slider(
            "Expected Churn Reduction (%)",
            min_value=5,
            max_value=50,
            value=20,
            step=5
        )
    
    with col3:
        cost_per_customer = st.number_input(
            "Outreach Cost per Customer ($)",
            min_value=0,
            max_value=500,
            value=50
        )
    
    # Validate that risk tiers are selected
    if not target_tier:
        st.info("Please select at least one Risk Tier to view campaign impact projections.")
        st.stop()
    
    # Calculate impact
    target_customers = df[df['Risk_Tier'].isin(target_tier)]
    total_targets = len(target_customers)
    
    # Validate that there are customers in selected tiers
    if total_targets == 0:
        st.warning("No customers found in the selected Risk Tier(s). Please adjust your selection.")
        st.stop()
    
    # Current metrics
    current_monthly_loss = target_customers[target_customers['Churn'] == 'Yes']['MonthlyCharges'].sum()
    current_annual_loss = current_monthly_loss * 12
    current_churn_rate = (target_customers['Churn_Flag'].mean() * 100)
    
    # Projected metrics
    reduced_churn_rate = current_churn_rate * (1 - expected_reduction/100)
    saved_customers = max(0, int(total_targets * (current_churn_rate - reduced_churn_rate) / 100))
    avg_monthly_charge = target_customers['MonthlyCharges'].mean()
    monthly_savings = saved_customers * avg_monthly_charge
    annual_savings = monthly_savings * 12
    
    # Campaign cost
    campaign_cost = total_targets * cost_per_customer
    
    # ROI
    net_annual_benefit = annual_savings - campaign_cost
    roi = ((annual_savings - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0
    
    st.markdown("---")
    
    # Results
    st.markdown("### Campaign Impact Projection")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Target Customers",
            f"{total_targets:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Current Churn Rate",
            f"{current_churn_rate:.1f}%",
            delta=f"→ {reduced_churn_rate:.1f}%"
        )
    
    with col3:
        st.metric(
            "Customers Saved",
            f"{saved_customers:,}",
            delta=f"{expected_reduction}% reduction"
        )
    
    with col4:
        st.metric(
            "Campaign ROI",
            f"{roi:.0f}%",
            delta=None
        )
    
    # Financial breakdown
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue Impact")
        
        revenue_data = pd.DataFrame({
            'Metric': ['Current Annual Loss', 'Projected Savings', 'Net Benefit'],
            'Amount': [current_annual_loss, annual_savings, net_annual_benefit]
        })
        
        fig = go.Figure()
        
        colors = ['#1f4788', '#91bfdb', '#0D47A1']
        
        for i, row in revenue_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['Metric']],
                y=[row['Amount']],
                name=row['Metric'],
                marker_color=colors[i],
                text=f"${row['Amount']:,.0f}",
                textposition='outside'
            ))
        
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis_title="Amount ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Cost-Benefit Analysis")
        
        # Waterfall chart
        fig = go.Figure(go.Waterfall(
            x=['Revenue Savings', 'Campaign Cost', 'Net Benefit'],
            y=[annual_savings, -campaign_cost, net_annual_benefit],
            text=[f"${annual_savings:,.0f}", f"-${campaign_cost:,.0f}", f"${net_annual_benefit:,.0f}"],
            textposition='outside',
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#0D47A1"}},
            decreasing={"marker": {"color": "#1f4788"}},
            totals={"marker": {"color": "#4A90E2"}}
        ))
        
        fig.update_layout(height=400, yaxis_title="Amount ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary
    st.markdown("---")
    st.markdown("### Campaign Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Investment")
        st.markdown(f"""
        - **Target Customers:** {total_targets:,}
        - **Cost per Customer:** ${cost_per_customer}
        - **Total Campaign Cost:** ${campaign_cost:,.0f}
        """)
    
    with col2:
        st.markdown("#### Returns")
        st.markdown(f"""
        - **Customers Retained:** {saved_customers:,}
        - **Annual Revenue Saved:** ${annual_savings:,.0f}
        - **Net Annual Benefit:** ${net_annual_benefit:,.0f}
        - **ROI:** {roi:.0f}%
        """)
    
    # Recommendation
    if roi > 200:
        st.success(f"""
        **HIGHLY RECOMMENDED**: This campaign shows excellent ROI ({roi:.0f}%).
        Expected to save {saved_customers:,} customers and generate ${net_annual_benefit:,.0f} net benefit.
        """)
    elif roi > 100:
        st.info(f"""
        **RECOMMENDED**: This campaign shows good ROI ({roi:.0f}%).
        Consider refining targeting or reducing cost per customer for even better returns.
        """)
    elif roi > 0:
        st.warning(f"""
        **MARGINAL**: ROI is positive but modest ({roi:.0f}%).
        Consider adjusting parameters or targeting higher-value customer segments.
        """)
    else:
        st.error(f"""
        **NOT RECOMMENDED**: Campaign cost exceeds projected savings.
        Reduce cost per customer or improve expected churn reduction rate.
        """)
    
    # Sensitivity analysis
    st.markdown("---")
    st.markdown("### Sensitivity Analysis")
    
    st.markdown("#### Impact of Different Churn Reduction Rates")
    
    reduction_rates = range(5, 51, 5)
    rois = []
    savings = []
    
    for rate in reduction_rates:
        reduced_rate = current_churn_rate * (1 - rate/100)
        saved = int(total_targets * (current_churn_rate - reduced_rate) / 100)
        monthly_save = saved * avg_monthly_charge
        annual_save = monthly_save * 12
        campaign_roi = ((annual_save - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0
        
        rois.append(campaign_roi)
        savings.append(annual_save)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=list(reduction_rates), y=rois, name="ROI (%)", 
                  line=dict(color='#1f4788', width=3)),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=list(reduction_rates), y=savings, name="Annual Savings ($)", 
                  line=dict(color='#4A90E2', width=3)),
        secondary_y=True
    )
    
    fig.update_xaxes(title_text="Churn Reduction Rate (%)")
    fig.update_yaxes(title_text="ROI (%)", secondary_y=False)
    fig.update_yaxes(title_text="Annual Savings ($)", secondary_y=True)
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Telco Customer Churn Analysis Dashboard</p>
    <p>Built with Streamlit • Data Science Portfolio Project</p>
    <p><a href='https://github.com/YOUR-USERNAME/telco-churn-analysis' target='_blank'>View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
