# GitHub Setup & Push Instructions

## 🚀 Step-by-Step Guide to Push Your Project to GitHub

Your project is now committed to git locally. Follow these steps to push it to GitHub:

---

## Step 1: Create a New GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name:** `telco-churn-analysis` or `da_project_1`
   - **Description:** "Customer churn analysis identifying $1.67M revenue exposure and risk segmentation framework"
   - **Visibility:** ✅ **Public** (for portfolio visibility)
   - **DO NOT** initialize with README, .gitignore, or license (you already have these)
5. Click **"Create repository"**

---

## Step 2: Link Your Local Repository to GitHub

GitHub will show you commands to run. Use the **"...or push an existing repository from the command line"** section.

In your terminal, run:

```bash
cd /Users/gagepiercegaubert/Desktop/career_projects/da_project_1

# Add GitHub as remote (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/telco-churn-analysis.git

# Verify the remote was added
git remote -v

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Important:** Replace `YOUR-USERNAME` with your actual GitHub username!

---

## Step 3: Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md should display automatically with your visualizations

---

## Step 4: Configure Repository Settings

### Add Topics/Tags

1. Go to your repository on GitHub
2. Click the ⚙️ icon next to "About" (top right of repo)
3. Add these topics:
   - `data-analysis`
   - `python`
   - `machine-learning`
   - `customer-analytics`
   - `scikit-learn`
   - `churn-prediction`
   - `logistic-regression`
   - `pandas`
4. Update the description if needed
5. Click "Save changes"

### Pin to Your Profile

1. Go to your GitHub profile page
2. Click "Customize your pins"
3. Select this repository
4. It will appear in your top 6 repositories

---

## Step 5: Create a Release (Optional but Recommended)

1. Go to your repository on GitHub
2. Click "Releases" on the right sidebar
3. Click "Create a new release"
4. Tag version: `v1.0`
5. Release title: "Initial Release - Portfolio Ready"
6. Description:
   ```
   Complete telco customer churn analysis project including:
   - Portfolio notebook for quick review (15-20 min)
   - Full technical analysis with detailed methodology
   - Risk segmentation framework identifying $1.67M revenue exposure
   - Executive-ready visualizations
   - Interview preparation materials
   ```
7. Click "Publish release"

---

## Step 6: Update README with Your Information

Update the placeholder links in your README:

```bash
# Open README in your editor and update:
# - GitHub link (add your actual repo URL)
# - LinkedIn URL
# - Email or portfolio website
```

Then commit and push the changes:

```bash
git add README.md
git commit -m "docs: Add personal links to README"
git push origin main
```

---

## 📋 Quick Reference Commands

```bash
# Check status
git status

# View commit history
git log --oneline -n 10

# Add specific files
git add filename.py

# Add all changed files
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main

# Pull latest changes (if collaborating)
git pull origin main

# Check remote URL
git remote -v
```

---

## 🔒 If You Want to Use SSH Instead of HTTPS

SSH is more convenient (no password required after setup):

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy your public key
cat ~/.ssh/id_ed25519.pub

# Add it to GitHub:
# 1. Go to GitHub Settings → SSH and GPG keys
# 2. Click "New SSH key"
# 3. Paste your public key

# Change your remote to SSH
git remote set-url origin git@github.com:YOUR-USERNAME/telco-churn-analysis.git
```

---

## 🎯 Verify Everything Works

After pushing, verify these are visible on GitHub:

- [ ] README.md displays correctly with images
- [ ] All 3 images show up in the README
- [ ] Notebooks are viewable (GitHub renders .ipynb files)
- [ ] PROJECT_SUMMARY.md and INTERVIEW_PREP.md are accessible
- [ ] Repository has relevant topics/tags
- [ ] Repository description is clear and compelling

---

## 📱 Share Your Project

Once published, you can share it in multiple ways:

### Direct Link
```
https://github.com/YOUR-USERNAME/telco-churn-analysis
```

### In Applications/Emails
```
"View my telco churn analysis project identifying $1.67M revenue exposure: 
https://github.com/YOUR-USERNAME/telco-churn-analysis"
```

### LinkedIn Post
```
🎯 Just completed a customer retention analysis project!

Analyzed 7K+ telecom customer records and built a risk segmentation framework 
that identified $1.67M in annual revenue exposure.

Key findings:
• Month-to-month contracts churn at 15x the rate of yearly contracts
• First 12 months are critical for retention
• Built ML model with 80% recall to catch at-risk customers

Tools: Python, Pandas, Scikit-learn, SQL

Check out the full analysis: [GitHub Link]

#DataScience #Python #MachineLearning #CustomerAnalytics
```

---

## ⚠️ Troubleshooting

### "Permission denied" when pushing
- Make sure you're using the correct GitHub username in the remote URL
- Try using a Personal Access Token instead of your password
- Go to GitHub Settings → Developer settings → Personal access tokens → Generate new token

### "Remote already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/telco-churn-analysis.git
```

### Images don't show in README on GitHub
- Make sure the images are committed: `git ls-files images/`
- Check the image paths in README are correct (case-sensitive)
- Try pushing again: `git push origin main`

### Large files causing issues
- The .gitignore should handle this, but if you have large data files:
```bash
git rm --cached path/to/large/file
echo "path/to/large/file" >> .gitignore
git commit -m "Remove large file from tracking"
```

---

## 🎉 Next Steps After Pushing

1. Share the link with 2-3 trusted friends for feedback
2. Add the GitHub link to your resume
3. Create a LinkedIn post announcing the project
4. Consider recording a quick Loom walkthrough (3-5 min)
5. Apply to jobs with this as your featured project!

---

**Need Help?** 
If you encounter any issues pushing to GitHub, let me know and I can help troubleshoot!
