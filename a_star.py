from pathfinding_common import *


# Aviv Ben Shitrit , id 313357766
def a_star_search(graph, start, goal, heuristic):
    start_time = time.time()  
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while frontier:
        current = heapq.heappop(frontier)[1]
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)  # usinge heuristic here
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    end_time = time.time() 
    print(f"Path found from {start} to {goal} in {end_time - start_time:.4f} seconds")
    return came_from, cost_so_far

def heuristic(a, b):
    #manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    #euclidean distance
    #return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Initialization and pathfinding execution
grid = initialize_grid_and_obstacles(10,100)
waypoints = generate_waypoints((0, 0), (99, 99), 10, 100)
complete_path, segment_times, total_search_time = run_pathfinding_algorithm(grid, waypoints, a_star_search, heuristic)

print("a_star Segment times:", segment_times)
print(f"a_star Total search time: {total_search_time:.4f} seconds")

content = [
    f"a_star Segment times: " + str(segment_times),
    f"a_star Total search time: {total_search_time:.4f} seconds"
]

path_validity = "Path is valid." if is_path_valid(complete_path, grid.obstacles) else "Path is not valid."
print(path_validity)
content.append(path_validity)

with open('./a_star_output.txt', 'w') as file:
    for line in content:
        file.write(line + '\n')
    
visualize_path(complete_path, waypoints, grid.obstacles, total_search_time,"A* Algorithm Visualization: 10 Waypoints, 100 Obstacles, 100x100 Grid Size")

