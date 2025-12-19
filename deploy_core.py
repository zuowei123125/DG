import os
import subprocess
import sys
import shutil

# Path to npm (ensure it's in PATH or provide full path)
NPM_CMD = "npm" # or "npm.cmd" on Windows
PUBLISH_SCRIPT = "publish.py"
DESIGNER_DIR = "Designer"
DIST_DIR = os.path.join(DESIGNER_DIR, "dist_core")

def run_command(command, cwd=None, shell=True):
    """Run a shell command and check for errors."""
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, cwd=cwd, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main():
    print("=== Auto Deploy Designer Core ===")
    
    # 1. Build Core
    print("\n[1/3] Building Designer Core...")
    # Using npm run build:core as requested (or build:shell if that's what produces the needed output)
    # The user prompt said "npm run build:core -> Designer/dist_core/"
    # Let's verify package.json scripts again. 
    # package.json says: "build:core": "vue-tsc && vite build"
    # Usually vite build outputs to 'dist' by default, user said 'dist_core'. 
    # I'll assume vite.config.ts is configured to output to dist_core OR I should move it.
    # Let's run the build command.
    
    run_command(f"{NPM_CMD} run build:core", cwd=DESIGNER_DIR)
    
    # Verify output directory exists
    # Note: If vite config outputs to 'dist', we might need to rename it to 'dist_core' to match user expectation
    # Let's check if dist_core exists, if not check dist
    if not os.path.exists(DIST_DIR):
        default_dist = os.path.join(DESIGNER_DIR, "dist")
        if os.path.exists(default_dist):
            print(f"Build output found at '{default_dist}', renaming to '{DIST_DIR}'...")
            if os.path.exists(DIST_DIR):
                shutil.rmtree(DIST_DIR)
            os.rename(default_dist, DIST_DIR)
        else:
            print(f"Error: Build output directory '{DIST_DIR}' not found.")
            sys.exit(1)

    # 2. Package and Upload
    print("\n[2/3] Packaging and Uploading...")
    # Call existing publish.py script
    # It will auto-zip 'Designer/dist_core' into 'core_{timestamp}.zip' and upload
    run_command(f"{sys.executable} {PUBLISH_SCRIPT} {DIST_DIR}")

    print("\n[3/3] Deployment Complete!")

if __name__ == "__main__":
    main()
