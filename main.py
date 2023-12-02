import random
import math
import heapq
import tkinter as tk

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

    min_distances = heapq.nsmallest(k, ((euclidean_distance(Point(x, y, ""), point), point.color) for point in
                                        training_data))

    # Count the occurrences of each color in the k nearest neighbors
    color_counts = {'red': 0, 'green': 0, 'blue': 0, 'purple': 0}
    for distance, color in min_distances:
        color_counts[color] += 1

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
                if random.randint(1, 100) > 1:
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
                if random.randint(1, 100) > 1:
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
                if random.randint(1, 100) > 1:
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
                if random.randint(1, 100) > 1:
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

def classify_point(color, color_count, color_list, color_index, k):
    global errors

    if color_count < len(color_list[color_index]):
        point = color_list[color_index][color_count]
        x, y = point.x, point.y
        color_count += 1

        new_color = classify(x, y, k)

        if new_color != color:
            errors += 1

    return color_count

def plot_points(classified_data):
    root = tk.Tk()
    canvas_width = 800
    canvas_height = 800
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Find the range of x and y coordinates
    min_x = min(point.x for point in classified_data)
    max_x = max(point.x for point in classified_data)
    min_y = min(point.y for point in classified_data)
    max_y = max(point.y for point in classified_data)

    # Calculate the scale factors for x and y
    scale_factor_x = canvas_width / (max_x - min_x)
    scale_factor_y = canvas_height / (max_y - min_y)

    for point in classified_data:
        x, y, color = point.x, point.y, point.color

        # Scale down the coordinates for visibility
        x_scaled = (x - min_x) * scale_factor_x
        y_scaled = (y - min_y) * scale_factor_y

        # Adjust the size and position of the ovals
        oval_size = 20
        canvas.create_oval(x_scaled - oval_size, y_scaled - oval_size, x_scaled + oval_size, y_scaled + oval_size, fill=color, outline=color)

    root.mainloop()

if __name__ == "__main__":
    NUMBER = 10000
    generate_points(NUMBER)
    print("generated")

    for i in range(4):
        k_values = [1, 3, 7, 15]
        for k in k_values:
            errors = 0
            training_data = [Point(x, y, color) for color, coordinates in starting_points.items() for x, y in coordinates]
            classified_data = [Point(x, y, color) for color, coordinates in starting_points.items() for x, y in coordinates]

            color_counts = {'red': 0, 'green': 0, 'blue': 0, 'purple': 0}
            color_list = {'red': red, 'green': green, 'blue': blue, 'purple': purple}

            while not all(count == NUMBER for count in color_counts.values()):
                color = random.choice(['red', 'green', 'blue', 'purple'])
                color_counts[color] = classify_point(color, color_counts[color], color_list, color, k)

            print("Errors for k =", k, ":", errors)
            print(len(classified_data))
            plot_points(classified_data)
