import sys
sys.path.append("src")

import streamlit as st
import plotly.express as px
from db import run_query
from queries import QUERIES

st.set_page_config(page_title="Global Seismic Trends", page_icon="🌍", layout="wide")
st.title("🌍 Global Seismic Trends: Data-Driven Earthquake Insights")

page = st.sidebar.radio("Navigate", ["Overview", "SQL Insights (26 queries)", "Map Explorer"])

@st.cache_data(show_spinner=False)
def q(sql, params=None):
    return run_query(sql, params)

NOTES = {
    "6.": "2026 is a partial year (January to October), so its count is lower.",
    "11.": "Casualty data is not in the 26 features; total significance (sig) is used as a proxy.",
    "13.": "Alert levels are not in the 26 features; magnitude category is used as a proxy.",
    "20.": "Alert levels are not in the 26 features; magnitude category is used as a proxy.",
    "23.": "2026 is a partial year, so its growth rate is understated.",
    "21.": "Only countries with at least 30 events are included.",
    "26.": "Only countries with at least 30 events and at least one deep event are included.",
}

def auto_chart(df):
    if df.shape[0] < 2 or df.shape[0] > 60 or df.shape[1] < 2:
        return None
    cols = [c for c in df.columns if c != "id"]
    x = cols[0]
    nums = [c for c in cols[1:] if df[c].dtype.kind in "if"]
    if x in ("year", "yr", "month", "hour"):
        nums = nums or [c for c in cols[1:] if df[c].dtype.kind in "if"]
    if not nums:
        return None
    if x in ("year", "yr", "month", "hour"):
        return px.line(df, x=x, y=nums[0], markers=True)
    return px.bar(df, x=x, y=nums[0], text_auto=True)

# ---------------- Overview ----------------
if page == "Overview":
    k = q("""SELECT COUNT(*) AS total, ROUND(AVG(mag),2) AS avg_mag, MAX(mag) AS max_mag,
                    SUM(tsunami) AS tsunamis, COUNT(DISTINCT country) AS countries
             FROM earthquakes""").iloc[0]
    c = st.columns(5)
    c[0].metric("Total earthquakes", f"{int(k['total']):,}")
    c[1].metric("Average magnitude", k["avg_mag"])
    c[2].metric("Maximum magnitude", k["max_mag"])
    c[3].metric("Tsunami events", int(k["tsunamis"]))
    c[4].metric("Countries / regions", int(k["countries"]))

    left, right = st.columns(2)
    yr = q("SELECT `year`, COUNT(*) AS total FROM earthquakes GROUP BY `year` ORDER BY `year`")
    left.plotly_chart(px.line(yr, x="year", y="total", markers=True,
                              title="Earthquakes per year (2026 is partial)"), use_container_width=True)
    top = q("SELECT country, COUNT(*) AS total FROM earthquakes GROUP BY country ORDER BY total DESC LIMIT 10")
    right.plotly_chart(px.bar(top, x="country", y="total", text_auto=True,
                              title="Top 10 most active countries / regions"), use_container_width=True)

# ---------------- SQL Insights ----------------
elif page == "SQL Insights (26 queries)":
    group = st.sidebar.selectbox("Category", list(QUERIES))
    name = st.selectbox("Question", list(QUERIES[group]))
    sql = QUERIES[group][name]
    df = q(sql)

    st.subheader(name)
    for key, note in NOTES.items():
        if name.startswith(key):
            st.info(note)
    with st.expander("View SQL"):
        st.code(sql.strip(), language="sql")

    col1, col2 = st.columns(2)
    col1.dataframe(df, use_container_width=True)
    fig = auto_chart(df)
    if fig:
        col2.plotly_chart(fig, use_container_width=True)
    st.download_button("Download result as CSV", df.to_csv(index=False), file_name="result.csv")

# ---------------- Map Explorer ----------------
else:
    yrs = q("SELECT MIN(`year`) AS a, MAX(`year`) AS b FROM earthquakes").iloc[0]
    y = st.sidebar.slider("Year", int(yrs["a"]), int(yrs["b"]), (int(yrs["a"]), int(yrs["b"])))
    m = st.sidebar.slider("Magnitude", 3.0, 9.5, (5.0, 9.5))
    conts = q("SELECT DISTINCT continent FROM earthquakes ORDER BY continent")["continent"].tolist()
    sel = st.sidebar.multiselect("Continent", conts, default=conts)

    if sel:
        marks = ",".join(f":c{i}" for i in range(len(sel)))
        params = {"y1": y[0], "y2": y[1], "m1": m[0], "m2": m[1],
                  **{f"c{i}": v for i, v in enumerate(sel)}}
        df = q(f"""SELECT latitude, longitude, mag, depth_km, place, `time`
                   FROM earthquakes
                   WHERE `year` BETWEEN :y1 AND :y2 AND mag BETWEEN :m1 AND :m2
                         AND continent IN ({marks})
                   ORDER BY mag DESC LIMIT 5000""", params)
        st.write(f"Showing {len(df):,} earthquakes (strongest 5,000 at most)")
        if len(df):
            st.plotly_chart(px.scatter_geo(df, lat="latitude", lon="longitude", color="depth_km",
                            size="mag", hover_name="place", projection="natural earth",
                            color_continuous_scale="Turbo"), use_container_width=True)
    else:
        st.warning("Select at least one continent.")