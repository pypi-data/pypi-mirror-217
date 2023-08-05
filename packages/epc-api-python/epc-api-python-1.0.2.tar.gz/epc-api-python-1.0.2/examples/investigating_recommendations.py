import json
import time

import numpy as np

from epc_api.client import EpcClient

# I have auth_token in my environment
client = EpcClient(version="v1", auth_token="a2Nvbm5rb3dsZXNzYXJAZ21haWwuY29tOjY5MGJiMWM0NmIyOGI5ZDUxYzAxMzQzYzNiZGNlZGJjZDNmODQwMzA=")



# TODO: Do this on a much bigger dataset, e.g. get 10k homes from each constituency

# Let's pull 100 pages
n_pages = 10
page_size = 1000

offset_from = 0
n_completed = 0
results = []
complete = False
while not complete:
    print("Pulling for page %s" % str(int(offset_from/page_size) + 1))
    time.sleep(0.2)
    search_resp = client.domestic.search(params={}, offset_from=offset_from, size=page_size)

    # Note: We can only make 10k queries for a single set of search queries.
    # It might make sense to download data via zip for machine learning since we don't need this
    # data to be perfectly up to date
    if search_resp is None:
        break
    results.extend(search_resp["rows"])
    if n_completed == n_pages:
        complete = True
    else:
        offset_from += page_size

# Testing epc rating
import pandas as pd
import numpy as np
data = pd.DataFrame(results)

columns = ['low-energy-fixed-light-count', 'address', 'uprn-source',
       'floor-height', 'heating-cost-potential', 'unheated-corridor-length',
       'hot-water-cost-potential', 'construction-age-band',
       'potential-energy-rating', 'mainheat-energy-eff', 'windows-env-eff',
       'lighting-energy-eff', 'environment-impact-potential', 'glazed-type',
       'heating-cost-current', 'address3', 'mainheatcont-description',
       'sheating-energy-eff', 'property-type', 'local-authority-label',
       'fixed-lighting-outlets-count', 'energy-tariff',
       'mechanical-ventilation', 'hot-water-cost-current', 'county',
       'postcode', 'solar-water-heating-flag', 'constituency',
       'co2-emissions-potential', 'number-heated-rooms', 'floor-description',
       'energy-consumption-potential', 'local-authority', 'built-form',
       'number-open-fireplaces', 'windows-description', 'glazed-area',
       'inspection-date', 'mains-gas-flag', 'co2-emiss-curr-per-floor-area',
       'address1', 'heat-loss-corridor', 'flat-storey-count',
       'constituency-label', 'roof-energy-eff', 'total-floor-area',
       'building-reference-number', 'environment-impact-current',
       'co2-emissions-current', 'roof-description', 'floor-energy-eff',
       'number-habitable-rooms', 'address2', 'hot-water-env-eff', 'posttown',
       'mainheatc-energy-eff', 'main-fuel', 'lighting-env-eff',
       'windows-energy-eff', 'floor-env-eff', 'sheating-env-eff',
       'lighting-description', 'roof-env-eff', 'walls-energy-eff',
       'photo-supply', 'lighting-cost-potential', 'mainheat-env-eff',
       'multi-glaze-proportion', 'main-heating-controls', 'lodgement-datetime',
       'flat-top-storey', 'current-energy-rating', 'secondheat-description',
       'walls-env-eff', 'transaction-type', 'uprn',
       'current-energy-efficiency', 'energy-consumption-current',
       'mainheat-description', 'lighting-cost-current', 'lodgement-date',
       'extension-count', 'mainheatc-env-eff', 'lmk-key', 'wind-turbine-count',
       'tenure', 'floor-level', 'potential-energy-efficiency',
       'hot-water-energy-eff', 'low-energy-lighting', 'walls-description',
       'hotwater-description']

numrical_columns = ['low-energy-fixed-light-count',
       'floor-height', 'heating-cost-potential', 'unheated-corridor-length',
       'hot-water-cost-potential',
       'environment-impact-potential',
       'heating-cost-current',
       'fixed-lighting-outlets-count',
       'hot-water-cost-current',
       'co2-emissions-potential', 'number-heated-rooms',
       'number-open-fireplaces',
       'co2-emiss-curr-per-floor-area',
       'flat-storey-count',
       'total-floor-area',
       'environment-impact-current',
       'co2-emissions-current',
       'number-habitable-rooms',
       'photo-supply', 'lighting-cost-potential',
       'multi-glaze-proportion',
       'current-energy-efficiency', 'energy-consumption-current',
       'lighting-cost-current',
       'extension-count', 'wind-turbine-count','potential-energy-efficiency', 'low-energy-lighting',
                    ]

str_colums = [c for c in columns if c not in numrical_columns]

for col in numrical_columns:
    # temp
    if all(data[col].unique() == ""):
        continue
    # TEMP - should be filled with a better value e.g. mean, median, or shouldn't be filled at all, not 0
    data[col] = np.where(
        data[col] == "",
        "0.0",
        data[col]
    )
    data[col] = data[col].astype(float)

numerical_data = data[numrical_columns]

response = 'current-energy-efficiency'
cors = numerical_data[numerical_data.columns[1:]].corr()[response][:-1]
cors = cors.sort_values(ascending=False)

# Based on cost of energy,
# i.e. energy required for space heating, water heating and lighting [in kWh/year]
# multiplied by fuel costs. (£/m²/year where cost is derived from kWh).

data["energy-consumption-current"] * data['heating-cost-current'] + \
data[""] * data['hot-water-cost-current'] + \
data['fixed-lighting-outlets-count'] * data['lighting-cost-current']


# Let's get recommendations for these properties
recommendations = []
for i, config in enumerate(results):
    time.sleep(0.01)
    try:
        recs = client.domestic.recommendations(lmk_key=config["lmk-key"])
    except Exception as _:
        print("No recommendations for property %s" % str(i))
        continue
    recommendations.extend(recs["rows"])

# Just ran for 2223 iterations and got 6429 recommendations
# with open("/Users/khalimconn-kowlessar/Documents/hestia/data/recommendations_10th_may.json", "w") as f:
#     json.dump(recommendations, f)

# with open("/Users/khalimconn-kowlessar/Documents/hestia/data/recommendations_10th_may.json", "r") as f:
#     recommendations = json.load(f)

# Let's take a look
import pandas as pd
pd.set_option('display.max_columns', None)
recs = pd.DataFrame(recommendations)

# Recommendation types
rec_types = recs.drop(columns=["lmk-key"]).drop_duplicates()
rec_types = rec_types.sort_values(["improvement-id"], ascending=True)

# We still have duplications due to differing improvement-item
rec_types = rec_types.drop(columns=["improvement-item"]).drop_duplicates()

# We still have duplicates
rec_types = rec_types.drop(columns=["improvement-summary-text", "improvement-descr-text", "improvement-id"]).drop_duplicates()

# We only have 32 unique recommendation id texts in this
# Some recommendation ids have different pricings which indicates that perhaps
# 1) backend is maintaining a database of these works which is changing over time
# 2) Pricings are dependent on the home size/properties, which is the more likely
rec_types["improvement-id-text"].nunique()

# df = pd.DataFrame(search_resp["rows"])
# df = df.sort_values("address")
#
# us = df[df["address"] == "28 Distillery Wharf, Regatta Lane"]
#
# certificate = client.domestic.recommendations(lmk_key=us["lmk-key"].values[0])
#
#
# recommendation_resp = client.domestic.recommendations(lmk_key=search_resp["rows"][0]["lmk-key"])

fields = [
    "roof-description", "walls-description", "floor-description", "windows-description", "glazed-type",
    "multi-glaze-proportion", "glazed-area",
    # Main heating
    "mainheat-description",
    "mainheatcont-description",
    "mainheat-energy-eff",
    "mainheat-env-eff",
    "main-fuel",
    # Hot water
    "hotwater-description",
    "hot-water-energy-eff",
    "hot-water-env-eff",
    # Secondary heating
    "secondheat-description"
]
homes = pd.DataFrame(results)
def make_data_dictionary(fields):
    """
    For the data dictionary, we need to create a hierarchy between what the user currently has and
    what the user should therefore install to improve
    """
    data_dictionary = []
    for field in fields:
        df = pd.DataFrame(
            {
                "field": field,
                "value": homes[field].unique()
            }
        ).sort_values("value", ascending=True)

        data_dictionary.append(df)

    # TODO: Concatenate dictionaries
    #       save as csv


# Pulling data to compare to perse:
resp = client.domestic.search(params={"address": "28 distillery wharf", "postcode": "w6 9bf"}, offset_from=0, size=100)
df = pd.DataFrame(resp["rows"])

# This is the energy consumption in 12 months measured as KWh/m2
energy_consumption = df["energy-consumption-current"].astype(float).values[0]
floor_area = df["total-floor-area"].astype(float).values[0]
kwh_energy_consumption = energy_consumption * floor_area
energy_cost = (0.332 * kwh_energy_consumption)

cert = client.domestic.certificate(lmk_key=df["lmk-key"].values[0])

