# covid19-india-mobility-report

## 1. Background

Google has published aggregated, anonymized mobility data across 6 categories to help covid19 researchers and policymakers. This exploratory data analysis inspects the data to understand how much the mobility in India has changed from pre-lockdown to the end of phase-3 of the lockdown in the worst affected states.

[Google Mobility Data Source](https://www.google.com/covid19/mobility/index.html?hl=en).

The 6 place categories.

**Grocery & pharmacy Mobility** trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.

**Parks Mobility** trends for places like local parks, national parks, public beaches, marinas, dog parks, plazas, and public gardens.

**Transit Stations Mobility** trends for places like public transport hubs such as subway, bus, and train stations.

**Retail & Recreation Mobility** trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.

**Residential Mobility** trends for places of residence.

**Workplaces Mobility** trends for places of work.

The data shows how visitors to (or time spent in) categorized places change compared to the baseline days. A baseline day represents a normal value for that day of the week. The baseline day is the median value from the 5‑week period Jan 3 – Feb 6, 2020.

For each region-category, the baseline isn’t a single value—it’s 7 individual values. The baseline day is the median value from the 5‑week period Jan 3 – Feb 6, 2020.

For each region-category, the baseline isn’t a single value—it’s 7 individual values. The same number of visitors on 2 different days of the week, result in different percentage changes.

India was the 48th country to start a National-level lockdown to control the spread of COVID19, which was extended multiple times. For our analysis we have following phases to look at:

- Pre-lockdown (before 25th March)
- Phase 1 (25 March – 14 April)
- Phase 2 (15 April – 3 May)
- Phase 3 (4 May – 17 May)
- Phase 4 (18 May – 31 May)

As phase-4 is ongoing we do not have the data on it but Google’s raw dataset does contain information from 15th Feb (pre-lockdown) till the end of 3rd lockdown.

## 2. Methodology

Google published mobility data on most of the countries in the world. But as our focus is India, we filter out the rest of the data. Then we apply a state-level cutoff of 5000+ cases (as of 23rd May) to avoid our graphs getting incomprehensible. It gives us 7 worst affected states in India:

- Maharashtra
- Tamil Nadu
- Gujarat
- Delhi
- Rajasthan
- Madhya Pradesh
- Uttar Pradesh

Then we simply plot the data across each of the 6 place categories for all these 7 states in an interactive plotly graph. (available below if you want to play around)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AksChougule/covid19-india-mobility-report/master?filepath=mobility-data.ipynb)

