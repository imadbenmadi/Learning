import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def generate_fake_data(num_samples=100, num_features=5):
    data = np.random.randn(num_samples, num_features)
    df = pd.DataFrame(data, columns=[f"feature_{i+1}" for i in range(num_features)])
    return df


def process_data(data: pd.DataFrame, export_path: str):
    clean_data(data)
    scaled_data = normalize_data(data)
    principal_components = compute_pca(scaled_data)
    clusters = add_cluster_feature(data, principal_components)
    cluster_summary = compute_cluster_summary(data)
    print(f"Cluster summary:\n{cluster_summary}")
    make_pca_plot(clusters, export_path, principal_components)
    export_data(data, cluster_summary, export_path)
    make_correlation_plot(data, export_path)
    print("Data processing complete")


def make_correlation_plot(data, export_path, figsize=(10, 7)):
    corr_matrix = data.corr()
    print(f"Correlation matrix:\n{corr_matrix}")
    # Visualize correlation matrix
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(f"{export_path}/correlation_matrix.png")
    plt.close()
    print("Correlation matrix plot saved")


def export_data(data, cluster_summary, export_path):
    data.to_csv(f"{export_path}/processed_data.csv", index=False)
    cluster_summary.to_csv(f"{export_path}/cluster_summary.csv")
    print(f"Processed data and cluster summary exported to {export_path}")


def make_pca_plot(clusters, export_path, principal_components, figsize=(10, 7)):
    plt.figure(figsize=figsize)
    plt.scatter(
        principal_components[:, 0],
        principal_components[:, 1],
        c=clusters,
        cmap="viridis",
    )
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of Dataset")
    plt.colorbar()
    plt.savefig(f"{export_path}/pca_clusters.png")
    plt.close()
    print("PCA scatter plot saved")


def compute_cluster_summary(data):
    cluster_summary = data.groupby("Cluster").mean()
    return cluster_summary


def add_cluster_feature(data, principal_components, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(principal_components)
    data["Cluster"] = clusters
    print("Clustering completed")
    return clusters


def compute_pca(scaled_data, n_components=2):
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaled_data)
    print(
        f"PCA completed with explained variance ratio: {pca.explained_variance_ratio_}"
    )
    return principal_components


def normalize_data(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    print("Data normalized")
    return scaled_data


def clean_data(data):
    data.fillna(data.mean(), inplace=True)
    print("Missing values filled")
    data.drop_duplicates(inplace=True)
    print(f"Data shape after removing duplicates: {data.shape}")


def load_data(filepath):
    data = pd.read_csv(filepath)
    print(f"Data loaded with shape: {data.shape}")
    return data


def main():
    data = generate_fake_data(num_samples=1000, num_features=5)
    # data = load_data("path/to/data.csv")

    process_data(data, ".")


if __name__ == "__main__":
    main()
