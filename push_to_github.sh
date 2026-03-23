#!/bin/bash
# GitHub Push Script for Telco Churn Analysis Project

echo "=================================================="
echo "  TELCO CHURN ANALYSIS - GitHub Push Script"
echo "=================================================="
echo ""

# Step 1: Create GitHub Repository
echo "📝 STEP 1: Create GitHub Repository"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: telco-churn-analysis"
echo "3. Description: Customer churn analysis identifying \$1.67M revenue exposure and risk segmentation framework"
echo "4. Visibility: ✅ PUBLIC"
echo "5. DO NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
read -p "Press ENTER after creating the repository on GitHub..."

# Step 2: Get GitHub username
echo ""
echo "🔗 STEP 2: Configure Remote"
echo ""
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GitHub username cannot be empty"
    exit 1
fi

# Step 3: Add remote
echo ""
echo "Adding GitHub remote..."
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin "https://github.com/$GITHUB_USERNAME/telco-churn-analysis.git"

if [ $? -eq 0 ]; then
    echo "✅ Remote added successfully"
else
    echo "❌ Error adding remote"
    exit 1
fi

# Step 4: Verify what will be pushed
echo ""
echo "📊 STEP 3: Files to be Pushed"
echo ""
echo "Public Portfolio Files:"
echo "  ✓ README.md (with visualizations)"
echo "  ✓ PROJECT_SUMMARY.md"
echo "  ✓ INTERVIEW_PREP.md"
echo "  ✓ GITHUB_SETUP.md"
echo "  ✓ CHECKLIST.md"
echo "  ✓ notebooks/telco_churn_portfolio.ipynb (streamlined)"
echo "  ✓ notebooks/telco_churn_portfolio.html"
echo "  ✓ notebooks/telco_churn.ipynb (full analysis)"
echo "  ✓ data/telco_churn.csv (public Kaggle dataset)"
echo "  ✓ images/ (3 key visualizations)"
echo "  ✓ output/ (charts and high_risk_customers.csv)"
echo ""
echo "Excluded (kept private):"
echo "  ✗ first_thoughts.md (working notes)"
echo "  ✗ critique.md (working notes)"
echo "  ✗ project_guide.md (working notes)"
echo "  ✗ risk_seg_results.md (working notes)"
echo "  ✗ risk_segmentation_framework.md (working notes)"
echo "  ✗ Notebook working files"
echo ""
read -p "Ready to push? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ Push cancelled"
    exit 0
fi

# Step 5: Push to GitHub
echo ""
echo "🚀 STEP 4: Pushing to GitHub"
echo ""
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "  ✅ SUCCESS! Project Pushed to GitHub"
    echo "=================================================="
    echo ""
    echo "Your repository is live at:"
    echo "https://github.com/$GITHUB_USERNAME/telco-churn-analysis"
    echo ""
    echo "Next steps:"
    echo "1. Visit your repository and verify it displays correctly"
    echo "2. Add topics: data-analysis, python, machine-learning, churn-prediction"
    echo "3. Pin to your GitHub profile"
    echo "4. Update README with your personal links"
    echo ""
else
    echo ""
    echo "❌ Error pushing to GitHub"
    echo ""
    echo "Common issues:"
    echo "1. Check your GitHub username is correct"
    echo "2. Make sure the repository exists on GitHub"
    echo "3. You may need to authenticate with a Personal Access Token"
    echo ""
    echo "For help, see: GITHUB_SETUP.md"
fi
