import math
import random
import matplotlib.pyplot as plt
import os

class Fractal(object):
    def __init__(self, vertices, starting_point):
        '''
        Initiates a fractal object
        param: vertices - A list of x,y coordinates that are the vertices for the polygon
        param: starting_point - The starting X,Y coordinate for building the fractal
        '''
        self.vertices = vertices
        self.starting_point = starting_point
        self.fractal_points = []


    def random_vertex(self):
        ''' Returns a random vertex from the list of vertices'''
        return random.choice(self.vertices)


    def midpoint(self, vertex, x, y):
        '''Finds the midpoint between a vertex and the current point'''
        vertex_x, vertex_y = vertex
        return ( (vertex_x+x)/2.0, (vertex_y+y)/2.0 )


    def build_fractal(self, iterations):
        '''The next vertex can be any random vertex'''
        for i in range(0, iterations):

            if i==0:
                start_x, start_y = self.starting_point
                self.fractal_points.append(self.midpoint(self.random_vertex(), start_x, start_y))
            else:
                last_x, last_y = self.fractal_points[-1]
                self.fractal_points.append(self.midpoint(self.random_vertex(), last_x, last_y))


    def build_fractal_restrict_single_history(self, iterations, restrictions=[]):
        '''
        The next vertex selected will not be part of the restrictions list
        example: a restriction of 1 will not allow for the selection of a vertex that has an index of one greater in fractal.vertices
        '''
        for i in range(0, iterations):

            if i==0:
                new_vertex = self.random_vertex()
                start_x, start_y = self.starting_point
                self.fractal_points.append(self.midpoint(new_vertex, start_x, start_y))

            else:
                #new_vertex = self.random_vertex()
                last_index = self.vertices.index(last_vertex)
                temp_restrictions = list(restrictions)
                temp_vertices = list(self.vertices)

                temp_restrictions = [(restriction + last_index) % len(self.vertices) for restriction in temp_restrictions]
                temp_vertices = [vertex for idx, vertex in enumerate(temp_vertices) if idx not in temp_restrictions]

                new_vertex = random.choice(temp_vertices)
                last_x, last_y = self.fractal_points[-1]
                self.fractal_points.append(self.midpoint(new_vertex, last_x, last_y))

            last_vertex = new_vertex


    def build_fractal_restrict_multiple_history(self, iterations, restrictions={}):
        '''
        The next vertex selected will not be contained in the restrictions dictionary
        example:
            dictionary: {0: [1],
                         1: [3]}

            The next vertex will not have an index one greater than the last index.
            The next vertex will not have an index three greater than the second to last index
        '''
        historic_vertices = []

        for i in range(0, iterations):

            # Build a history to the length of restrictions without plotting
            if i < len(restrictions):
                new_vertex = self.random_vertex()
                historic_vertices.insert(0, new_vertex)
                if i == 0:
                    start_x, start_y = self.starting_point
                else:
                    start_x, start_y = historic_vertices[-1]
                self.fractal_points.append(self.midpoint(new_vertex, start_x, start_y))


            else:
                # itterate through restrictions build a list of vertices that are possible to select from
                available_vertices_list = []
                for idx, single_restrictions in restrictions.items():

                    temp_restrictions = list(single_restrictions)
                    temp_vertices = list(self.vertices)
                    historic_vertex = historic_vertices[idx]
                    historic_vertex_index = self.vertices.index(historic_vertex)

                    temp_restrictions = [(restriction + historic_vertex_index) % len(self.vertices) for restriction in temp_restrictions]
                    available_vertices_list.append([vertex for idx, vertex in enumerate(temp_vertices) if idx not in temp_restrictions])

                available_vertices = list(set.intersection(*map(set, available_vertices_list)))

                try:
                    new_vertex = random.choice(available_vertices)
                except:
                    #Returns false when restrictions prevent the completion of all iterations
                    return False

                last_x, last_y = self.fractal_points[-1]
                self.fractal_points.append(self.midpoint(new_vertex, last_x, last_y))

                historic_vertices.insert(0, new_vertex)
                historic_vertices.pop()
        return True


    def plot_vertices(self):
        '''Plots the vertices as squares'''
        x = [point[0] for point in self.vertices]
        y = [point[1] for point in self.vertices]
        plt.scatter(x,y, s= 100, marker='s')
        plt.show()


    def plot_fractal(self, save=False, name=None, folder=None):
        ''' plots the fractal '''
        x = [point[0] for point in self.vertices]
        y = [point[1] for point in self.vertices]
        plt.figure()
        plt.scatter(x,y, s = 50, c='black', marker='s')

        fractal_points_x = [point[0] for point in self.fractal_points]
        fractal_points_y = [point[1] for point in self.fractal_points]
        plt.plot(fractal_points_x, fractal_points_y, markersize=.25, color='black', marker=',', linewidth=0)

        plt.xticks([])
        plt.yticks([])

        if folder:
            cwd = os.getcwd()
            path = folder + '/' + str(name) + ".png"
        else:
            path = str(name) + ".png"

        if save:
            plt.savefig(path, dpi=400)
            plt.close()
        else:
            plt.show()

def create_polygon_vertices(degree, center_point=None, radius=None):
    '''Returns the vertices for a n degree polynomial with the specified centerpoint and radius'''
    if not center_point:
        center_point = (100, 100)
    if not radius:
        radius = 100

    theta = (-1*2*math.pi)/(2*degree)
    vertices = []
    for i in range(0,degree):
        x = radius*math.sin(theta)
        y = radius*math.cos(theta)

        vertices.append((center_point[0]+x, center_point[1]+y))
        theta = theta + 2*math.pi/degree

    return vertices


def name_from_rules_shape(vertices, rules):
    '''Builds a string name for a fractal that is unique to the rules degree and restrictions'''
    degrees = len(vertices)

    name = str(degrees)
    for key, current_rules in rules.items():
        rules_id = [0 for i in range(0, degrees)]

        for idx, place in enumerate(rules_id):
            if idx in current_rules:
                rules_id[idx] = 1

        name = name + '_' + ''.join(map(str,rules_id))

    return name


def build_single_restriction(vertices):
    '''
    Creates a list of restrictions for a single history chaos game
    param: vertices - A list of vertices
    '''
    num = random.randint(0,2**len(vertices) - 1) # subtract 1 to prevent the possibility of restricting all vertices
    binary = bin(num)[2:]
    binary = binary.zfill(len(vertices))

    restrictions = [i for i in range(0, len(vertices))]
    binary = [int(bit) for bit in list(binary)]

    return [restriction for restriction, bit in zip(restrictions, binary) if bit == 1]


def build_multiple_history_restrictions(vertices, p_cont):
    '''
    Creates a dictionary of restrictions for a multiple history chaos game
    param: vertices - A list of vertices.
    param: p_cont - The probability that the rule creator will create restrictions for the next level of restrictions.
    '''
    restrictions = {0: []}

    current_key = 0
    while(p_cont > random.random() or current_key==0):

        restrictions[current_key] = build_single_restriction(vertices)

        current_key += 1

    return restrictions
