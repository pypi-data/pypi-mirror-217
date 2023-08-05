import datetime

from .components import Rule, RuleOption, StatuteSerialCategory
from .models import NamedPattern
from .recipes import CONST, ROC, SP_CIVIL, SP_COMMERCE, SP_PENAL


def make_spanish(name: str, regex: str):
    return NamedPattern(
        name=f"Old {name.title()} Code",
        regex_base=regex,
        rule=Rule(cat=StatuteSerialCategory.Spain, num=name),
    )


spain_civil = make_spanish("civil", SP_CIVIL)
spain_commerce = make_spanish("commerce", SP_COMMERCE)
spain_penal = make_spanish("penal", SP_PENAL)
spain_codes = [spain_civil, spain_commerce, spain_penal]


civ = NamedPattern(
    name="Civil Code of 1950",
    regex_base=r"""
        (?: New|NEW|The|THE)?\s?
        (?: (?<![Ss]panish\s)(?<![Oo]ld\s))
        (Civil|CIVIL)\s+
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES|
            \s+of\s+1950
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="386"),
    matches=[
        "NEW CIVIL CODE",
        "The Civil Code of the Philippines",
        "Civil Code of 1950",
        "Civil Code",
        "CIVIL CODE",
    ],
    excludes=[
        "Spanish Civil Code",
        "OLD CIVIL CODE",
        "The new Civil Code of 1889",
    ],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.Spain, num="civil"),
            date=datetime.date(year=1889, month=1, day=15),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="386"),
            date=datetime.date(year=1950, month=6, day=18),
        ),
    ],
)

family = NamedPattern(
    name="Family Code",
    regex_base=r"""
        (?: The|THE)?\s?
        (Family|FAMILY)\s+
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.ExecutiveOrder, num="209"),
    matches=[
        "Family Code",
        "FAMILY CODE OF THE PHILIPPINES",
    ],
)

child = NamedPattern(
    name="Child and Youth Welfare Code",
    regex_base=r"""
        (?: The|THE)?\s?
        Child\s+
        (and|&)\s+
        Youth\s+
        Welfare\s+
        Code
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.PresidentialDecree, num="603"),
    matches=[
        "Child and Youth Welfare Code",
        "Child & Youth Welfare Code",
    ],
)


tax = NamedPattern(
    name="Tax Code",
    regex_base=r"""
        (
            N\.?I\.?R\.?C\.?|
            National\s+Internal\s+Revenue\s+Code|
            (\d{4}\s+)Tax\s+Code # see Real Property Tax Code
        )
    """,
    rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="8424"),
    matches=[
        "NIRC",
        "N.I.R.C.",
        "National Internal Revenue Code",
        "1997 Tax Code",
    ],
    excludes=[
        "nirc",
        "BNIRC",
        "NIRCx",
    ],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.CommonwealthAct, num="466"),
            date=datetime.date(year=1939, month=6, day=15),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.PresidentialDecree, num="1158"),
            date=datetime.date(year=1977, month=6, day=3),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="8424"),
            date=datetime.date(year=1997, month=12, day=11),
        ),
    ],
)


rpc = NamedPattern(
    name="Revised Penal Code",
    regex_base=r"""
        (
            (?: The\s|THE\s)?
            (?: (?<![Ss]panish\s)(?<![Oo]ld\s))
            (Revised|REVISED)\s+
            (Penal|PENAL)\s+
            (Code|CODE)
            (?:
                \s+of\s+the\s+Philippines|
                \s+OF\s+THE\s+PHILIPPINES|
                \s+\(RPC\)
            )?
        )
    """,
    rule=Rule(cat=StatuteSerialCategory.Act, num="3815"),
    matches=[
        "Revised Penal Code (RPC)",
        "The Revised Penal Code of the Philippines",
        "Revised Penal Code",
    ],
    excludes=[
        "The Penal Code",
        "OLD PENAL CODE",
        "The Spanish Penal Code",
    ],
)


const = NamedPattern(
    name="Constitution",
    regex_base=CONST,
    rule=Rule(cat=StatuteSerialCategory.Constitution, num="1987"),
    matches=[
        "Phil. Constitution",
        "Const.",
        "Constitution of the Philippines",
    ],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.Constitution, num="1935"),
            date=datetime.date(year=1935, month=2, day=8),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.Constitution, num="1973"),
            date=datetime.date(year=1973, month=1, day=17),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.Constitution, num="1987"),
            date=datetime.date(year=1986, month=10, day=15),
        ),
    ],
)


roc = NamedPattern(
    name="Rules of Court",
    regex_base=ROC,
    rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="1964"),
    matches=[
        "Rules of Court",
    ],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="1918"),
            date=datetime.date(year=1918, month=10, day=2),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="1940"),
            date=datetime.date(year=1940, month=7, day=1),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="1964"),
            date=datetime.date(year=1964, month=1, day=1),
        ),
    ],
)


corp = NamedPattern(
    name="Corporation Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (Revised\s+|REVISED\s+)?
        (Corporation|CORPORATION)\s+
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="11232"),
    matches=[
        "Corporation Code",
        "Revised Corporation Code",
    ],
    excludes=["Corporation Law"],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.BatasPambansa, num="68"),
            date=datetime.date(year=1980, month=5, day=1),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="11232"),
            date=datetime.date(year=2019, month=2, day=20),
        ),
    ],
)

labor = NamedPattern(
    name="Labor Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (Labor\s+|LABOR\s+)
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.PresidentialDecree, num="442"),
    matches=[
        "Labor Code",
        "The Labor Code of the Philippines",
    ],
    excludes=["Corporation Law"],
)

locgov = NamedPattern(
    name="Local Government Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (Local\s+|LOCAL\s+)
        (Govt.?\s+|Government\s+|GOVERNMENT\s+)
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="7160"),
    matches=[
        "Local Government Code",
        "The Local Government Code of the Philippines",
    ],
    excludes=["Corporation Law"],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.BatasPambansa, num="337"),
            date=datetime.date(year=1983, month=2, day=10),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="7160"),
            date=datetime.date(year=1991, month=10, day=10),
        ),
    ],
)

admin = NamedPattern(
    name="Administrative Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (Admin.?\s+|ADMIN\s+|Administrative\s+|ADMINISTRATIVE\s+)
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.ExecutiveOrder, num="292"),
    matches=[
        "Administrative Code",
        "Admin. Code",
        "ADMIN Code",
        "The Administrative Code of the Philippines",
    ],
    excludes=["Corporation Law"],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.Act, num="2657"),
            date=datetime.date(year=1916, month=12, day=31),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.Act, num="2711"),
            date=datetime.date(year=1917, month=3, day=10),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.ExecutiveOrder, num="292"),
            date=datetime.date(year=1987, month=7, day=25),
        ),
    ],
)


election = NamedPattern(
    name="Election Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (?: Omnibus\s+|OMNIBUS\s+)?
        (Election\s+|ELECTION\s+)
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.BatasPambansa, num="881"),
    matches=[
        "Election Code",
        "Omnibus Election Code",
    ],
    excludes=["Corporation Law"],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.CommonwealthAct, num="357"),
            date=datetime.date(year=1938, month=8, day=22),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="180"),
            date=datetime.date(year=1947, month=6, day=21),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="6388"),
            date=datetime.date(year=1971, month=9, day=2),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.PresidentialDecree, num="1296"),
            date=datetime.date(year=1978, month=2, day=7),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.BatasPambansa, num="881"),
            date=datetime.date(year=1985, month=12, day=3),
        ),
    ],
)


insurance = NamedPattern(
    name="Insurance Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (Insurance\s+|INSURANCE\s+)
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.PresidentialDecree, num="612"),
    matches=[
        "Insurance Code",
    ],
    excludes=["Insurance Law", "Insurance Act"],
)

cooperative = NamedPattern(
    name="Cooperative Code",
    regex_base=r"""
        (?: The\s|THE\s)?
        (?: Philippine\s+)?
        (Cooperative\s+|COOPERATIVE\s+)
        (Code|CODE)
        (?:
            \s+of\s+the\s+Philippines|
            \s+OF\s+THE\s+PHILIPPINES
        )?
    """,
    rule=Rule(cat=StatuteSerialCategory.RepublicAct, num="6938"),
    matches=[
        "Cooperative Code",
        "Philippine Cooperative Code",
    ],
    excludes=["Cooperative Law", "Cooperative Act"],
)


prof_responsibility = NamedPattern(
    name="Code of Professional Responsibility",
    regex_base=r"""
        (?:
            (?:Code|CODE)
            \s+
            (?:of|Of|OF)
            \s+
            (?:Professional|PROFESSIONAL)
            \s+
            (?:Responsibility|RESPONSIBILITY)
            (?:
                \s+
                and
                \s+
                Accountability|ACCOUNTABILITY
            )?
            (?:\s+
                \(
                    CPR
                    A?
                \)
            )?
        )|
        (?:
            of\s+
            the\s+
            CPR
            A?
        )
    """,
    rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="cpr"),
    matches=[
        "Code of Professional Responsibility and Accountability (CPRA)",
        "Code of Professional Responsibility and Accountability",
        "Code of Professional Responsibility (CPR)",
        "Code of Professional Responsibility",
        "CODE OF PROFESSIONAL RESPONSIBILITY",
        "of the CPRA",
        "of the CPR",
    ],
    excludes=[
        "Responsibility and Accountability",
        "Code of Professional Ethics",
        "CPA",
    ],
    options=[
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="cpr"),
            date=datetime.date(year=1988, month=6, day=21),
        ),
        RuleOption(
            rule=Rule(cat=StatuteSerialCategory.RulesOfCourt, num="cpra"),
            date=datetime.date(year=2023, month=4, day=13),
        ),
    ],
)


NAMED_COLLECTION = [
    admin,
    civ,
    rpc,
    corp,
    labor,
    locgov,
    prof_responsibility,
    const,
    roc,
    tax,
    insurance,
    election,
    cooperative,
] + spain_codes
"""
Each named legal title, not falling under `SERIAL_COLLECTION`,
will also have its own manually crafted regex string. Examples include
'the Spanish Civil Code' or the '1987 Constitution' or the
'Code of Professional Responsibility'.
"""
