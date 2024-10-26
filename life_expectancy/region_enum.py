"""Region class"""
from enum import Enum
from typing import List

class Region(Enum):
    """
    Enum representing various regions and countries with their
    associated codes, and a class method that returns a list of country
    codes excluding union and regional codes.
    """
    AL = 'AL'
    AM = 'AM'
    AT = 'AT'
    AZ = 'AZ'
    BE = 'BE'
    BG = 'BG'
    BY = 'BY'
    CH = 'CH'
    CY = 'CY'
    CZ = 'CZ'
    DE = 'DE'
    DK = 'DK'
    EE = 'EE'
    EL = 'EL'
    ES = 'ES'
    FI = 'FI'
    FR = 'FR'
    FX = 'FX'
    GE = 'GE'
    HR = 'HR'
    HU = 'HU'
    IE = 'IE'
    IS = 'IS'
    IT = 'IT'
    LI = 'LI'
    LT = 'LT'
    LU = 'LU'
    LV = 'LV'
    MD = 'MD'
    ME = 'ME'
    MK = 'MK'
    MT = 'MT'
    NL = 'NL'
    NO = 'NO'
    PL = 'PL'
    PT = 'PT'
    RO = 'RO'
    RS = 'RS'
    RU = 'RU'
    SE = 'SE'
    SI = 'SI'
    SK = 'SK'
    SM = 'SM'
    TR = 'TR'
    UA = 'UA'
    UK = 'UK'
    XK = 'XK'

    @classmethod
    def actual_countries(cls) -> List[str]:
        """
        Returns a list of country codes excluding union and regional codes.
        """
        non_country_codes = {'DE_TOT', 'EA18', 'EA19', 'EEA30_2007', 'EEA31', 'EFTA',
                             'EU27_2007', 'EU27_2020', 'EU28'}
        return [region.value for region in cls if region.name not in non_country_codes]
