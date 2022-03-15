from pathlib import Path
from typing import Optional

from jinja2 import Environment, PackageLoader, select_autoescape


def render_day(day: dict, kind: str = "html"):
    env = Environment(loader=PackageLoader("workshop_schedules"), autoescape=select_autoescape())
    template = env.get_template(f"{kind}/day.tpl")
    return template.render(day=day)


def write_day(day: dict, filename: Optional[Path] = None, kind: str = "html"):
    filename = filename or Path(f'day.{kind}')
    filename.write_text(render_day(day=day))
