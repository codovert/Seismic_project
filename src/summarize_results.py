import glob, os, pandas as pd

os.makedirs("docs", exist_ok=True)
files = sorted(glob.glob("results/*.csv"), key=lambda x: int(os.path.basename(x).split("_")[0]))
with open("docs/results_summary.txt", "w", encoding="utf-8") as out:
    for f in files:
        df = pd.read_csv(f)
        out.write(f"=== {os.path.basename(f)} ({len(df)} rows) ===\n")
        out.write(df.head(5).to_string(index=False) + "\n\n")
print("Saved docs/results_summary.txt")