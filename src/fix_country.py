import re
import pandas as pd

df = pd.read_csv("data/cleaned_earthquakes.csv", parse_dates=["time", "updated"])

bad = (df["country"].str.contains("earthquake", case=False, na=False)
       | df["country"].str.match(r"^\d"))
print("Rows to fix:", bad.sum())

def fix_country(place):
    p = re.sub(r"^\d{4}\s+", "", place)                              # leading year
    p = re.sub(r"\s+earthquake(\s+sequence)?$", "", p, flags=re.I)   # trailing "Earthquake"
    m = re.search(r",\s*([^,]+)$", p)
    return (m.group(1) if m else p).strip()

EXTRA = {"Alaska": "United States", "California": "United States", "Nevada": "United States",
         "Texas": "United States", "Hawaii": "United States", "Lake Almanor": "United States",
         "Kahramanmaras": "Turkey"}

df.loc[bad, "country"] = df.loc[bad, "place"].apply(fix_country).replace(EXTRA)

lookup = df.loc[~bad].drop_duplicates("country").set_index("country")["continent"]
df.loc[bad, "continent"] = df.loc[bad, "country"].map(lookup).fillna("Ocean/Other")

print(df.loc[bad, ["place", "country", "continent"]].drop_duplicates("country").to_string())
left = df[df["country"].str.contains("earthquake", case=False) | df["country"].str.match(r"^\d")]
print("Still wrong:", len(left))
print(left[["place", "country"]].drop_duplicates().to_string())

df.to_csv("data/cleaned_earthquakes.csv", index=False)
print("Saved", df.shape)