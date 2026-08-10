#!/usr/bin/env python3
"""Update the profile SVG uptime once per month."""

from __future__ import annotations

import random
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = (ROOT / "assets" / "dark_mode.svg", ROOT / "assets" / "light_mode.svg")
START_DATE = date(2003, 7, 11)
UPTIME_PATTERN = re.compile(
    r'(<tspan class="key">Uptime</tspan>: <tspan class="value">)[^<]+(</tspan>)'
)


def uptime_parts(today: date) -> tuple[int, int]:
    years = today.year - START_DATE.year
    anniversary = START_DATE.replace(year=START_DATE.year + years)
    if anniversary > today:
        years -= 1
        anniversary = START_DATE.replace(year=START_DATE.year + years)
    return years, (today - anniversary).days


def update_svg(path: Path, value: str) -> None:
    content = path.read_text()
    updated, replacements = UPTIME_PATTERN.subn(rf"\g<1>{value}\g<2>", content, count=1)
    if replacements != 1:
        raise RuntimeError(f"Expected one Uptime field in {path}, found {replacements}")
    path.write_text(updated)


def main() -> int:
    today = date.today()
    years, days = uptime_parts(today)
    hours = random.SystemRandom().randrange(24)
    minutes = random.SystemRandom().randrange(60)
    year_label = "year" if years == 1 else "years"
    day_label = "day" if days == 1 else "days"
    hour_label = "hour" if hours == 1 else "hours"
    minute_label = "min" if minutes == 1 else "mins"
    value = (
        f"{years} {year_label}, {days} {day_label}, "
        f"{hours} {hour_label}, {minutes} {minute_label}"
    )

    for asset in ASSETS:
        update_svg(asset, value)

    print(f"Updated Uptime to: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
