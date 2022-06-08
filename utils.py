import sys
import yaml
import jinja2


def yml_load(x):
    try:
        with open(x) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print(str(e) + 'The YAML file could not be found')
        sys.exit(0)


def jinja2_load(filename):
    with open(filename) as t:
        return jinja2.Template(t.read())