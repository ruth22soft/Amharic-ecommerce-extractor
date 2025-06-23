# src/data/label_conversion.py
import os
from pathlib import Path
import pandas as pd

def convert_labels():
    # Ensure labeled data exists
    label_path = Path("data/labeled/initial_labels.txt")
    if not label_path.exists():
        print("Creating sample labeled data...")
        with open(label_path, "w") as f:
            f.write("PRODUCT: ልብስ\nPRICE: 500 ብር\nLOCATION: አዲስ አበባ")

    # Load and convert labels
    with open(label_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Conversion logic - modify based on your actual data
    conll_lines = []
    for line in content.split('\n'):
        if line.startswith("PRODUCT:"):
            product = line.split(":")[1].strip()
            conll_lines.append(f"{product}\tB-PRODUCT")
        elif line.startswith("PRICE:"):
            price = line.split(":")[1].strip()
            conll_lines.append(f"{price}\tB-PRICE")
        elif line.startswith("LOCATION:"):
            loc = line.split(":")[1].strip()
            conll_lines.append(f"{loc}\tB-LOC")

    # Save converted file
    output_path = "data/labeled/converted.conll"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(conll_lines))

    print(f"✅ Labels converted and saved to {output_path}")
    print("Next steps:")
    print("1. Review converted.conll file")
    print("2. Run model training: python src/models/training.py")

if __name__ == "__main__":
    convert_labels()