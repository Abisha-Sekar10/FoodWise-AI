"""
FoodWise AI - Push to GitHub Helper Script
Uses Dulwich pure-Python Git client to push without requiring git.exe on PATH.
"""

import sys
import getpass
from dulwich.repo import Repo
from dulwich import porcelain

def main():
    repo_path = "."
    print("=" * 60)
    print("FoodWise AI - Push Repository to GitHub")
    print("=" * 60)

    repo = Repo(repo_path)
    
    # 1. Ask for repository URL
    repo_url = input("\nEnter your GitHub repository URL\n(e.g., https://github.com/your-username/foodwise-ai.git): ").strip()
    if not repo_url:
        print("Error: Repository URL cannot be empty.")
        return

    # Normalize URL if needed
    if not repo_url.endswith(".git") and "github.com" in repo_url:
        repo_url += ".git"

    # Set or update origin remote
    try:
        porcelain.remote_add(repo, b"origin", repo_url.encode("utf-8"))
        print("Added remote 'origin'.")
    except Exception:
        # Remote may already exist
        config = repo.get_config()
        config.set((b"remote", b"origin"), b"url", repo_url.encode("utf-8"))
        config.write_to_path()
        print("Updated remote 'origin' URL.")

    # 2. Authentication
    print("\nGitHub Authentication:")
    print("Note: GitHub requires a Personal Access Token (PAT) instead of your password.")
    print("Create one at: https://github.com/settings/tokens (classic with 'repo' scope)")
    
    username = input("\nGitHub Username: ").strip()
    token = getpass.getpass("GitHub Personal Access Token (hidden input): ").strip()

    if not username or not token:
        print("Error: Username and Token are required to push.")
        return

    # Embed credentials into push URL
    # https://<username>:<token>@github.com/<owner>/<repo>.git
    clean_url = repo_url.replace("https://", "")
    auth_url = f"https://{username}:{token}@{clean_url}"

    print(f"\nPushing 'main' branch to {repo_url}...")
    try:
        # Dulwich push
        porcelain.push(repo, auth_url, refspecs=b"refs/heads/master:refs/heads/main")
        print("\n" + "=" * 60)
        print("SUCCESS! Your repository has been pushed to GitHub.")
        print(f"View it at: {repo_url.replace('.git', '')}")
        print("=" * 60)
    except Exception as e:
        # Try pushing master to master
        try:
            porcelain.push(repo, auth_url, refspecs=b"refs/heads/master:refs/heads/master")
            print("\n" + "=" * 60)
            print("SUCCESS! Your repository has been pushed to GitHub (branch: master).")
            print(f"View it at: {repo_url.replace('.git', '')}")
            print("=" * 60)
        except Exception as err:
            print(f"\nPush failed: {err}")
            print("\nAlternative: Use standard Git or GitHub Desktop if preferred.")

if __name__ == "__main__":
    main()
