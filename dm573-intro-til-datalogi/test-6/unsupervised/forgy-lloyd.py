def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def forgy_lloyd_kmeans(dataset, K, max_iterations=100, tolerance=1e-6):
    """
    K-means clustering using Forgy-Lloyd algorithm.

    Args:
        dataset: List of tuples (x, y, label) where label is initial cluster assignment
        K: Number of clusters
        max_iterations: Maximum number of iterations
        tolerance: Convergence threshold for centroid movement

    Returns:
        clusters: Dictionary mapping cluster name to list of points
        centroids: Dictionary mapping cluster name to centroid coordinates
        iterations: Number of iterations performed
    """
    # Extract points and initial labels
    points = [(x, y) for x, y, _ in dataset]
    initial_labels = [label for _, _, label in dataset]

    # Initialize centroids using Forgy method (random selection from data points)
    # For simplicity, we'll use the first K unique points
    unique_labels = list(set(initial_labels))

    # Group points by their initial labels
    label_groups = {}
    for i, label in enumerate(initial_labels):
        if label not in label_groups:
            label_groups[label] = []
        label_groups[label].append(points[i])

    # Get cluster names (first K unique labels)
    cluster_names = list(label_groups.keys())[:K]

    # If we need more cluster names, generate them
    name_counter = 1
    while len(cluster_names) < K:
        new_name = f"Cluster_{name_counter}"
        if new_name not in cluster_names:
            cluster_names.append(new_name)
        name_counter += 1

    # Initialize centroids as means of initial label groups
    centroids = {}
    for i, cluster_name in enumerate(cluster_names):
        if cluster_name in label_groups:
            group = label_groups[cluster_name]
            centroid_x = sum(p[0] for p in group) / len(group)
            centroid_y = sum(p[1] for p in group) / len(group)
            centroids[cluster_name] = (centroid_x, centroid_y)
        else:
            # Use a point from the dataset if no initial group exists
            centroids[cluster_name] = points[i % len(points)]

    # Lloyd's algorithm iterations
    clusters = {name: [] for name in cluster_names}
    iteration = 0

    for iteration in range(max_iterations):
        # Assignment step: assign each point to nearest centroid
        clusters = {name: [] for name in cluster_names}

        for point in points:
            distances = [euclidean_distance(point, centroids[name]) for name in cluster_names]
            nearest_cluster = cluster_names[distances.index(min(distances))]
            clusters[nearest_cluster].append(point)

        # Update step: recalculate centroids
        new_centroids = {}
        for cluster_name in cluster_names:
            if clusters[cluster_name]:  # If cluster is not empty
                centroid_x = sum(p[0] for p in clusters[cluster_name]) / len(clusters[cluster_name])
                centroid_y = sum(p[1] for p in clusters[cluster_name]) / len(clusters[cluster_name])
                new_centroids[cluster_name] = (centroid_x, centroid_y)
            else:
                # Keep old centroid if cluster is empty
                new_centroids[cluster_name] = centroids[cluster_name]

        # Check for convergence
        max_movement = max(euclidean_distance(centroids[name], new_centroids[name])
                          for name in cluster_names)

        centroids = new_centroids

        if max_movement < tolerance:
            print(f"Converged after {iteration + 1} iterations")
            break
    else:
        print(f"Reached maximum iterations ({max_iterations})")

    return clusters, centroids, iteration + 1

def calculate_td_squared(clusters, centroids):
    """
    Calculate TD² (Total Distance Squared) - sum of squared distances
    from each point to its cluster centroid.

    Args:
        clusters: Dictionary mapping cluster names to lists of points
        centroids: Dictionary mapping cluster names to centroid coordinates

    Returns:
        td_squared: The TD² value
    """
    td_squared = 0.0
    for cluster_name, cluster_points in clusters.items():
        centroid = centroids[cluster_name]
        for point in cluster_points:
            distance = euclidean_distance(point, centroid)
            td_squared += distance ** 2
    return td_squared

# Example usage
if __name__ == "__main__":
    # Your dataset
    dataset = [
        (1,5,"S"),
        (2,3,"S"),
        (3,4,"T"),
        (6,8,"C"),
        (7,7,"T"),
        (7,8,"C"),
        (7,9,"C"),
        (10,1,"T")
    ]

    K = 3  # Number of clusters

    print("Dataset:", dataset)
    print(f"K = {K}\n")

    clusters, centroids, iterations = forgy_lloyd_kmeans(dataset, K)

    td_squared = calculate_td_squared(clusters, centroids)

    print(f"Final centroids:")
    for cluster_name, centroid in centroids.items():
        print(f"  Cluster {cluster_name}: {centroid}")

    print(f"\nFinal clusters:")
    for cluster_name, cluster_points in clusters.items():
        print(f"  Cluster {cluster_name}: {cluster_points}")

    print(f"\nIterations: {iterations}")
    print(f"TD² (Total Distance Squared): {td_squared:.4f}")
