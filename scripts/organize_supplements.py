import os
import shutil
from pathlib import Path
import pandas as pd
import subprocess

def ensure_files_exist():
    # Create directories if not exist
    Path("data/raw/telegram").mkdir(parents=True, exist_ok=True)
    Path("data/raw/images").mkdir(parents=True, exist_ok=True)
    Path("data/labeled").mkdir(parents=True, exist_ok=True)
    Path("config").mkdir(exist_ok=True)

    # Telegram data
    telegram_path = "data/raw/telegram/raw_messages.csv"
    if not os.path.exists(telegram_path):
        pd.DataFrame(columns=['text', 'date', 'views', 'channel']).to_csv(
            telegram_path, index=False)
        print("Created empty telegram data file")

    # Labeled data
    label_path = "data/labeled/initial_labels.txt"
    if not os.path.exists(label_path):
        with open(label_path, "w", encoding="utf-8") as f:
            f.write("# Sample label format\nPRODUCT: ልብስ\nPRICE: 500 ብር\nLOCATION: አዲስ አበባ")
        print("Created sample label file")

    # Channels list
    channels_path = "config/channels.txt"
    if not os.path.exists(channels_path):
        with open(channels_path, "w", encoding="utf-8") as f:
            f.write("@Shageronlinestore\n@Channel2\n@Channel3")
        print("Created sample channels file")

    # Images directory
    if not os.path.exists("data/raw/images"):
        os.makedirs("data/raw/images")
        print("Created empty images directory")

def initialize_dvc():
    try:
        # Initialize quietly
        subprocess.run(["dvc", "init", "-q"], check=True)
        print("DVC initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize DVC: {e}")
        return False

def organize_files():
    print("Organizing supplement files...")
    ensure_files_exist()
    
    # Initialize DVC
    if not initialize_dvc():
        print("Continuing without DVC initialization")
        return
    
    # Add files individually to avoid git-ignore issues
    try:
        subprocess.run(["dvc", "add", "data/raw/telegram", "data/labeled"], check=True)
        print("Files added to DVC")
        
        # Push to remote
        subprocess.run(["dvc", "push", "-q"], check=True)
        print("✅ Files versioned in DVC")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ DVC operation failed: {e}")

    print("\nNext steps:")
    print("1. Verify these files exist:")
    print("   - data/raw/telegram/raw_messages.csv")
    print("   - data/labeled/initial_labels.txt")
    print("2. Run: python src/data/label_conversion.py")

if __name__ == "__main__":
    organize_files()