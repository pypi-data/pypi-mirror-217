import datetime
from typing import NamedTuple

from slugify import slugify

from .category import StatuteSerialCategory


class Rule(NamedTuple):
    """A `Rule` is detected if it matches either a named pattern or a serial pattern.
    Each rule maps to a category and number.
    """  # noqa: E501

    cat: StatuteSerialCategory
    num: str

    def __repr__(self) -> str:
        return f"{self.cat} {self.num}"

    def __str__(self) -> str:
        return self.cat.serialize(self.num) or f"{self.cat.value=} {self.num=}"

    @property
    def slug(self) -> str:
        return slugify(
            " ".join([self.cat.value, self.num.lower()]), separator="_", lowercase=True
        )

    @property
    def serial_title(self):
        return StatuteSerialCategory(self.cat.value).serialize(self.num)


class RuleOption(NamedTuple):
    """Used for dated extractions on Named Patterns, e.g. if
    a document is dated 1940-01-01, and a match for a NamedPattern
    exists for the Civil Code, parse through the different options
    to get the statute option existing at the time of the document.
    """

    rule: Rule
    date: datetime.date
