from jinja2 import Environment, PackageLoader, select_autoescape


def render(day: dict, kind: str = "dummy"):
    env = Environment(loader=PackageLoader("workshop_schedules"), autoescape=select_autoescape())

    template = env.get_template(f"{kind}.tpl")

    print(template.render(days=[day]))
