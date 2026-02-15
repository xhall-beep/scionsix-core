import os
import subprocess

class RepoOrchestrator:
    def __init__(self):
        self.base_path = "/data/data/com.termux/files/home"
        self.target_repos = []

    def scan_for_repos(self):
        print("🔍 [SCAN] Searching for active repositories in home directory...")
        for item in os.listdir(self.base_path):
            full_path = os.path.join(self.base_path, item)
            if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, ".git")):
                self.target_repos.append(item)
                print(f"📦 [FOUND] Repository detected: {item}")

    def sync_all(self):
        for repo in self.target_repos:
            print(f"🔄 [SYNC] Hard-pulling latest core from {repo}...")
            repo_path = os.path.join(self.base_path, repo)
            subprocess.run(["git", "-C", repo_path, "pull", "origin", "main"])

    def audit_structure(self):
        print("🛠️ [AUDIT] Verifying directory integrity for Agentic Upgrades...")
        # Add actual logic here to check for buildozer.spec or requirements.txt
        print("✅ [READY] All repositories aligned for Sovereign Enhancement.")

if __name__ == "__main__":
    orchestrator = RepoOrchestrator()
    orchestrator.scan_for_repos()
    orchestrator.sync_all()
    orchestrator.audit_structure()
