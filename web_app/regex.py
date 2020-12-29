import re

regex_dict = {
    "Toyota": [("^XSE|^XLE", "XSE/XLE"), ("^Lim", "Limited"),
               ("^LE|^SE", "LE/SE")],
    "Honda": [(".*LX.*", "LX"), (".*EX-.*", "EX-L"), (".*EX.*", "EX"),
              (".*Spo.*", "Sport"), (".*Touring.*", "Touring")],
    "Nissan": [(".*SL.*", "SL"), (".*SR.*", "SR"), (".*SV.*", "SV"),
               (".*Platinum*", "Platinum"), (".*S.*", "S")],
    "Ford": [(".*SEL.*", "SEL"), (".*SE.*", "SE"), (".*XLT.*", "XLT"),
             (".*Titanium.*", "Titanium"), (".*Lim.*", "Limited"),
             (".*Spo.*", "Sport"), ("^S$|S\s.*", "S")]
}


def trim_parser(trim, make):
    """
    """
    trims = regex_dict.get(make)
    if trim is None or trims is None:
        return "Other"

    try:
        for trim_regex, clean_trim in trims:
            if re.match(trim_regex, trim):
                return clean_trim
        else:
            return "Other"
    except TypeError:
        return "Other"
