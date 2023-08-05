import datetime
import re
from collections import Counter
from collections.abc import Iterator
from operator import attrgetter
from typing import NamedTuple, Self

from .components import Rule, StatuteSerialCategory
from .models import NamedPattern, SerialPattern
from .models_names import NAMED_COLLECTION
from .models_serials import SERIAL_COLLECTION
from .recipes import split_digits


def create_pattern(collection: list[SerialPattern] | list[NamedPattern]) -> re.Pattern:
    return re.compile("|".join([style.regex for style in collection]), re.X)


COLLECTED_SERIALS = create_pattern(collection=SERIAL_COLLECTION)
"""Each serial regex string is combined into a single regex string so that `finditer()` can used."""  # noqa: E501
COLLECTED_NAMES = create_pattern(collection=NAMED_COLLECTION)
"""Each named regex string is combined into a single regex string so that `finditer()` can used."""  # noqa: E501


def extract_serial_rules(text: str) -> Iterator[Rule]:
    """Each `m`, a python Match object, represents a
    serial pattern category with possible ambiguous identifier found.

    So running `m.group(0)` should yield the entire text of the
    match which consists of (a) the definitive category;
    and (b) the ambiguous identifier.

    The identifier is ambiguous because it may be a compound one,
    e.g. 'Presidential Decree No. 1 and 2'. In this case, there
    should be 2 matches produced not just one.

    This function splits the identifier by commas `,` and the
    word `and` to get the individual component identifiers.
    """
    for match in COLLECTED_SERIALS.finditer(text):
        for style in SERIAL_COLLECTION:
            if match.lastgroup == style.group_name:
                if candidates := style.digits_in_match.search(match.group(0)):
                    for d in split_digits(candidates.group(0)):
                        yield Rule(cat=style.cat, num=d.lower())


def extract_named_rules(
    text: str, document_date: datetime.date | None = None
) -> Iterator[Rule]:
    """Using `text`, get named rules in serial format with a special criteria when
    the `document_date` is provided.

    Args:
        text (str): The text to extract named patterns from.
        document_date (datetime.date | None, optional): When present, will use the `named.options`. Defaults to None.

    Yields:
        Iterator[Rule]: The applicable rule found
    """  # noqa: E501
    for m in COLLECTED_NAMES.finditer(text):
        for named in NAMED_COLLECTION:
            if m.lastgroup == named.group_name:
                if named.options and document_date:
                    # sorts the options in descending order
                    options = sorted(
                        named.options, key=attrgetter("date"), reverse=True
                    )
                    for option in options:
                        # default to the first option that can include
                        # the document date, so if the document date
                        # is 1940 and the civil code date sorted options are
                        # [1950, 1889]
                        # this will skip the first because of the `if` conditional
                        # but include the second
                        if document_date > option.date:
                            yield option.rule
                            break
                else:
                    yield named.rule


def extract_rules(
    text: str, document_date: datetime.date | None = None
) -> Iterator[Rule]:
    """If text contains [serialized][serial-pattern] (e.g. _Republic Act No. 386_)
    and [named][named-pattern] rules (_the Civil Code of the Philippines_),
    extract the [`Rules`][rule-model] into their canonical serial variants.

    Examples:
        >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
        >>> list(extract_rules(text)) # get all rules
        [ra 386, ra 386, spain civil]
        >>> ambiguous_text = "The Civil Code"
        >>> doc_date1 = datetime.date(year=1940, month=1, day=1)
        >>> list(extract_rules(ambiguous_text, doc_date1))
        [spain civil]
        >>> doc_date2 = datetime.date(year=1960, month=1, day=1)
        >>> list(extract_rules(ambiguous_text, doc_date2))
        [ra 386]

    Args:
        text (str): Text to search for statute patterns.

    Yields:
        Iterator[Rule]: Serialized Rules and Named Rule patterns
    """  # noqa: E501
    yield from extract_serial_rules(text)
    yield from extract_named_rules(text, document_date)


def extract_rule(text: str) -> Rule | None:
    """Thin wrapper over [`extract_rules()`][extract-rules]. If text contains a
    matching [`Rule`][rule-model], get the first one found.

    Examples:
        >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
        >>> extract_rule(text)  # get the first matching rule
        ra 386

    Args:
        text (str): Text to search for statute patterns.

    Returns:
        Rule | None: The first Rule found, if it exists
    """  # noqa: E501
    try:
        return next(extract_rules(text))
    except StopIteration:
        return None


class CountedStatute(NamedTuple):
    """Based on results from `extract_rules()`, get count of each
    unique rule found."""

    cat: StatuteSerialCategory
    num: str
    mentions: int

    def __repr__(self) -> str:
        return f"{self.cat} {self.num}: {self.mentions}"

    @classmethod
    def from_source(cls, text: str) -> Iterator[Self]:
        """Detect counted rules from source `text`.

        Examples:
            >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
            >>> results = list(CountedStatute.from_source(text))
            >>> results
            [ra 386: 2, spain civil: 1]
            >>> results[0] == CountedStatute(cat=StatuteSerialCategory('ra'),num='386', mentions=2)
            True
            >>> results[1] == CountedStatute(cat=StatuteSerialCategory('spain'),num='civil', mentions=1)
            True

        Args:
            text (str): Legalese containing statutory rules in various formats.

        Yields:
            Iterator[Self]: Each counted rule found.
        """  # noqa: E501
        rules = extract_rules(text)
        for k, v in Counter(rules).items():
            yield cls(cat=k.cat, num=k.num, mentions=v)

    @classmethod
    def from_repr_format(cls, repr_texts: list[str]) -> Iterator[Self]:
        """Generate their pydantic counterparts from `<cat> <id>: <mentions>` format.

        Examples:
            >>> repr_texts = ['ra 386: 2', 'spain civil: 1']
            >>> results = list(CountedStatute.from_repr_format(repr_texts))
            >>> results
            [ra 386: 2, spain civil: 1]
            >>> results[0].cat
            'ra'
            >>> results[0].num
            '386'
            >>> results[0].mentions
            2
            >>> str(results[0])
            'ra 386: 2'
            >>> repr(results[0])
            'ra 386: 2'


        Args:
            repr_texts (str): list of texts having `__repr__` format of a `CountedStatute`

        Yields:
            Iterator[Self]: Instances of CountedStatute
        """  # noqa: E501
        for text in repr_texts:
            counted_bits = text.split(":")
            if len(counted_bits) == 2:
                statute_bits = counted_bits[0].split()
                mentions = counted_bits[1]
                is_cat_id = len(statute_bits) == 2
                is_digit_bit = mentions.strip().isdigit()
                if is_cat_id and is_digit_bit:
                    if cat := StatuteSerialCategory(statute_bits[0]):
                        yield cls(cat=cat, num=statute_bits[1], mentions=int(mentions))
