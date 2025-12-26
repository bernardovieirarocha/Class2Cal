# Deploying to GitHub Pages

I have organized your project so it is **ready for 1-click deployment**.

## 1. File Reorganization
I moved your web application files to the `docs/` folder.
- `docs/index.html`
- `docs/app.js`

**Why?** GitHub Pages specifically allows deploying from a `/docs` folder on your main branch. This keeps your repository clean while allowing the site to be live.

## 2. How to Enable (GitHub Settings)
1.  **Push** these changes to your GitHub repository.
    ```bash
    git add .
    git commit -m "Prepare for GitHub Pages"
    git push origin main
    ```
2.  Go to your Repository on GitHub.
3.  Click **Settings** (tab).
4.  Click **Pages** (sidebar on left).
5.  Under **Build and deployment > Source**, choose **"Deploy from a branch"**.
6.  Under **Branch**, select `main` and then select the folder **`/docs`**.
7.  Click **Save**.

## 3. Result
In a few seconds, GitHub will give you a link (e.g., `https://your-user.github.io/Class2Cal/`). Your app is now online and free forever!
