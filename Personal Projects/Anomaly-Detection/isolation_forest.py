import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt


# Function to generate synthetic data with anomalies
def generate_synthetic_data(num_normal_points=1000, num_anomalies=50):
    np.random.seed(42)

    # Generate normal data from a Gaussian distribution
    normal_data = np.random.normal(loc=0, scale=1, size=(num_normal_points, 2))

    # Generate anomalies by adding outliers
    anomalies = np.random.uniform(low=-10, high=10, size=(num_anomalies, 2))

    # Combine normal and anomaly data
    data = np.vstack([normal_data, anomalies])

    return pd.DataFrame(data, columns=["Feature1", "Feature2"])


# Function to visualize the data and anomalies
def plot_data_with_anomalies(data, anomalies):
    plt.scatter(data["Feature1"], data["Feature2"], label="Normal Data", alpha=0.8)
    plt.scatter(
        anomalies["Feature1"], anomalies["Feature2"], label="Anomalies", color="red"
    )
    plt.title("Synthetic Data with Anomalies")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()


# Function to apply Isolation Forest and visualize results
def apply_isolation_forest(data, contamination=0.05):
    # Fit Isolation Forest model
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(data)

    # Predict anomalies
    data["Anomaly"] = model.predict(data)

    # Separate anomalies and normal data
    anomalies = data[data["Anomaly"] == -1].drop("Anomaly", axis=1)
    normal_data = data[data["Anomaly"] == 1].drop("Anomaly", axis=1)

    return normal_data, anomalies


# Generate synthetic data with anomalies
synthetic_data = generate_synthetic_data()

# Visualize the data with anomalies
plot_data_with_anomalies(
    synthetic_data, synthetic_data.loc[synthetic_data.index[-50:], :]
)

# Apply Isolation Forest and visualize results
normal_data, detected_anomalies = apply_isolation_forest(
    synthetic_data, contamination=0.05
)

# Visualize the results
plot_data_with_anomalies(normal_data, detected_anomalies)
