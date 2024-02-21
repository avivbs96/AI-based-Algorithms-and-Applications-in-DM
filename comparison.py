import matplotlib.pyplot as plt
import ast

def read_times_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Find the line with segment times
        for line in lines:
            if line.startswith("a_star Segment times:") or line.startswith("dijkstra Segment times:"):
                # Use ast.literal_eval to safely convert string representation of list to a list
                segment_times = ast.literal_eval(line.split(': ')[1])
                return segment_times
    return []

# Reading segment times from the output files
a_star_times = read_times_from_file('a_star_output.txt')
dijkstra_times = read_times_from_file('dijkstra_output.txt')

# Assuming each step represents a pathfinding operation from one waypoint to the next
steps = range(1, len(a_star_times) + 1)

plt.figure(figsize=(12, 7))
plt.plot(steps, a_star_times, label='A* (Heuristic, Approximate)', marker='o', linestyle='-', color='blue')
plt.plot(steps, dijkstra_times, label='Dijkstra (Exact, Optimal)', marker='s', linestyle='--', color='red')

plt.title('A* vs Dijkstra Pathfinding Performance')
plt.xlabel('Pathfinding Step')
plt.ylabel('Time Taken (seconds)')
plt.xticks(steps)
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Adding annotations for minimum A* time and maximum Dijkstra time
min_a_star_time_index = a_star_times.index(min(a_star_times)) + 1  # Adding 1 for 1-based indexing in the graph
max_dijkstra_time_index = dijkstra_times.index(max(dijkstra_times)) + 1  # Adding 1 for 1-based indexing

plt.annotate('Fastest A*', xy=(min_a_star_time_index, min(a_star_times)),
             xytext=(min_a_star_time_index - 1, max(a_star_times) + 0.02), arrowprops=dict(facecolor='blue', shrink=0.05))

plt.annotate('Slowest Dijkstra', xy=(max_dijkstra_time_index, max(dijkstra_times)),
             xytext=(max_dijkstra_time_index - 1, max(dijkstra_times) + 0.05), arrowprops=dict(facecolor='red', shrink=0.05))

plt.tight_layout()

# Display the plot
plt.show()
