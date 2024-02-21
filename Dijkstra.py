from pathfinding_common import *
import heapq
import time

# Aviv Ben Shitrit , id 313357766
def dijkstra_search(graph, start, goal):
    start_time = time.time()  # Start timing
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while frontier:
        current_cost, current = heapq.heappop(frontier)
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                heapq.heappush(frontier, (new_cost, next))
                came_from[next] = current

    end_time = time.time()
    print(f"dijkstra Path found from {start} to {goal} in {end_time - start_time:.4f} seconds")
    return came_from, cost_so_far

# Initialization and pathfinding execution
grid = initialize_grid_and_obstacles(300,100)
waypoints = generate_waypoints((0, 0), (99, 99), 10, 100)
complete_path, segment_times, total_search_time = run_pathfinding_algorithm(grid, waypoints, dijkstra_search)

print("dijkstra Segment times:", segment_times)
print(f"dijkstra Total search time: {total_search_time:.4f} seconds")

content = [
    f"dijkstra Segment times: {segment_times}",
    f"dijkstra Total search time: {total_search_time:.4f} seconds"
]

path_validity = "Path is valid." if is_path_valid(complete_path, grid.obstacles) else "Path is not valid."
print(path_validity)
content.append(path_validity)

with open('./dijkstra_output.txt', 'w') as file:
    for line in content:
        file.write(line + '\n')

visualize_path(complete_path, waypoints, grid.obstacles, total_search_time, "Dijkstra's Algorithm Visualization: 10 Waypoints, 100 Obstacles, 100x100 Grid Size")
