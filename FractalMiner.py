import yaml
import random
import Fractal


def read_yml(file_name):
    '''
    Param - file_name: Name of the yaml file that contains the configuration values
    Returns: Dictionary of configuration values
    '''
    with open(file_name, 'r') as f:
        yaml_file = yaml.load(f)
    return yaml_file



def main():
    config_data = read_yml("FractalMinerConfig.yml")
    polygon_lower_bound = config_data['polygon_lower_bound']
    polygon_upper_bound = config_data['polygon_upper_bound']
    fractal_path = config_data['fractal_path']
    p_continue = config_data['p_continue']
    iterations = config_data['iterations']

    while True:

        # pick a random polygon between the lower and upper bounds
        random_polygon_size = random.randint(polygon_lower_bound, polygon_upper_bound)
        print(random_polygon_size)

        # build vertices
        vertices = Fractal.create_polygon_vertices(random_polygon_size)

        # create rule and give it a name
        rules = Fractal.build_multiple_history_restrictions(vertices, p_continue)
        print(rules)
        name = Fractal.name_from_rules_shape(vertices, rules)

        # Initiate fractal, build with the rules, and save it
        new_fractal = Fractal.Fractal(vertices, starting_point=(10,10))
        new_fractal.build_fractal_restrict_multiple_history(iterations, rules)
        new_fractal.plot_fractal(save=True, name=name, folder=fractal_path)





if __name__ == "__main__":
    main()
