import sys
import yaml
import jinja2


def yml_load(x):
    try:
        with open(x) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print(str(e) + '\nCreate a "vpws.yml" file in the current working directoy.'
                       '\nOr specify the path to your .yml file with the "-c" option')
        sys.exit(0)


def jinja2_load(filename):
    with open(filename) as t:
        return jinja2.Template(t.read())