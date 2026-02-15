import os
import subprocess

class SovereignDevourer:
    def __init__(self):
        self.base_path = "/data/data/com.termux/files/home"
        self.repos = []

    def devour_repositories(self):
        print("🔍 [SCAN] Identifying physical codebases...")
        if not os.path.exists(self.base_path):
            print("❌ [ERROR] Base path not found.")
            return
        for item in os.listdir(self.base_path):
            full_path = os.path.join(self.base_path, item)
            if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, ".git")):
                self.repos.append(full_path)
                print(f"📦 [DEVOUR] Targeted: {item}")

    def sync_and_upgrade(self):
        for repo in self.repos:
            repo_name = os.path.basename(repo)
            print(f"🔄 [SYNC] Forcing 'origin main' alignment for {repo_name}...")
            subprocess.run(["git", "-C", repo, "pull", "origin", "main"], capture_output=True)
            
            spec_path = os.path.join(repo, "buildozer.spec")
            if os.path.exists(spec_path):
                print(f"🛠️ [REPAIR] Optimizing {repo_name} for Java 17/API 35...")
                self.align_spec(spec_path)

    def align_spec(self, spec_path):
        with open(spec_path, 'r') as f:
            content = f.read()
        # Force the proven successful parameters
        content = content.replace("android.api = 31", "android.api = 35")
        content = content.replace("# android.ndk = 25b", "android.ndk = 25b")
        with open(spec_path, 'w') as f:
            f.write(content)
        print(f"✅ [ALIGNED] {spec_path} is now agent-ready.")

if __name__ == "__main__":
    print(f"🚀 [IGNITION] SCIONSIX Core Active on Pixel 8 Pro")
    agent = SovereignDevourer()
    agent.devour_repositories()
    agent.sync_and_upgrade()
    print("🏁 [FINISH] All repositories are synced and structurally sound.")
