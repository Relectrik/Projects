from datasets import load_dataset as ld
import pandas as pd
from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest as IF
import re

league_dataset = ld("Arconte/league_of_legends_wiki_scrape")

league_dataset = pd.DataFrame(league_dataset["train"])

selected_features = ["stats"]
scatterplot_data = league_dataset[selected_features]

for index, row in scatterplot_data.iterrows():
    print(row["stats"])


def extract_health_armor(stats_string):
    # Use regular expressions to find health and armor values
    health_match = re.search(r"health: Health(\d+)\+(\d+)", stats_string)
    armor_match = re.search(r"armor: Armor(\d+)\+(\d+\.\d+)", stats_string)

    # Extracting the matched values
    if health_match and armor_match:
        health_base = int(health_match.group(1))
        armor_base = int(armor_match.group(1))
        return {
            "health_base": health_base,
            "armor_base": armor_base,
        }
    else:
        return None


extracted_data = pd.DataFrame()

extracted_data[["health_base", "armor_base"]] = (
    league_dataset["stats"].apply(extract_health_armor).apply(pd.Series)
)

print(extracted_data)

metadata = SingleTableMetadata()
metadata.detect_from_dataframe(extracted_data)

synthesizer = SingleTablePreset(metadata, name="FAST_ML")
synthesizer.fit(extracted_data)

synthetic_data = synthesizer.sample(num_rows=len(extracted_data))

num_anomalies = int(0.05 * len(extracted_data))  # 5% of data as anomalies
random_indices = np.random.choice(len(extracted_data), num_anomalies, replace=False)
synthetic_data.loc[
    random_indices, "health_base"
] += 60  # Increase health value for anomalies

print("Original Data:")
print(extracted_data)

print("\nSynthetic Data with Anomalies:")
print(synthetic_data)

plt.scatter(
    extracted_data["health_base"],
    extracted_data["armor_base"],
    label="Original Data",
)
plt.scatter(
    synthetic_data["health_base"],
    synthetic_data["armor_base"],
    label="Synthetic Data with Anomalies",
    alpha=0.5,
)

plt.xlabel("Health")
plt.ylabel("Armor")
plt.legend()
plt.title("Scatterplot of Original and Synthetic Data with Anomalies")

plt.show()
