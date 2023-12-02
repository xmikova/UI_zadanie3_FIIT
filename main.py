import random
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KDTree

classified_data = []
training_data = []
red = []
green = []
blue = []
purple = []

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.distance = -1

def euclidean_distance(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

def classify(x, y, k):
    global training_data
    global classified_data

    for point in training_data:
        point.distance = euclidean_distance(Point(x, y, ""), point)

    sorted_training_data = sorted(training_data, key=lambda point: point.distance)

    color_counts = {'red': 0, 'green': 0, 'blue': 0, 'purple': 0}
    for point in sorted_training_data[:k]:
        color_counts[point.color] += 1

    new_color = max(color_counts, key=color_counts.get)
    classified_data.append(Point(x, y, new_color))
    training_data.append(Point(x, y, new_color))

    return new_color

def classify_kdtree(x, y, k):
    global training_data
    global classified_data

    # Convert training_data to a numpy array for KD-tree
    training_array = np.array([(point.x, point.y) for point in training_data])

    # Create a KD-tree using the training data
    tree = KDTree(training_array)

    # Query the KD-tree to find the k nearest neighbors
    _, indices = tree.query([(x, y)], k=k)
    neighbors = [training_data[i] for i in indices[0]]

    # Count the occurrences of each color in the neighbors
    color_counts = {'red': 0, 'green': 0, 'blue': 0, 'purple': 0}
    for neighbor in neighbors:
        color_counts[neighbor.color] += 1

    # Determine the most common color
    new_color = max(color_counts, key=color_counts.get)
    classified_data.append(Point(x, y, new_color))
    training_data.append(Point(x, y, new_color))

    return new_color


starting_points = {
    'red': [(-4500, -4400), (-4100, -3000), (-1800, -2400), (-2500, -3400), (-2000, -1400)],
    'green': [(4500, -4400), (4100, -3000), (1800, -2400), (2500, -3400), (2000, -1400)],
    'blue': [(-4500, 4400), (-4100, 3000), (-1800, 2400), (-2500, 3400), (-2000, 1400)],
    'purple': [(4500, 4400), (4100, 3000), (1800, 2400), (2500, 3400), (2000, 1400)]
}

def generate_points(number_of_points_per_color):
    colors = ['red', 'green', 'blue', 'purple']
    global red
    global green
    global blue
    global purple

    for color in colors:
        for _ in range(number_of_points_per_color):
            if color == 'red':
                if random.randint(1,100) > 1:
                    x = random.randint(-5000, 500)
                    y = random.randint(-5000, 500)
                else:
                    while x < 500 and y < 500:
                        x = random.randint(-5000, 5000)
                        y = random.randint(-5000, 5000)

                point = Point(x, y, color)
                if point not in red:
                    unique_point = point
                red.append(unique_point)
            elif color == 'green':
                if random.randint(1,100) > 1:
                    x = random.randint(-500, 5000)
                    y = random.randint(-5000, 500)
                else:
                    while x > -500 and y < 500:
                        x = random.randint(-5000, 5000)
                        y = random.randint(-5000, 5000)

                point = Point(x, y, color)
                if point not in green:
                    unique_point = point
                green.append(unique_point)
            elif color == 'blue':
                if random.randint(1,100) > 1:
                    x = random.randint(-5000, 500)
                    y = random.randint(-500, 5000)
                else:
                    while x < 500 and y > -500:
                        x = random.randint(-5000, 5000)
                        y = random.randint(-5000, 5000)

                point = Point(x, y, color)
                if point not in blue:
                    unique_point = point
                blue.append(unique_point)
            else:
                if random.randint(1,100) > 1:
                    x = random.randint(-500, 5000)
                    y = random.randint(-500, 5000)
                else:
                    while x > -500 and y > -500:
                        x = random.randint(-5000, 5000)
                        y = random.randint(-5000, 5000)

                point = Point(x, y, color)
                if point not in purple:
                    unique_point = point
                purple.append(unique_point)

NUMBER = 100
generate_points(NUMBER)


def classify_point(choice, color, color_count, color_list, color_index):
    global errors

    if color_count < len(color_list[color_index]):
        point = color_list[color_index][color_count]
        x, y = point.x, point.y
        color_count += 1

        if choice == "kdtree":
            new_color = classify_kdtree(x, y, k)
        else:
            new_color = classify(x, y, k)

        if new_color != color:
            errors += 1

    return color_count


k_values = [1, 3, 7, 15]

if __name__ == "__main__":
    for k in k_values:
        choice = "kdtree"
        errors = 0
        training_data = [Point(x, y, color) for color, coordinates in starting_points.items() for x, y in coordinates]
        classified_data = [Point(x, y, color) for color, coordinates in starting_points.items() for x, y in coordinates]

        color_counts = {'red': 0, 'green': 0, 'blue': 0, 'purple': 0}
        color_list = {'red': red, 'green': green, 'blue': blue, 'purple': purple}

        while not all(count == NUMBER for count in color_counts.values()):
            color = random.choice(['red', 'green', 'blue', 'purple'])
            color_counts[color] = classify_point(choice, color, color_counts[color], color_list, color)

        print("Errors for k =", k, ":", errors)

        plt.figure(figsize=(10, 10))
        for point in classified_data:
            plt.scatter(point.x, point.y, c=point.color, marker='o', s=500)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

