import cv2
import numpy as np
import heapq

def load_image(path):
    """Load the maze image and convert it to binary."""
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return binary

def find_start_and_end(maze):
    """Find the start and end points in the maze."""
    height, width = maze.shape
    start = None
    end = None

    for x in range(width):
        if maze[0, x] == 255:  # Top row
            start = (0, x)
        elif maze[x,0] == 255:
            start = (x,0)
        if maze[height - 1, x] == 255:  # Bottom row
            end = (height - 1, x)
        elif maze[x,width-1] == 255:
            end = (x,width-1)

    return start, end

def neighbors(maze, node):

    """Get all valid neighbors of a node."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for d in directions:
        new_node = (node[0] + d[0], node[1] + d[1])
        if 0 <= new_node[0] < maze.shape[0] and 0 <= new_node[1] < maze.shape[1]:
            if maze[new_node] == 255:  # Check if walkable
                result.append(new_node)
    return result

def dijkstra(maze, start, end):
    """Find the shortest path using Dijkstra's algorithm."""
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {start: 0}
    previous = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in neighbors(maze, current_node):
            distance = current_distance + 1
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path

def draw_path(maze, path):
    """Draw the path on the maze."""
    thickness = 2  # Width of the path
    for node in path:
        cv2.circle(maze, (node[1], node[0]), thickness, (0, 0, 255), -1)  # Draw circle for wider path
    return maze

def main(image_path, output_path):
    maze = load_image(image_path)
    start, end = find_start_and_end(maze)

    if not start or not end:
        print("Start or end point not found!")
        return

    path = dijkstra(maze, start, end)

    if not path:
        print("No path found!")
        return

    solved_maze = draw_path(cv2.cvtColor(maze, cv2.COLOR_GRAY2BGR), path)
    cv2.imwrite(output_path, solved_maze)
    print(f"Solved maze saved to {output_path}")

if __name__ == "__main__":
    image_path = "maze.jpg"  # Input maze image
    output_path = "solved_maze.jpg"  # Output solved maze
    main(image_path, output_path)
