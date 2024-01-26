from datasets import load_dataset as ld
import pandas as pd
from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest as IF

wine_dataset = ld("lvwerra/red-wine")

wine_dataset = pd.DataFrame(wine_dataset["train"])

selected_features = ["alcohol", "residual sugar"]
scatterplot_data = wine_dataset[selected_features]

metadata = SingleTableMetadata()
metadata.detect_from_dataframe(scatterplot_data)

synthesizer = SingleTablePreset(metadata, name="FAST_ML")
synthesizer.fit(scatterplot_data)

synthetic_data = synthesizer.sample(num_rows=len(scatterplot_data))

num_anomalies = int(0.05 * len(scatterplot_data))  # 5% of data as anomalies
random_indices = np.random.choice(len(scatterplot_data), num_anomalies, replace=False)
synthetic_data.loc[
    random_indices, "alcohol"
] += 5  # Increase alcohol content for anomalies

print("Original Data:")
print(scatterplot_data)

print("\nSynthetic Data with Anomalies:")
print(synthetic_data)

plt.scatter(
    scatterplot_data["alcohol"],
    scatterplot_data["residual sugar"],
    label="Original Data",
)
plt.scatter(
    synthetic_data["alcohol"],
    synthetic_data["residual sugar"],
    label="Synthetic Data with Anomalies",
    alpha=0.5,
)

plt.xlabel("Alcohol")
plt.ylabel("Residual Sugar")
plt.legend()
plt.title("Scatterplot of Original and Synthetic Data with Anomalies")

plt.show()
