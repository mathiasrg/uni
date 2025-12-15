def first_fit(items, bin_capacity):
    bins = []

    for item_id, item_size in enumerate(items):
        placed = False
        for bin_idx, bin_items in enumerate(bins):
            bin_usage = sum(size for _, size in bin_items)

            if bin_usage + item_size <= bin_capacity:
                bin_items.append((item_id, item_size))
                placed = True
                break

        if not placed:
            bins.append([(item_id, item_size)])

    return bins, len(bins)


def print_bins(bins, bin_capacity):
    """Print the bin packing result in a readable format."""
    print(f"Bin capacity: {bin_capacity}")
    print(f"Number of bins used: {len(bins)}\n")

    for bin_idx, bin_items in enumerate(bins):
        total = sum(size for _, size in bin_items)
        items_str = ", ".join([f"item{item_id}({size})" for item_id, size in bin_items])
        print(f"Bin {bin_idx}: [{items_str}] -> Total: {total}/{bin_capacity}")


items1 = [0.7, 0.3, 0.5, 0.6, 0.4, 0.2, 0.8]
bin_capacity1 = 1.0

print("Example 1:")
bins1, num_bins1 = first_fit(items1, bin_capacity1)
print_bins(bins1, bin_capacity1)

print("\n" + "="*60 + "\n")
