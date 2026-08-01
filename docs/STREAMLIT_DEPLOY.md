# Streamlit Community Cloud — Exact Deployment Steps

## 1) Push to GitHub

Create a GitHub repository and push this project to the `main` branch.

```bash
git init
git add .
git commit -m "feat: add deploy-ready World Cup analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

## 2) Deploy

Open Streamlit Community Cloud and choose **Create app**.

Use:

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`

Deploy the app.

## 3) After deployment

The app should open on a `*.streamlit.app` URL. Test these pages in order:

1. Overview
2. Match Center
3. Teams Intelligence
4. Player Lab
5. Squad & Venue Lab
6. SQL Analytics Lab
7. Data & Methodology

## 4) SQL page

The SQLite warehouse is intentionally not committed. The SQL layer creates it automatically from `data/raw/*.csv` the first time a SQL query is executed.

## 5) Mobile test

Open the deployed URL from a phone and check:

- top navigation scrolls horizontally
- sidebar starts collapsed
- filters remain usable
- charts remain readable
- Match Center and SQL tables can scroll horizontally when needed

## 6) Updates

Push changes to GitHub. Streamlit Community Cloud automatically rebuilds the app when the source or dependency files change.
