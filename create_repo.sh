#!/bin/bash
# Quick GitHub Repository Creation Script

echo "🚀 Creating GitHub Repository: telco-churn-analysis"
echo ""

# Method 1: Try GitHub CLI first
echo "Attempting to create repository with GitHub CLI..."
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI found"

    # Check authentication
    if gh auth status &> /dev/null; then
        echo "✓ Already authenticated"
    else
        echo "⚠ Not authenticated - logging in..."
        gh auth login
    fi

    # Create repository and push
    echo ""
    echo "Creating public repository and pushing..."
    gh repo create telco-churn-analysis \
        --public \
        --source=. \
        --description="Customer churn analysis identifying \$1.67M revenue exposure and risk segmentation framework" \
        --push

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ SUCCESS! Repository created and pushed!"
        echo ""
        gh repo view --web
        exit 0
    else
        echo "❌ GitHub CLI method failed, trying manual method..."
    fi
else
    echo "ℹ GitHub CLI not installed"
fi

# Method 2: Manual method
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MANUAL SETUP (if CLI didn't work)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Create repository on GitHub:"
echo "    → Go to: https://github.com/new"
echo "    → Name: telco-churn-analysis"
echo "    → Make it PUBLIC"
echo "    → DON'T initialize with README"
echo ""
echo "2️⃣  Then run these commands:"
echo ""
echo "    # Add your GitHub username below:"
read -p "    Enter your GitHub username: " USERNAME
echo ""

if [ -z "$USERNAME" ]; then
    echo "    No username provided. Here's what to run:"
    echo ""
    echo "    git remote add origin https://github.com/YOUR-USERNAME/telco-churn-analysis.git"
    echo "    git branch -M main"
    echo "    git push -u origin main"
else
    echo "    Running commands now..."
    git remote remove origin 2>/dev/null
    git remote add origin "https://github.com/$USERNAME/telco-churn-analysis.git"
    git branch -M main

    echo ""
    echo "📤 Pushing to GitHub..."
    git push -u origin main

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ SUCCESS!"
        echo ""
        echo "Your repository: https://github.com/$USERNAME/telco-churn-analysis"
        echo ""
        echo "Next steps:"
        echo "  • Add topics: data-analysis, python, machine-learning"
        echo "  • Pin to your profile"
        echo "  • Update README with your links"
    else
        echo ""
        echo "⚠ Push failed. Common fixes:"
        echo ""
        echo "  • Make sure you created the repo on GitHub first"
        echo "  • You may need to use a Personal Access Token instead of password"
        echo "  • Get token at: https://github.com/settings/tokens"
    fi
fi

echo ""
