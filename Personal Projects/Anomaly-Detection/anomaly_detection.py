from datasets import load_dataset as ld
import pandas as pd
from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import re

# Load LoL dataset from HuggingFace
league_dataset: Dataset = ld("Arconte/league_of_legends_wiki_scrape")
league_dataset: pd.DataFrame = pd.DataFrame(league_dataset["train"])


# Extract useful stats for use in our project (in our case, health and armor)
def extract_health_armor(stats_string) -> dict[str, int]:
    """
    Extracts the useful stats that we need from the data.

    Args:
        stats_string str: String holding the relevant stats we need in the format:
        "health: Health590+96, resource: Mana418+25, health regen: Health regen. (per..."

    Returns:
        dict[str, int]: Dictionary mapping of health and armor to their corresponding values in game.
    """
    # Use regular expressions to find health and armor values
    health_match: str = re.search(r"health: Health(\d+)\+(\d+)", stats_string)
    armor_match: str = re.search(r"armor: Armor(\d+)\+(\d+\.\d+)", stats_string)

    # Extracting the matched values
    if health_match and armor_match:
        health_base: int = int(health_match.group(1))
        armor_base: int = int(armor_match.group(1))
        return {
            "health_base": health_base,
            "armor_base": armor_base,
        }
    else:
        return None


# Put extracted data into a dataframe
extracted_data: pd.DataFrame = pd.DataFrame()
extracted_data[["health_base", "armor_base"]] = (
    league_dataset["stats"].apply(extract_health_armor).apply(pd.Series)
)

# Drop any NaN values in the dataframe
extracted_data = extracted_data.dropna()

# Capture metadata, and synthesize new data based on old data
metadata: SingleTableMetadata = SingleTableMetadata()
metadata.detect_from_dataframe(extracted_data)
synthesizer: SingleTablePreset = SingleTablePreset(metadata, name="FAST_ML")
synthesizer.fit(extracted_data)
synthetic_data: pd.DataFrame = synthesizer.sample(num_rows=len(extracted_data))

# Intrdouce anomalies by incrememnting 5% of the dataset by some arbritrary value (50 in this case)
num_anomalies: int = int(0.05 * (len(synthetic_data)))
synthetic_data.iloc[
    -num_anomalies:, synthetic_data.columns.get_loc("health_base")
] += 50
synthetic_data.iloc[
    -num_anomalies:, synthetic_data.columns.get_loc("health_base")
] += 50
#

print("Original Data:")
print(extracted_data)

print("\nSynthetic Data with Anomalies:")
print(synthetic_data)

def apply_isolation_forest(data, contamination=0.05) -> pd.DataFrame:
    """
    Apply Isolation Forest to the data to return a dataframe of normal data and anomalies.

    Args:
        data (pd.dataframe): Dataframe holding raw features as data on a scatterplot.
        contamination (float, optional): Arbitrary contamination rate that can be changed by user. Defaults to 0.05.

    Returns:
        pd.dataframe: data separated into normal data and anomalies.
    """
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(data)

    data["Anomaly"] = model.predict(data)

    anomalies = data[data["Anomaly"] == -1].drop("Anomaly", axis=1)
    normal_data = data[data["Anomaly"] == 1].drop("Anomaly", axis=1)

    return normal_data, anomalies


def plot_data_with_anomalies(data, anomalies, title) -> None:
    """
    Plots data using matplotlib library with anomaly values defined.

    Args:
        data (pd.dataframe): Data to plot
        anomalies (pd.dataframe): Values of anomalies to plot
        title (str): Title of the plot
    """
    plt.scatter(data["health_base"], data["armor_base"], label="Normal Data", alpha=0.8)

    plt.scatter(
        anomalies["health_base"],
        anomalies["armor_base"],
        label="Anomalies",
        color="red",
    )

    plt.title(title)
    plt.xlabel("Health")
    plt.ylabel("Armor")
    plt.legend()
    plt.show()


def plot_data_without_anomalies(data, title):
    """
    Plots data using matplotlib library without anomalies.

    Args:
        data (pd.dataframe): Data to plot
        title (str): Title of the plot
    """
    plt.scatter(data["health_base"], data["armor_base"], label="Normal Data", alpha=0.8)
    plt.title(title)
    plt.xlabel("Health")
    plt.ylabel("Armor")
    plt.legend()
    plt.show()


plot_data_without_anomalies(
    pd.concat([extracted_data, synthetic_data], ignore_index=True),
    "All data including synthetic and introduced anomalies",
)

plot_data_with_anomalies(
    extracted_data,
    synthetic_data.tail(num_anomalies),
    "All data highlighting introduced anomalies",
)
normal_data, detected_anomalies = apply_isolation_forest(
    synthetic_data, contamination=0.05
)

plot_data_with_anomalies(
    normal_data, detected_anomalies, "All data using isolation forest to detect anomalies"
)

contamination: float = 0.01
for i in range(5):
    normal_data, detected_anomalies = apply_isolation_forest(
        extracted_data, contamination=contamination
    )
    plot_data_with_anomalies(
        normal_data,
        detected_anomalies,
        f"Anomaly detection applied to original data with contamination rate: {contamination}",
    )
    contamination += 0.01
