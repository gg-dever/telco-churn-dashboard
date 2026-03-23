# Streamlit Cloud Deployment Guide

## 🚀 Deploy Your Dashboard to Streamlit Cloud

### Prerequisites
- [x] GitHub repository created and pushed
- [x] `streamlit_app.py` created
- [x] `requirements.txt` created
- [x] `.streamlit/config.toml` created

### Step 1: Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up" and authenticate with GitHub
3. Grant Streamlit Cloud access to your repositories

### Step 2: Deploy Your App

1. Click "New app" from your Streamlit Cloud dashboard
2. Select your repository: `YOUR-USERNAME/telco-churn-analysis`
3. Set the following:
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose a custom subdomain (e.g., `telco-churn-analysis`)
4. Click "Deploy!"

### Step 3: Wait for Deployment

- Streamlit Cloud will:
  - Clone your repository
  - Install dependencies from `requirements.txt`
  - Run your app
- Usually takes 2-5 minutes
- Watch the deployment logs for any errors

### Step 4: Test Your Live App

1. Visit your app at: `https://YOUR-SUBDOMAIN.streamlit.app`
2. Test all four pages:
   - 🏠 Overview
   - 🎯 Risk Analyzer
   - 🔮 Churn Predictor
   - 💰 Business Impact
3. Verify all visualizations load correctly
4. Test interactive features (filters, sliders, inputs)

### Step 5: Update README

Replace the placeholder in `README.md`:
```markdown
**[Launch Live Demo →](https://YOUR-APP-NAME.streamlit.app)** *(Coming Soon)*
```

With your actual URL:
```markdown
**[Launch Live Demo →](https://telco-churn-analysis.streamlit.app)**
```

Commit and push this update:
```bash
git add README.md
git commit -m "Update README with live dashboard link"
git push origin main
```

### Step 6: Update Project Links

Add the dashboard link to:

1. **GitHub Repository Description**
   - Go to your repo on GitHub
   - Click the gear icon ⚙️ next to "About"
   - Add your Streamlit Cloud URL
   - Add topics: `data-science`, `churn-prediction`, `streamlit`, `data-analysis`

2. **LinkedIn Featured Section**
   - Add as "External link"
   - Title: "Interactive Churn Analysis Dashboard"
   - URL: Your Streamlit Cloud link

3. **PROJECT_SUMMARY.md**
   - Add dashboard link at the top

## 🔧 Troubleshooting

### App Won't Start
- Check deployment logs in Streamlit Cloud
- Verify `requirements.txt` has all dependencies
- Ensure data file path is correct (`data/telco_churn.csv`)

### Missing Dependencies
Add to `requirements.txt`:
```
streamlit==1.29.0
pandas==2.1.3
numpy==1.26.2
plotly==5.18.0
scikit-learn==1.3.2
```

### File Not Found Errors
- Ensure `data/telco_churn.csv` exists in your repository
- Check file paths are relative (not absolute)

### App is Slow
- Add `@st.cache_data` decorator to data loading (already done)
- Consider reducing data size if necessary
- Optimize heavy computations

## 📊 App Management

### Reboot App
- From Streamlit Cloud dashboard
- Click "⋮" menu → "Reboot app"
- Useful after pushing changes

### View Logs
- Click "Manage app" to see real-time logs
- Helpful for debugging issues

### Update App
- Just push changes to GitHub
- Streamlit Cloud auto-deploys from `main` branch
- Changes typically reflect in 1-2 minutes

## 🎯 Post-Deployment Checklist

- [ ] App loads successfully at public URL
- [ ] All four pages render correctly
- [ ] Visualizations display properly
- [ ] Filters and inputs work as expected
- [ ] README updated with live link
- [ ] GitHub repo description updated
- [ ] LinkedIn Featured section updated
- [ ] PROJECT_SUMMARY.md updated with dashboard link

## 🌟 Make Your Dashboard Stand Out

### Custom Domain (Optional)
- Upgrade to Streamlit Cloud paid plan
- Add your own domain (e.g., `churn.yourdomain.com`)

### Share on Social Media
Use this sample post:

> 🚀 Just deployed an interactive customer churn analysis dashboard!
> 
> Built with Python & Streamlit, it allows you to:
> ✅ Predict churn risk for new customers
> ✅ Filter 7K+ customers by risk profile
> ✅ Calculate ROI for retention campaigns
> 
> Try it yourself: [YOUR-LINK]
> GitHub: [YOUR-REPO]
> 
> #DataScience #MachineLearning #Streamlit #CustomerAnalytics

---

**Next Step:** Test your live dashboard and share it on LinkedIn!
