import os, re
from db import run_query
from queries import QUERIES

os.makedirs("results", exist_ok=True)
sql_lines = []

for group, qs in QUERIES.items():
    for name, sql in qs.items():
        df = run_query(sql)
        fname = "results/" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:60] + ".csv"
        df.to_csv(fname, index=False)
        print(f"{name} -> {len(df)} rows")
        sql_lines.append(f"-- {name}\n{sql.strip()};\n")

with open("sql/queries.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines))
print("\nDone. 26 results saved in results/, SQL saved in sql/queries.sql")