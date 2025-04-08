def find_max_product_cycle(graph, start, max_edges=5):
    # Store the maximum log sum found
    max_product = [0]
    best_path = []

    def dfs(node, product, path, depth):
        if depth > max_edges:
            return

        if node == start and depth > 0:
            # valid cycle
            if product > max_product[0]:
                max_product[0] = product
                best_path.clear()
                best_path.extend(path)

        for neighbor, weight in graph.get(node, []):
            dfs(neighbor, product * weight, path + [neighbor], depth + 1)

    dfs(start, 1.0, [], 0)
    return max_product[0] * 500, best_path

def main():
    graph = {
        "Snowballs" : [("Snowballs", 1), ("Pizza's", 1.45), ("Silicon Nuggets", 0.52), ("SeaShells", 0.72)],
        "Pizza's" : [("Snowballs", 0.7), ("Pizza's", 1), ("Silicon Nuggets", 0.31), ("SeaShells", 0.48)],
        "Silicon Nuggets" : [("Snowballs", 1.95), ("Pizza's", 3.1), ("Silicon Nuggets", 1), ("SeaShells", 1.49)],
        "SeaShells" : [("Snowballs", 1.34), ("Pizza's", 1.98), ("Silicon Nuggets", 0.64), ("SeaShells", 1)],
    }
    
    max_product, path = find_max_product_cycle(graph, "SeaShells")
    
    print("Multiplier:", max_product)
    print("Path:", path)
    
if __name__ == "__main__":
    main()
