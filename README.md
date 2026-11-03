# Global Earthquake Data Analysis (Python + MySQL)

In this project I cleaned a global earthquake dataset (2021 to 2026), loaded it into a MySQL database, and answered 30 analytical questions with SQL to understand where, when and how strongly earthquakes occur.

## Project Goals

- Clean and prepare raw earthquake records (USGS-style data) using Python and pandas.
- Engineer useful features such as country, continent, magnitude category, depth category, year, month, hour and day of week.
- Store the cleaned data in MySQL.
- Use SQL to study magnitude, depth, time patterns, impact, event quality and regional trends.
- Summarise the findings and give practical recommendations.

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python 3 |
| Data cleaning | pandas, NumPy, re (Google Colab notebook) |
| Database | MySQL (MySQL Workbench) |
| Connectivity | SQLAlchemy / PyMySQL |
| Editor and version control | VS Code, Git, GitHub |

## Repository Structure

```
.
├── data/
│   └── cleaned_earthquakes.csv     # cleaned dataset (121,771 rows, 36 columns)
├── src/
│   ├── load_to_mysql.py            # creates the table and loads the CSV into MySQL
│   ├── queries.py                  # all SQL queries, grouped by theme
│   ├── run_queries.py              # runs the queries and saves each result as a CSV
│   ├── summarize_results.py        # builds a readable results summary
│   └── fix_country.py              # corrects country and continent labels for named earthquakes
├── docs/
│   └── results_summary.txt         # summary of all query results
├── results/                        # one CSV per query
├── notebook/                       # Colab notebook with the cleaning steps
└── README.md
```

## Dataset

- Records: **121,771** earthquake events
- Columns: **36** (after cleaning and feature engineering)
- Period: **2021 to 2026** (2026 is a partial year)
- Key fields: `id`, `time`, `place`, `latitude`, `longitude`, `depth_km`, `mag`, `magType`, `sig`, `tsunami`, `status`, `type`, `net`, `nst`, `gap`, `rms`
- Engineered fields: `country`, `continent`, `mag_category`, `depth_category`, `year`, `month`, `day_of_week`, `hour`

## Methodology

1. **Cleaning (Colab):** I removed duplicates, handled missing values, fixed data types and parsed timestamps.
2. **Feature engineering:** I extracted the country from the `place` text, mapped countries to continents, and created magnitude and depth categories plus time features.
3. **Label correction:** Named events such as "2025 Kamchatka Peninsula, Russia Earthquake" or "Pazarcik earthquake, Kahramanmaras earthquake sequence" were first given wrong country labels. I wrote `src/fix_country.py` to correct them (for example, Alaska and California map to United States, and Kahramanmaras maps to Turkey) and to reassign the continent. The row count stays at 121,771.
4. **Load to MySQL:** `load_to_mysql.py` writes the cleaned CSV to the `earthquakes` table and checks that the MySQL row count matches the CSV.
5. **Analysis:** `queries.py` holds the SQL, `run_queries.py` executes it, and `summarize_results.py` writes `docs/results_summary.txt`.

## How to Run

```bash
# 1. Clone the repo and create a virtual environment
git clone <your-repo-url>
cd <repo-folder>
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt

# 2. Set your MySQL password (PowerShell)
$env:DB_PASSWORD="<your-password>"

# 3. (Only if starting from the unfixed CSV) correct country labels
python src/fix_country.py

# 4. Load data, run queries and summarise
python src/load_to_mysql.py
python src/run_queries.py
python src/summarize_results.py
```

Expected load message: `Rows in MySQL: 121771 | Rows in CSV: 121771`.

## SQL Questions Covered

| Theme | Questions |
|---|---|
| Magnitude and depth | Q1, Q2, Q3, Q5 |
| Time analysis | Q6 to Q10 |
| Impact (significance as a casualty proxy) | Q11, Q13, Q20 |
| Event type and quality | Q14, Q15, Q16, Q18, Q19 |
| Seismic patterns and trends | Q21 to Q24 |
| Depth, location and reliability | Q25 to Q28, Q30 |

## Key Findings

- **Strongest event:** the 2025 Kamchatka Peninsula, Russia earthquake (M8.8). Next were Alaska 2021 (M8.2), South Sandwich Islands 2021 (M8.1) and Kermadec Islands, New Zealand 2021 (M8.1).
- **Shallow and strong:** 16 earthquakes were shallower than 50 km with magnitude above 7.5, including the 2023 Turkey earthquake (M7.8 at 10 km depth).
- **Busiest years:** 2025 had the most events (22,833), followed by 2021 (21,926) and 2023 (20,830). Year-over-year growth in 2025 was +22.37%.
- **Seasonality:** August and July had the most earthquakes, while the day of the week showed almost no meaningful difference.
- **Impact proxy:** the United States (about 4.29M total significance), Indonesia, Japan, Russia and the Philippines rank highest.
- **Most active regions (frequency x average magnitude):** United States, Indonesia and Japan.
- **Deep-focus events (> 300 km):** Fiji dominates with 4,338 events, followed by Tonga, Japan, Indonesia and Timor-Leste, consistent with the Tonga-Fiji subduction zone.
- **Equatorial depth:** the Philippines (about 110 km), Papua New Guinea and Peru have the deepest average depths within 5 degrees of the equator.
- **Tsunamis:** tsunami-associated events average about 1.17 magnitude units higher than the rest (5.42 vs 4.25).
- **Data quality:** 121,589 events are reviewed and 182 are automatic; 865 events are mining explosions.

## Recommendations

- Focus preparedness and building-code enforcement on subduction-zone countries such as Indonesia, Japan, the Philippines, Russia and New Zealand.
- Assess risk using magnitude and depth together, since shallow events above M7.5 are the most dangerous.
- Interpret US counts with care: dense local seismic networks record many small events, which inflates counts.
- Exclude non-earthquake events (mining explosions, ice quakes and similar) from seismic analysis.

## Limitations

- `sig` (significance) is a proxy for impact, not actual casualty data.
- Countries with few seismic stations (remote islands) show high average magnitudes (Q21) because small events go undetected.
- Shallow-to-deep ratios (Q26) can be inflated when a country has very few deep events.
- 2026 is a partial year, so it should not be compared directly with full years.
- A small number of events without a clear country in `place` (open ocean, ridges) are grouped under `Ocean/Other`.
