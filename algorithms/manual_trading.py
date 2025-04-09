# def find_max_product_cycle(graph, start, max_edges=5):
#     max_product = [0]
#     best_path = []

#     def dfs(node, product, path, depth):
#         if depth > max_edges:
#             return

#         if node == start and depth > 0:
#             # valid cycle
#             if product > max_product[0]:
#                 max_product[0] = product
#                 best_path.clear()
#                 best_path.extend(path)

#         for neighbor, weight in graph.get(node, []):
#             dfs(neighbor, product * weight, path + [neighbor], depth + 1)

#     dfs(start, 1.0, [], 0)
    # return max_product[0] * 500, best_path
    
def find_best_path(graph, start):
    '''
    Brute force strategy
    '''
    nodes = graph.keys()
    route_list = [([start], 1)]
    
    for i in range(4): # number of steps
        new_routes = []
        while route_list:
            route = route_list.pop()
            for node in nodes:
                new_multiplier = route[1] * graph[route[0][-1]][node]
                new_route = route[0] + [node]
                new_routes.append((new_route, new_multiplier))
        
        route_list = new_routes
    
    for i in range(len(route_list)):
        path, multiplier = route_list[i]
        path = path + [start]
        multiplier *= (graph[path[-2]][start] * 500)
        route_list[i] = (path, round(multiplier, 2))
        print((path, round(multiplier, 2)))
        
    max_path, max_multiplier = max(route_list, key=lambda x : x[1])
    
    return max_path, max_multiplier

def main():
    exchange_rates = {
    "Snowballs": {
        "Snowballs": 1,
        "Pizza's": 1.45,
        "Silicon Nuggets": 0.52,
        "SeaShells": 0.72
    },
    "Pizza's": {
        "Snowballs": 0.7,
        "Pizza's": 1,
        "Silicon Nuggets": 0.31,
        "SeaShells": 0.48
    },
    "Silicon Nuggets": {
        "Snowballs": 1.95,
        "Pizza's": 3.1,
        "Silicon Nuggets": 1,
        "SeaShells": 1.49
    },
    "SeaShells": {
        "Snowballs": 1.34,
        "Pizza's": 1.98,
        "Silicon Nuggets": 0.64,
        "SeaShells": 1
    }
    }

    path, max_product = find_best_path(exchange_rates, "SeaShells")
    
    print("Multiplier:", max_product)
    print("Path:", path)
    
if __name__ == "__main__":
    main()
