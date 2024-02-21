# pathfinding_common.py
import numpy as np
import heapq
import random
import pygame
import sys
import time
import math


def heuristic(a, b):
    #manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    #euclidean distance
    #return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

class GridWithWeights:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.weights = {}
        self.obstacles = set()

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.obstacles

    def neighbors(self, id):
        (x, y) = id
        neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        return [neighbor for neighbor in neighbors if self.in_bounds(neighbor) and self.passable(neighbor)]

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current)
    path.append(start)
    path.reverse()
    return path

def is_path_valid(path, obstacles):
    for i in range(len(path) - 1):
        current, next_node = path[i], path[i + 1]
        if not (current in obstacles or next_node in obstacles):
            if abs(current[0] - next_node[0]) > 1 or abs(current[1] - next_node[1]) > 1:
                return False
    return True


cell_size = 10
grid_size = 100
screen_size = grid_size * cell_size
screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def draw_grid(path, obstacles, waypoints, forward_path):
    for y in range(grid_size):
        for x in range(grid_size):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            if (x, y) in path:
                if (x, y) in forward_path and (x, y) != forward_path[-1]:
                    pygame.draw.rect(screen, GREEN, rect)
                else:
                    pygame.draw.rect(screen, BLUE, rect)  # Path color
            elif (x, y) in obstacles:
                pygame.draw.rect(screen, BLACK, rect)  # Obstacle color
            elif (x, y) in waypoints or (x, y) == waypoints[0] or (x, y) == waypoints[-1]:
                # Increased circle radius for waypoints and changed color to magenta
                pygame.draw.circle(screen, (255, 0, 255), (x*cell_size + cell_size//2, y*cell_size + cell_size//2), cell_size//2 + 5)
            else:
                pygame.draw.rect(screen, WHITE, rect, 1)  # Grid color
                
def initialize_grid_and_obstacles(obstacle_count, grid_size):
    grid = GridWithWeights(grid_size, grid_size)
    for _ in range(obstacle_count):
        x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        grid.obstacles.add((x, y))
    return grid                

# def reordering_waypoints(start, goal, waypoint_count, grid_size):   
#     random_waypoints = [(random.randint(0, grid_size-1), random.randint(0, grid_size-1)) for _ in range(waypoint_count)]
#     waypoints_with_distance = [(waypoint, heuristic(start, waypoint)) for waypoint in random_waypoints]
#     sorted_waypoints = sorted(waypoints_with_distance, key=lambda x: x[1])
#     reordered_waypoints = [waypoint for waypoint, _ in sorted_waypoints]
#     waypoints = [start] + reordered_waypoints + [goal]
#     return waypoints


def generate_waypoints(start, goal, waypoint_count, grid_size):
    """
    Generate waypoints and reorder them based on proximity to the start.
    Includes the start and goal in the final list of waypoints.
    """
    # Generate random waypoints
    random_waypoints = [(random.randint(0, grid_size-1), random.randint(0, grid_size-1)) for _ in range(waypoint_count)]
    
    # Reorder waypoints based on proximity to the start
    waypoints_with_distance = [(waypoint, heuristic(start, waypoint)) for waypoint in random_waypoints]
    sorted_waypoints = sorted(waypoints_with_distance, key=lambda x: x[1])
    reordered_waypoints = [waypoint for waypoint, _ in sorted_waypoints]
    
    # Include start and goal in the list of waypoints
    waypoints = [start] + reordered_waypoints + [goal]
    return waypoints

def run_pathfinding_algorithm(grid, waypoints, search_algorithm, heuristic=None, visualize=False):
    start_time = time.time()
    complete_path = []
    segment_times = []  # Collect individual segment times
    total_search_time = 0

    for i in range(len(waypoints) - 1):
        start, goal = waypoints[i], waypoints[i + 1]
        segment_start_time = time.time()

        came_from, _ = search_algorithm(grid, start, goal, heuristic) if heuristic else search_algorithm(grid, start, goal)

        segment_end_time = time.time()
        segment_time = segment_end_time - segment_start_time
        segment_times.append(segment_time)
        total_search_time += segment_time

        path_segment = reconstruct_path(came_from, start, goal)
        complete_path.extend(path_segment[:-1])  # Exclude goal to prevent duplication

    complete_path.append(waypoints[-1])  # Ensure the final goal is included
    end_time = time.time()

    if visualize:
        # This check allows you to control when visualization occurs
        visualize_path(complete_path, waypoints, grid.obstacles, total_search_time, "Your Algorithm Name")

    return complete_path, segment_times, total_search_time

def visualize_path(complete_path, waypoints, grid_obstacles, total_search_time, search_algorithm_name):
    pygame.init()
    font = pygame.font.Font(None, 24)  # Create a font object
    running = True
    index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        forward_path = complete_path[:index+1]
        draw_grid(complete_path[:index], grid_obstacles, waypoints, forward_path)
        
        # Render the total search time text
        time_text = font.render(f"Total Search Time: {total_search_time:.4f} seconds", True, BLACK)
        screen.blit(time_text, (10, screen_size - 30))  # Position the text on the screen

        # Render the search algorithm name
        algorithm_text = font.render(f"Search Algorithm: {search_algorithm_name}", True, BLACK)
        screen.blit(algorithm_text, (10, screen_size - 60))  # Position the text on the screen
        
        pygame.display.flip()
        clock.tick(50)
        index += 1
        if index >= len(complete_path):
            index = len(complete_path) - 1
    pygame.quit()


    
