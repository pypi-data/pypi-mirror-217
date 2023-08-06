Weekshot Lottery Winner Selection
====

## GitHub

[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/Weekshot/weekshot-lottery-winner-selection?label=latest%20stable&sort=semver&style=for-the-badge)](https://github.com/Weekshot/weekshot-lottery-winner-selection/releases)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Weekshot/weekshot-lottery-winner-selection?label=latest%20unstable&style=for-the-badge)](https://github.com/Weekshot/weekshot-lottery-winner-selection/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/Weekshot/weekshot-lottery-winner-selection?style=for-the-badge)](https://github.com/Weekshot/weekshot-lottery-winner-selection/commits/master)

## PyPI

[![PyPI - Version](https://img.shields.io/pypi/v/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)
[![PyPI - Python Wheel](https://img.shields.io/pypi/wheel/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)
[![PyPI - Format](https://img.shields.io/pypi/format/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)
[![PyPI - Status](https://img.shields.io/pypi/status/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)
[![PyPI - Downloads](https://img.shields.io/pypi/dd/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)
[![PyPI - License](https://img.shields.io/pypi/l/weekshot-lottery-winner-selection?style=for-the-badge)](https://pypi.org/project/weekshot-lottery-winner-selection/)


## Installation

```
pip install weekshot_lottery_winner_selection
```

or

```
poetry add async-casbin-weekshot_lottery_winner_selection-adapter
```

## Simple Example

```python
# Stdlib:
import asyncio

# Thirdparty:
from weekshot_lottery_winner_selection import generate_random_numbers


async def main():
    numbers = await generate_random_numbers(
        api_key="RANDOM_ORG_API_KEY",
        max_number=200,
        count=5,
    )

    print(numbers)


asyncio.run(main())
```

### License

This project is licensed under the [MIT license](LICENSE).