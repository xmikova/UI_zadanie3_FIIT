import random
from collections import Counter
import math
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def classify(x, y, k, training_data):
    new_point = Point(x, y, "")

    distances = [(calculate_distance(new_point, point), point.color) for point in training_data]

    k_nearest_neighbors = sorted(distances)[:k]

    class_counts = Counter(neigh[1] for neigh in k_nearest_neighbors)

    most_common_class = class_counts.most_common(1)[0][0]

    return most_common_class


def generate_starting_points(color, coordinates):
    return [Point(x, y, color) for x, y in coordinates]


# Define starting points for each class
starting_points = {
    'R': [(-4500, -4400), (-4100, -3000), (-1800, -2400), (-2500, -3400), (-2000, -1400)],
    'G': [(4500, -4400), (4100, -3000), (1800, -2400), (2500, -3400), (2000, -1400)],
    'B': [(-4500, 4400), (-4100, 3000), (-1800, 2400), (-2500, 3400), (-2000, 1400)],
    'P': [(4500, 4400), (4100, 3000), (1800, 2400), (2500, 3400), (2000, 1400)]
}

# Generate starting points for each class
starting_points = {class_: generate_starting_points(class_, coordinates) for class_, coordinates in
                   starting_points.items()}


def create_new_points_random(number_of_points_per_color):
    points = []
    colors = ['R', 'G', 'B', 'P']

    for _ in range(number_of_points_per_color):
        for color in colors:
            unique_point = None

            while unique_point is None:
                if color == 'R':
                    x = random.randint(-5000, 500)
                    y = random.randint(-5000, 500)
                    if random.random() < 0.01:
                        while x < 500 and y < 500:
                            x = random.randint(-5000, 5000)
                            y = random.randint(-5000, 5000)
                elif color == 'G':
                    x = random.randint(-500, 5000)
                    y = random.randint(-5000, 500)
                    if random.random() < 0.01:
                        while x > -500 and y < 500:
                            x = random.randint(-5000, 5000)
                            y = random.randint(-5000, 5000)
                elif color == 'B':
                    x = random.randint(-5000, 500)
                    y = random.randint(-500, 5000)
                    if random.random() < 0.01:
                        while x < 500 and y > -500:
                            x = random.randint(-5000, 5000)
                            y = random.randint(-5000, 5000)
                else:
                    x = random.randint(-500, 5000)
                    y = random.randint(-500, 5000)
                    if random.random() < 0.01:
                        while x > -500 and y > -500:
                            x = random.randint(-5000, 5000)
                            y = random.randint(-5000, 5000)

                point = Point(x, y, color)

                # Check if the point is unique before adding it
                if point not in points:
                    unique_point = point

            points.append(unique_point)

    return points


# Set parameters
NUMBER_PER_COLOR = 1000

# Generate points using the specified distribution
new_points = create_new_points_random(NUMBER_PER_COLOR)

# Plot the generated points
plt.figure(figsize=(10, 10))

# Mapping of class names to colors
color_mapping = {'R': 'red', 'G': 'green', 'B': 'blue', 'P': 'purple'}


training_data = starting_points['R'] + starting_points['G'] + starting_points['B'] + starting_points['P'] + new_points

k_value = 3  # Replace with the desired k value

# Apply classify function to each point in the generated list
classified_points = [(point.x, point.y, classify(point.x, point.y, k_value, training_data)) for point in training_data]

# Print the classified points
for x, y, color in classified_points:
    print(f"Point at ({x}, {y}) is classified as: {color}")

# Plot the classified points
plt.figure(figsize=(10, 10))
for x, y, color in classified_points:
    plt.scatter(x, y, c=color_mapping[color], marker='.', s=500)

plt.title('Classified Points')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()