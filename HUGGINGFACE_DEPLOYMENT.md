# Hugging Face Spaces Deployment Guide

Hugging Face Spaces provides free hosting for ML and data science apps. It's particularly good if you want visibility in the machine learning community since lots of researchers and practitioners browse Spaces regularly.

## What You Need

You already have:
- Streamlit app created (streamlit_app.py)
- requirements.txt with dependencies

You'll need:
- Hugging Face account (free to create)
- GitHub repository (optional but recommended)

---

## Two Ways to Deploy

### Option 1: Direct Upload (Fastest)

This is simpler if you haven't pushed to GitHub yet or just want to get it live quickly.

**Step 1: Create a Hugging Face Account**
1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up" (free account)
3. Verify your email

**Step 2: Create a New Space**

1. Click your profile icon and select "New Space"
2. Fill in the form:
   - Name: telco-churn-analysis (or whatever you prefer)
   - License: MIT
   - Space SDK: Choose Streamlit from the dropdown
   - Space Hardware: CPU basic (this is free)
   - Visibility: Public
3. Click "Create Space"

The Space will be created but empty at first. That's normal.

**Step 3: Upload Your Files**

You need to get these files into your Space:
- streamlit_app.py (your main app)
- requirements.txt (dependencies)
- data/telco_churn.csv (the dataset)
- README_SPACE.md (rename this to README.md when uploading)

Optional:
- .streamlit/config.toml (theme config)

**Step 4: Actually Upload Them**

1. In your new Space, click the "Files" tab
2. Click "Add file" then "Upload files"
3. Select streamlit_app.py, requirements.txt, and telco_churn.csv
4. For the data folder structure, you have two options:
   - Upload telco_churn.csv and manually create the data/ folder structure
   - Or modify streamlit_app.py to look for the CSV at the root level
5. Upload README_SPACE.md as README.md (this shows up on your Space homepage)
6. Click "Commit changes to main"

Hugging Face uses git under the hood, so every change is a commit.

**Step 5: Wait for It to Build**

Hugging Face will automatically install your dependencies and start the app. This takes 2-5 minutes typically. You can watch the build logs at the top of the page. When you see "Running" instead of "Building", you're live.

**Step 6: Test It**

Your app will be at: https://huggingface.co/spaces/YOUR-USERNAME/telco-churn-analysis

Make sure all four pages load and the filters work correctly.

---

### Option 2: Sync from GitHub (Better Long-Term)

If you plan to keep updating the dashboard, syncing from GitHub is cleaner. Every time you push to GitHub, your Space automatically updates.

**Step 1: Push Everything to GitHub**
If you haven't already:
```bash
# Make sure everything is committed
git add .
git commit -m "Add Streamlit dashboard for deployment"

# Create GitHub repo and push (if not done)
# Follow GITHUB_SETUP.md
git push origin main
```

### Step 2: Create Hugging Face Space
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in details:
   - **Name**: `telco-churn-analysis`
   - **License**: MIT
   - **Space SDK**: **Streamlit**
   - **Space Hardware**: CPU basic (free)
   - **Visibility**: Public
3. Click "Create Space"

**Step 2: Create Your Space**

1. Go to huggingface.co/new-space
2. Fill in:
   - Name: telco-churn-analysis
   - License: MIT
   - Space SDK: Streamlit
   - Space Hardware: CPU basic (free)
   - Visibility: Public
3. Click "Create Space"

**Step 3: Connect to GitHub**

Once the Space is created:
1. Go to the "Settings" tab
2. Find "Repository sync" section
3. Click "Connect to GitHub"
4. Select your repository: YOUR-USERNAME/telco-churn-analysis
5. Choose branch: main
6. Enable "Sync on push" so it auto-updates when you push changes
7. Click "Sync repository"

Hugging Face will pull all your files from GitHub and start building.

**Step 4: Use the Space README**

I already created README_SPACE.md in your project. If you're syncing from GitHub, just rename it to README.md or copy its contents. The Space displays this README on your app's homepage, so it's worth having a good one.

If you're manually uploading files, upload README_SPACE.md as README.md to your Space.

## What Your Space Should Look Like

File structure:
```
your-space/
├── streamlit_app.py
├── requirements.txt
├── data/
│   └── telco_churn.csv
├── .streamlit/
│   └── config.toml (optional)
└── README.md
```

The requirements.txt you have should work fine. If you run into version conflicts, try using minimum versions instead of pinned ones:
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
scikit-learn>=1.3.0
```

## If Something Goes Wrong

**Getting "Application Error"**

Check the build logs first (Settings tab, then View Logs). Usually it's a missing file or dependency issue. Make sure data/telco_churn.csv actually exists in your Space.

**"Module not found" errors**

Add the missing package to requirements.txt. If that doesn't work, try pinning to a specific version that you know works locally. You can also try Settings > Factory reboot to clear the cache.

**App is slow or times out**

The first load on the free tier can take 10-30 seconds. That's normal. After that it should be faster. If it's consistently slow, you might need to upgrade to a better CPU tier (costs a bit) or optimize your data loading further.

**File not found errors**

Double-check that your file paths are relative, not absolute. The CSV should be at data/telco_churn.csv, and your streamlit_app.py should load it with that relative path.

## After It's Live

**Update your links**

Change the "Coming Soon" in your README to the actual Space URL:
```markdown
**[Launch Live Demo](https://huggingface.co/spaces/YOUR-USERNAME/telco-churn-analysis)**
```

Also update:
- GitHub repo description (add the Space link)
- LinkedIn Featured section (add as external link)
- PROJECT_SUMMARY.md
- Your resume or portfolio site

**Share it**

If you want to post on LinkedIn, here's a template without the corporate jargon:

```
I just deployed an interactive dashboard for my customer churn analysis project. 

You can explore 7,000+ customer records, predict churn risk for individual customers, and model the ROI of different retention strategies. The analysis identified $1.67M in annual revenue exposure with a model that catches 80% of actual churners.

Try it: https://huggingface.co/spaces/YOUR-USERNAME/telco-churn-analysis
Code: github.com/YOUR-USERNAME/telco-churn-analysis

#DataScience #MachineLearning #CustomerAnalytics
```

Keep it straightforward. Let the work speak for itself.

**Make it look better**

Take a screenshot of your dashboard and upload it as thumbnail.png to your Space. Add this line to your README frontmatter: `thumbnail: thumbnail.png`. This shows up when people are browsing Spaces.

Add some tags in your Space settings for discoverability: customer-analytics, churn-prediction, business-intelligence, etc.

Pin the Space to your profile so it shows up prominently when people visit your Hugging Face page.

---

## Why Hugging Face Spaces

It's free with a generous tier, you get automatic GitHub sync, and there's good discoverability in the ML community. People actually browse Spaces looking for interesting projects. You also get basic analytics (views, likes) and people can comment or start discussions on your Space.

The URL looks professional too: huggingface.co/spaces/your-username/project-name

## Quick Checklist

- Create Hugging Face account
- Create new Space with Streamlit SDK
- Either upload files directly or sync from GitHub  
- Wait 2-5 minutes for build
- Test all four pages
- Update your README and other links
- Share it

That's it. Pretty straightforward once you get started.

## Streamlit Cloud vs Hugging Face

Both are good options:

**Streamlit Cloud**: Better if you want the official Streamlit branding. Free tier gives you one private app. Setup is slightly simpler.

**Hugging Face**: Better for visibility in the ML community. Unlimited public apps on free tier. Good if you want your work to be discovered organically.

For a portfolio project, I'd go with Hugging Face. More people will stumble across it, and it's specifically targeted at the data science audience you want to reach.
