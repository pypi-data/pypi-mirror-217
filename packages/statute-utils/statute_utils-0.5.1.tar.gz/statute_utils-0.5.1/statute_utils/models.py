import datetime
import re
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from re import Pattern
from typing import NamedTuple

from slugify import slugify
from sqlite_utils import Database

from .components import StatuteSerialCategory, make_regex_readable

STATUTE_DB = Database("statute_files.db", use_counts_table=True)


def create_db(db: Database = STATUTE_DB):
    rows = []
    for item in STATUTE_DIR.glob("**/*.yml"):
        cat, num, date, variant = item.parts[-4:]
        v = variant.split(".")[0]
        rows.append(
            {
                "id": "-".join([cat, num, date, v]),
                "cat": cat,
                "num": num,
                "date": date,
                "variant": variant.split(".")[0],
                "size": item.stat().st_size,
            }
        )
    db["statutes"].insert_all(rows, pk="id", ignore=True)  # type: ignore
    db["statutes"].create_index(  # type: ignore
        columns={"cat", "num"},
        index_name="idx_statutes_cat_num",
        if_not_exists=True,
    )
    db["statutes"].create_index(  # type: ignore
        columns={"cat", "num", "date"},
        index_name="idx_statutes_cat_num_date",
        if_not_exists=True,
    )


STATUTE_DIR = Path().home().joinpath("code/corpus-statutes")
if not STATUTE_DB["statutes"].exists():
    create_db()


@dataclass(frozen=True)
class Rule:
    """A `Rule` is detected if it matches either a named pattern or a serial pattern.
    Each rule maps to a category and number.
    """  # noqa: E501

    cat: StatuteSerialCategory
    num: str

    def __repr__(self) -> str:
        return f"<Rule: {self.cat.value} {self.num}>"

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

    @cached_property
    def date(self) -> datetime.date | None:
        try:
            date_str = STATUTE_DB.execute_returning_dicts(
                """--sql
                    select max(s.date) max_date
                    from statutes s
                    where s.cat = :cat and s.num = :num
                    group by s.cat, s.num;
                    """,
                params={"cat": self.cat.value.lower(), "num": self.num.lower()},
            )[0]["max_date"]
            return datetime.date.fromisoformat(date_str)
        except Exception:
            return None


class NamedPattern(NamedTuple):
    name: str
    regex_base: str
    rule: Rule
    matches: list[str] | None = None
    excludes: list[str] | None = None
    options: list[Rule] | None = None

    @property
    def regex(self) -> str:
        return make_regex_readable(rf"(?P<{self.group_name}>{self.regex_base})")

    @property
    def pattern(self) -> Pattern:
        return re.compile(self.regex, re.X)

    @property
    def group_name(self) -> str:
        return self.rule.slug


class SerialPattern(NamedTuple):
    """The word _serial_ is employed because the documents representing rules are numbered consecutively.

    Each serial pattern refers to a statute category, e.g. `RA`, `CA`, etc. matched with an identifier, e.g. 386.

    Field | Description | Example
    --:|:--|:--
    `cat` | [`Statute Category`][statute-category-model] | StatuteSerialCategory.RepublicAct
    `regex_bases` | How do we pattern the category name? | ["r.a. no.", "Rep. Act. No."]
    `regex_serials` | What digits are allowed | ["386", "11114"]
    `matches` | Usable in parametized tests to determine whether the pattern declared matches the samples | ["Republic Act No. 7160", "R.A. 386 and 7160" ]
    `excludes` | Usable in parametized tests to determine that the full pattern will not match | ["Republic Act No. 7160:", "RA 9337-"]
    """  # noqa: E501

    cat: StatuteSerialCategory
    regex_bases: list[str]
    regex_serials: list[str]
    matches: list[str] | None = None
    excludes: list[str] | None = None

    @property
    def lines(self) -> Iterator[str]:
        """Each regex string produced matches the serial rule. Note the line break
        needs to be retained so that when printing `@regex`, the result is organized.
        """
        for base in self.regex_bases:
            for idx in self.regex_serials:
                yield rf"""({base}\s*{idx})
                """

    @property
    def group_name(self) -> str:
        return rf"serial_{self.cat.value}"

    @property
    def regex(self) -> str:
        return rf"(?P<{self.group_name}>{r'|'.join(self.lines)})"

    @property
    def pattern(self) -> Pattern:
        return re.compile(self.regex, re.X)

    @property
    def digits_in_match(self) -> Pattern:
        return re.compile(r"|".join(self.regex_serials))
