# Tables.
import json
from time import time

import requests

from .exceptions import DefinitionError
from .globals import defined
from .utilities import dictFromUnit

# Tables utilities


def getRep(family: str) -> str:
    """
    Returns a reference unit given its family.
    """

    table = getBase()
    table.update(getDerived())

    if family in table:
        # This shouldn't raise an IndexError as long as there's a reference unit for every family.
        return [u for u in table[family] if table[family][u] == 1].pop()


def getFamily(unit: str) -> str:
    """
    Returns the family of a convertible unit.
    """

    table = getBase()
    table.update(getDerived())
    table.update(getCurrencies())

    for family in table:
        if unit in table[family]:
            return family

    return ""


# Tables functions.


def getBase() -> dict:
    # SI units.
    table = SI_TABLE.copy()

    # User defined units.
    table.update(defined.BASE_TABLE)

    return table


def getDerived() -> dict:
    # SI derived units.
    table = SI_DERIVED_TABLE.copy()

    # User defined derived units.
    table.update(defined.DERIVED_TABLE)

    return table


def getDerivedUnpacking() -> dict:
    # SI derived units.
    table = SI_DERIVED_UNPACKING_TABLE.copy()

    # User defined derived units.
    table.update(defined.DERIVED_UNPACKING_TABLE)

    return table


def getCurrencies() -> dict:
    # Standard currencies.
    table = CURRENCIES_TABLE.copy()

    return table


def fetchCurrencies() -> None:
    from .globals import currencies

    try:
        file = open(currencies.path, "r")
        data = json.load(file)

        # Reload rates older than 6 hours.
        if time() - data["time"] < 3600 * 6:
            rates = data["rates"]

        else:
            raise FileNotFoundError

    except (FileNotFoundError, json.JSONDecodeError):
        rates = requests.get(
            "https://misura.diantonioandrea.com/currencies/rates.json"
        ).json()["rates"]

        file = open(currencies.path, "w")
        data = {"time": time(), "rates": rates}
        json.dump(data, file)

    file.close()

    for curr in rates:
        CURRENCIES_TABLE["currency"][curr] = 1 / rates[curr]


# Conversion tables.


def addUnit(family: str, units: dict, unpacks: str = ""):
    """
    addUnit function, allows users to define new units.
    """

    table = getBase()
    table.update(getDerived())

    try:
        assert isinstance(family, str)
        assert isinstance(units, dict)
        assert family
        assert units

        assert isinstance(unpacks, str) if unpacks else True

    except AssertionError:
        raise DefinitionError("invalid options")

    family = family.lower()

    # Checks family.
    if family in table:
        raise DefinitionError("'{}' already exixts".format(family))

    # Checks rep.
    if len([u for u in units if units[u] == 1]) != 1:
        raise DefinitionError("missing or invalid rep for family {}".format(family))

    # Checks units.
    for u in units:
        if not isinstance(u, str):
            raise DefinitionError("invalid unit '{}'".format(u))

        if not isinstance(units[u], (int, float)):
            raise DefinitionError(
                "invalid unit factor for '{}: {}'".format(u, units[u])
            )

        if any([u in table[family] for family in table]):
            raise DefinitionError(
                "unit already defined in family '{}'".format(getFamily(u))
            )

    # Derived units checks.
    if unpacks:
        rep = [u for u in units if units[u] == 1].pop()

        if rep in getDerivedUnpacking():
            raise DefinitionError(
                "unit already defined in the unpacking table '{}'".format(rep)
            )

        for u in dictFromUnit(unpacks):
            if not getFamily(u):
                raise DefinitionError("invalid unit '{}'".format(u))

    if not unpacks:
        defined.BASE_TABLE[family] = {u: units[u] for u in units}

    else:
        defined.DERIVED_TABLE[family] = {u: units[u] for u in units}
        defined.DERIVED_UNPACKING_TABLE[rep] = unpacks


# QUANTITIES

# Base units - SI.
SI_TABLE = {
    "time": {
        "qs": 1e-30,
        "rs": 1e-27,
        "ys": 1e-24,
        "zs": 1e-21,
        "as": 1e-18,
        "fs": 1e-15,
        "ps": 1e-12,
        "ns": 1e-09,
        "µs": 1e-06,
        "ms": 0.001,
        "cs": 0.01,
        "ds": 0.1,
        "s": 1.0,
        "das": 10.0,
        "hs": 100.0,
        "ks": 1000.0,
        "Ms": 1000000.0,
        "Gs": 1000000000.0,
        "Ts": 1000000000000.0,
        "Ps": 1000000000000000.0,
        "Es": 1e18,
        "Zs": 1e21,
        "Ys": 1e24,
        "Rs": 1e27,
        "Qs": 1e30,
    },
    "length": {
        "qm": 1e-30,
        "rm": 1e-27,
        "ym": 1e-24,
        "zm": 1e-21,
        "am": 1e-18,
        "fm": 1e-15,
        "pm": 1e-12,
        "nm": 1e-09,
        "µm": 1e-06,
        "mm": 0.001,
        "cm": 0.01,
        "dm": 0.1,
        "m": 1.0,
        "dam": 10.0,
        "hm": 100.0,
        "km": 1000.0,
        "Mm": 1000000.0,
        "Gm": 1000000000.0,
        "Tm": 1000000000000.0,
        "Pm": 1000000000000000.0,
        "Em": 1e18,
        "Zm": 1e21,
        "Ym": 1e24,
        "Rm": 1e27,
        "Qm": 1e30,
    },
    "mass": {
        "qg": 1e-33,
        "rg": 1e-30,
        "yg": 1e-27,
        "zg": 1e-24,
        "ag": 1e-21,
        "fg": 1e-18,
        "pg": 1e-15,
        "ng": 1e-12,
        "µg": 1e-09,
        "mg": 1e-06,
        "cg": 1e-05,
        "dg": 1e-04,
        "g": 0.001,
        "dag": 0.01,
        "hg": 0.1,
        "kg": 1.0,
        "Mg": 1000.0,
        "Gg": 1000000.0,
        "Tg": 1000000000.0,
        "Pg": 1000000000000.0,
        "Eg": 1e15,
        "Zg": 1e18,
        "Yg": 1e21,
        "Rg": 1e24,
        "Qg": 1e27,
    },
    "electric current": {
        "qA": 1e-30,
        "rA": 1e-27,
        "yA": 1e-24,
        "zA": 1e-21,
        "aA": 1e-18,
        "fA": 1e-15,
        "pA": 1e-12,
        "nA": 1e-09,
        "µA": 1e-06,
        "mA": 0.001,
        "cA": 0.01,
        "dA": 0.1,
        "A": 1.0,
        "daA": 10.0,
        "hA": 100.0,
        "kA": 1000.0,
        "MA": 1000000.0,
        "GA": 1000000000.0,
        "TA": 1000000000000.0,
        "PA": 1000000000000000.0,
        "EA": 1e18,
        "ZA": 1e21,
        "YA": 1e24,
        "RA": 1e27,
        "QA": 1e30,
    },
    "thermodynamic temperature": {
        "qK": 1e-30,
        "rK": 1e-27,
        "yK": 1e-24,
        "zK": 1e-21,
        "aK": 1e-18,
        "fK": 1e-15,
        "pK": 1e-12,
        "nK": 1e-09,
        "µK": 1e-06,
        "mK": 0.001,
        "cK": 0.01,
        "dK": 0.1,
        "K": 1.0,
        "daK": 10.0,
        "hK": 100.0,
        "kK": 1000.0,
        "MK": 1000000.0,
        "GK": 1000000000.0,
        "TK": 1000000000000.0,
        "PK": 1000000000000000.0,
        "EK": 1e18,
        "ZK": 1e21,
        "YK": 1e24,
        "RK": 1e27,
        "QK": 1e30,
    },
    "amount of substance": {
        "qmol": 1e-30,
        "rmol": 1e-27,
        "ymol": 1e-24,
        "zmol": 1e-21,
        "amol": 1e-18,
        "fmol": 1e-15,
        "pmol": 1e-12,
        "nmol": 1e-09,
        "µmol": 1e-06,
        "mmol": 0.001,
        "cmol": 0.01,
        "dmol": 0.1,
        "mol": 1.0,
        "damol": 10.0,
        "hmol": 100.0,
        "kmol": 1000.0,
        "Mmol": 1000000.0,
        "Gmol": 1000000000.0,
        "Tmol": 1000000000000.0,
        "Pmol": 1000000000000000.0,
        "Emol": 1e18,
        "Zmol": 1e21,
        "Ymol": 1e24,
        "Rmol": 1e27,
        "Qmol": 1e30,
    },
    "luminous intensity": {
        "qcd": 1e-30,
        "rcd": 1e-27,
        "ycd": 1e-24,
        "zcd": 1e-21,
        "acd": 1e-18,
        "fcd": 1e-15,
        "pcd": 1e-12,
        "ncd": 1e-09,
        "µcd": 1e-06,
        "mcd": 0.001,
        "ccd": 0.01,
        "dcd": 0.1,
        "cd": 1.0,
        "dacd": 10.0,
        "hcd": 100.0,
        "kcd": 1000.0,
        "Mcd": 1000000.0,
        "Gcd": 1000000000.0,
        "Tcd": 1000000000000.0,
        "Pcd": 1000000000000000.0,
        "Ecd": 1e18,
        "Zcd": 1e21,
        "Ycd": 1e24,
        "Rcd": 1e27,
        "Qcd": 1e30,
    },
}

# Derived units - SI.
# Missing Celsius.
SI_DERIVED_TABLE = {
    "plane angle": {
        "qrad": 1e-30,
        "rrad": 1e-27,
        "yrad": 1e-24,
        "zrad": 1e-21,
        "arad": 1e-18,
        "frad": 1e-15,
        "prad": 1e-12,
        "nrad": 1e-09,
        "µrad": 1e-06,
        "mrad": 0.001,
        "crad": 0.01,
        "drad": 0.1,
        "rad": 1.0,
        "darad": 10.0,
        "hrad": 100.0,
        "krad": 1000.0,
        "Mrad": 1000000.0,
        "Grad": 1000000000.0,
        "Trad": 1000000000000.0,
        "Prad": 1000000000000000.0,
        "Erad": 1e18,
        "Zrad": 1e21,
        "Yrad": 1e24,
        "Rrad": 1e27,
        "Qrad": 1e30,
    },
    "solid angle": {
        "qsr": 1e-30,
        "rsr": 1e-27,
        "ysr": 1e-24,
        "zsr": 1e-21,
        "asr": 1e-18,
        "fsr": 1e-15,
        "psr": 1e-12,
        "nsr": 1e-09,
        "µsr": 1e-06,
        "msr": 0.001,
        "csr": 0.01,
        "dsr": 0.1,
        "sr": 1.0,
        "dasr": 10.0,
        "hsr": 100.0,
        "ksr": 1000.0,
        "Msr": 1000000.0,
        "Gsr": 1000000000.0,
        "Tsr": 1000000000000.0,
        "Psr": 1000000000000000.0,
        "Esr": 1e18,
        "Zsr": 1e21,
        "Ysr": 1e24,
        "Rsr": 1e27,
        "Qsr": 1e30,
    },
    "frequency": {
        "qHz": 1e-30,
        "rHz": 1e-27,
        "yHz": 1e-24,
        "zHz": 1e-21,
        "aHz": 1e-18,
        "fHz": 1e-15,
        "pHz": 1e-12,
        "nHz": 1e-09,
        "µHz": 1e-06,
        "mHz": 0.001,
        "cHz": 0.01,
        "dHz": 0.1,
        "Hz": 1.0,
        "daHz": 10.0,
        "hHz": 100.0,
        "kHz": 1000.0,
        "MHz": 1000000.0,
        "GHz": 1000000000.0,
        "THz": 1000000000000.0,
        "PHz": 1000000000000000.0,
        "EHz": 1e18,
        "ZHz": 1e21,
        "YHz": 1e24,
        "RHz": 1e27,
        "QHz": 1e30,
    },
    "force": {
        "qN": 1e-30,
        "rN": 1e-27,
        "yN": 1e-24,
        "zN": 1e-21,
        "aN": 1e-18,
        "fN": 1e-15,
        "pN": 1e-12,
        "nN": 1e-09,
        "µN": 1e-06,
        "mN": 0.001,
        "cN": 0.01,
        "dN": 0.1,
        "N": 1.0,
        "daN": 10.0,
        "hN": 100.0,
        "kN": 1000.0,
        "MN": 1000000.0,
        "GN": 1000000000.0,
        "TN": 1000000000000.0,
        "PN": 1000000000000000.0,
        "EN": 1e18,
        "ZN": 1e21,
        "YN": 1e24,
        "RN": 1e27,
        "QN": 1e30,
    },
    "pressure": {
        "qPa": 1e-30,
        "rPa": 1e-27,
        "yPa": 1e-24,
        "zPa": 1e-21,
        "aPa": 1e-18,
        "fPa": 1e-15,
        "pPa": 1e-12,
        "nPa": 1e-09,
        "µPa": 1e-06,
        "mPa": 0.001,
        "cPa": 0.01,
        "dPa": 0.1,
        "Pa": 1.0,
        "daPa": 10.0,
        "hPa": 100.0,
        "kPa": 1000.0,
        "MPa": 1000000.0,
        "GPa": 1000000000.0,
        "TPa": 1000000000000.0,
        "PPa": 1000000000000000.0,
        "EPa": 1e18,
        "ZPa": 1e21,
        "YPa": 1e24,
        "RPa": 1e27,
        "QPa": 1e30,
    },
    "energy": {
        "qJ": 1e-30,
        "rJ": 1e-27,
        "yJ": 1e-24,
        "zJ": 1e-21,
        "aJ": 1e-18,
        "fJ": 1e-15,
        "pJ": 1e-12,
        "nJ": 1e-09,
        "µJ": 1e-06,
        "mJ": 0.001,
        "cJ": 0.01,
        "dJ": 0.1,
        "J": 1.0,
        "daJ": 10.0,
        "hJ": 100.0,
        "kJ": 1000.0,
        "MJ": 1000000.0,
        "GJ": 1000000000.0,
        "TJ": 1000000000000.0,
        "PJ": 1000000000000000.0,
        "EJ": 1e18,
        "ZJ": 1e21,
        "YJ": 1e24,
        "RJ": 1e27,
        "QJ": 1e30,
    },
    "power": {
        "qW": 1e-30,
        "rW": 1e-27,
        "yW": 1e-24,
        "zW": 1e-21,
        "aW": 1e-18,
        "fW": 1e-15,
        "pW": 1e-12,
        "nW": 1e-09,
        "µW": 1e-06,
        "mW": 0.001,
        "cW": 0.01,
        "dW": 0.1,
        "W": 1.0,
        "daW": 10.0,
        "hW": 100.0,
        "kW": 1000.0,
        "MW": 1000000.0,
        "GW": 1000000000.0,
        "TW": 1000000000000.0,
        "PW": 1000000000000000.0,
        "EW": 1e18,
        "ZW": 1e21,
        "YW": 1e24,
        "RW": 1e27,
        "QW": 1e30,
    },
    "electric charge": {
        "qC": 1e-30,
        "rC": 1e-27,
        "yC": 1e-24,
        "zC": 1e-21,
        "aC": 1e-18,
        "fC": 1e-15,
        "pC": 1e-12,
        "nC": 1e-09,
        "µC": 1e-06,
        "mC": 0.001,
        "cC": 0.01,
        "dC": 0.1,
        "C": 1.0,
        "daC": 10.0,
        "hC": 100.0,
        "kC": 1000.0,
        "MC": 1000000.0,
        "GC": 1000000000.0,
        "TC": 1000000000000.0,
        "PC": 1000000000000000.0,
        "EC": 1e18,
        "ZC": 1e21,
        "YC": 1e24,
        "RC": 1e27,
        "QC": 1e30,
    },
    "electric potential": {
        "qV": 1e-30,
        "rV": 1e-27,
        "yV": 1e-24,
        "zV": 1e-21,
        "aV": 1e-18,
        "fV": 1e-15,
        "pV": 1e-12,
        "nV": 1e-09,
        "µV": 1e-06,
        "mV": 0.001,
        "cV": 0.01,
        "dV": 0.1,
        "V": 1.0,
        "daV": 10.0,
        "hV": 100.0,
        "kV": 1000.0,
        "MV": 1000000.0,
        "GV": 1000000000.0,
        "TV": 1000000000000.0,
        "PV": 1000000000000000.0,
        "EV": 1e18,
        "ZV": 1e21,
        "YV": 1e24,
        "RV": 1e27,
        "QV": 1e30,
    },
    "capacitance": {
        "qF": 1e-30,
        "rF": 1e-27,
        "yF": 1e-24,
        "zF": 1e-21,
        "aF": 1e-18,
        "fF": 1e-15,
        "pF": 1e-12,
        "nF": 1e-09,
        "µF": 1e-06,
        "mF": 0.001,
        "cF": 0.01,
        "dF": 0.1,
        "F": 1.0,
        "daF": 10.0,
        "hF": 100.0,
        "kF": 1000.0,
        "MF": 1000000.0,
        "GF": 1000000000.0,
        "TF": 1000000000000.0,
        "PF": 1000000000000000.0,
        "EF": 1e18,
        "ZF": 1e21,
        "YF": 1e24,
        "RF": 1e27,
        "QF": 1e30,
    },
    "resistance": {
        "qΩ": 1e-30,
        "rΩ": 1e-27,
        "yΩ": 1e-24,
        "zΩ": 1e-21,
        "aΩ": 1e-18,
        "fΩ": 1e-15,
        "pΩ": 1e-12,
        "nΩ": 1e-09,
        "µΩ": 1e-06,
        "mΩ": 0.001,
        "cΩ": 0.01,
        "dΩ": 0.1,
        "Ω": 1.0,
        "daΩ": 10.0,
        "hΩ": 100.0,
        "kΩ": 1000.0,
        "MΩ": 1000000.0,
        "GΩ": 1000000000.0,
        "TΩ": 1000000000000.0,
        "PΩ": 1000000000000000.0,
        "EΩ": 1e18,
        "ZΩ": 1e21,
        "YΩ": 1e24,
        "RΩ": 1e27,
        "QΩ": 1e30,
    },
    "electrical conductance": {
        "qS": 1e-30,
        "rS": 1e-27,
        "yS": 1e-24,
        "zS": 1e-21,
        "aS": 1e-18,
        "fS": 1e-15,
        "pS": 1e-12,
        "nS": 1e-09,
        "µS": 1e-06,
        "mS": 0.001,
        "cS": 0.01,
        "dS": 0.1,
        "S": 1.0,
        "daS": 10.0,
        "hS": 100.0,
        "kS": 1000.0,
        "MS": 1000000.0,
        "GS": 1000000000.0,
        "TS": 1000000000000.0,
        "PS": 1000000000000000.0,
        "ES": 1e18,
        "ZS": 1e21,
        "YS": 1e24,
        "RS": 1e27,
        "QS": 1e30,
    },
    "magnetic flux": {
        "qWb": 1e-30,
        "rWb": 1e-27,
        "yWb": 1e-24,
        "zWb": 1e-21,
        "aWb": 1e-18,
        "fWb": 1e-15,
        "pWb": 1e-12,
        "nWb": 1e-09,
        "µWb": 1e-06,
        "mWb": 0.001,
        "cWb": 0.01,
        "dWb": 0.1,
        "Wb": 1.0,
        "daWb": 10.0,
        "hWb": 100.0,
        "kWb": 1000.0,
        "MWb": 1000000.0,
        "GWb": 1000000000.0,
        "TWb": 1000000000000.0,
        "PWb": 1000000000000000.0,
        "EWb": 1e18,
        "ZWb": 1e21,
        "YWb": 1e24,
        "RWb": 1e27,
        "QWb": 1e30,
    },
    "magnetic flux density": {
        "qT": 1e-30,
        "rT": 1e-27,
        "yT": 1e-24,
        "zT": 1e-21,
        "aT": 1e-18,
        "fT": 1e-15,
        "pT": 1e-12,
        "nT": 1e-09,
        "µT": 1e-06,
        "mT": 0.001,
        "cT": 0.01,
        "dT": 0.1,
        "T": 1.0,
        "daT": 10.0,
        "hT": 100.0,
        "kT": 1000.0,
        "MT": 1000000.0,
        "GT": 1000000000.0,
        "TT": 1000000000000.0,
        "PT": 1000000000000000.0,
        "ET": 1e18,
        "ZT": 1e21,
        "YT": 1e24,
        "RT": 1e27,
        "QT": 1e30,
    },
    "inductance": {
        "qH": 1e-30,
        "rH": 1e-27,
        "yH": 1e-24,
        "zH": 1e-21,
        "aH": 1e-18,
        "fH": 1e-15,
        "pH": 1e-12,
        "nH": 1e-09,
        "µH": 1e-06,
        "mH": 0.001,
        "cH": 0.01,
        "dH": 0.1,
        "H": 1.0,
        "daH": 10.0,
        "hH": 100.0,
        "kH": 1000.0,
        "MH": 1000000.0,
        "GH": 1000000000.0,
        "TH": 1000000000000.0,
        "PH": 1000000000000000.0,
        "EH": 1e18,
        "ZH": 1e21,
        "YH": 1e24,
        "RH": 1e27,
        "QH": 1e30,
    },
    "luminous flux": {
        "qlm": 1e-30,
        "rlm": 1e-27,
        "ylm": 1e-24,
        "zlm": 1e-21,
        "alm": 1e-18,
        "flm": 1e-15,
        "plm": 1e-12,
        "nlm": 1e-09,
        "µlm": 1e-06,
        "mlm": 0.001,
        "clm": 0.01,
        "dlm": 0.1,
        "lm": 1.0,
        "dalm": 10.0,
        "hlm": 100.0,
        "klm": 1000.0,
        "Mlm": 1000000.0,
        "Glm": 1000000000.0,
        "Tlm": 1000000000000.0,
        "Plm": 1000000000000000.0,
        "Elm": 1e18,
        "Zlm": 1e21,
        "Ylm": 1e24,
        "Rlm": 1e27,
        "Qlm": 1e30,
    },
    "illuminance": {
        "qlx": 1e-30,
        "rlx": 1e-27,
        "ylx": 1e-24,
        "zlx": 1e-21,
        "alx": 1e-18,
        "flx": 1e-15,
        "plx": 1e-12,
        "nlx": 1e-09,
        "µlx": 1e-06,
        "mlx": 0.001,
        "clx": 0.01,
        "dlx": 0.1,
        "lx": 1.0,
        "dalx": 10.0,
        "hlx": 100.0,
        "klx": 1000.0,
        "Mlx": 1000000.0,
        "Glx": 1000000000.0,
        "Tlx": 1000000000000.0,
        "Plx": 1000000000000000.0,
        "Elx": 1e18,
        "Zlx": 1e21,
        "Ylx": 1e24,
        "Rlx": 1e27,
        "Qlx": 1e30,
    },
    "radionuclide activity": {
        "qBq": 1e-30,
        "rBq": 1e-27,
        "yBq": 1e-24,
        "zBq": 1e-21,
        "aBq": 1e-18,
        "fBq": 1e-15,
        "pBq": 1e-12,
        "nBq": 1e-09,
        "µBq": 1e-06,
        "mBq": 0.001,
        "cBq": 0.01,
        "dBq": 0.1,
        "Bq": 1.0,
        "daBq": 10.0,
        "hBq": 100.0,
        "kBq": 1000.0,
        "MBq": 1000000.0,
        "GBq": 1000000000.0,
        "TBq": 1000000000000.0,
        "PBq": 1000000000000000.0,
        "EBq": 1e18,
        "ZBq": 1e21,
        "YBq": 1e24,
        "RBq": 1e27,
        "QBq": 1e30,
    },
    "absorbed dose": {
        "qGy": 1e-30,
        "rGy": 1e-27,
        "yGy": 1e-24,
        "zGy": 1e-21,
        "aGy": 1e-18,
        "fGy": 1e-15,
        "pGy": 1e-12,
        "nGy": 1e-09,
        "µGy": 1e-06,
        "mGy": 0.001,
        "cGy": 0.01,
        "dGy": 0.1,
        "Gy": 1.0,
        "daGy": 10.0,
        "hGy": 100.0,
        "kGy": 1000.0,
        "MGy": 1000000.0,
        "GGy": 1000000000.0,
        "TGy": 1000000000000.0,
        "PGy": 1000000000000000.0,
        "EGy": 1e18,
        "ZGy": 1e21,
        "YGy": 1e24,
        "RGy": 1e27,
        "QGy": 1e30,
    },
    "equivalent dose": {
        "qSv": 1e-30,
        "rSv": 1e-27,
        "ySv": 1e-24,
        "zSv": 1e-21,
        "aSv": 1e-18,
        "fSv": 1e-15,
        "pSv": 1e-12,
        "nSv": 1e-09,
        "µSv": 1e-06,
        "mSv": 0.001,
        "cSv": 0.01,
        "dSv": 0.1,
        "Sv": 1.0,
        "daSv": 10.0,
        "hSv": 100.0,
        "kSv": 1000.0,
        "MSv": 1000000.0,
        "GSv": 1000000000.0,
        "TSv": 1000000000000.0,
        "PSv": 1000000000000000.0,
        "ESv": 1e18,
        "ZSv": 1e21,
        "YSv": 1e24,
        "RSv": 1e27,
        "QSv": 1e30,
    },
    "catalyc activity": {
        "qkat": 1e-30,
        "rkat": 1e-27,
        "ykat": 1e-24,
        "zkat": 1e-21,
        "akat": 1e-18,
        "fkat": 1e-15,
        "pkat": 1e-12,
        "nkat": 1e-09,
        "µkat": 1e-06,
        "mkat": 0.001,
        "ckat": 0.01,
        "dkat": 0.1,
        "kat": 1.0,
        "dakat": 10.0,
        "hkat": 100.0,
        "kkat": 1000.0,
        "Mkat": 1000000.0,
        "Gkat": 1000000000.0,
        "Tkat": 1000000000000.0,
        "Pkat": 1000000000000000.0,
        "Ekat": 1e18,
        "Zkat": 1e21,
        "Ykat": 1e24,
        "Rkat": 1e27,
        "Qkat": 1e30,
    },
}

SI_DERIVED_UNPACKING_TABLE = {
    "Hz": "s-1",
    "N": "kg m s-2",
    "Pa": "kg m-1 s-2",
    "J": "kg m2 s-2",
    "W": "kg m2 s-3",
    "C": "A s",
    "V": "kg m2 s-3 A-1",
    "F": "kg-1 m-2 s4 A2",
    "Ω": "kg m2 s-3 A-2",
    "S": "kg-1 m-2 s3 A2",
    "Wb": "kg m2 s-2 A-1",
    "T": "kg s-2 A-1",
    "H": "kg m2 s-2 A-2",
    "lm": "cd sr",
    "lx": "cd sr m-2",
    "Bq": "s-1",
    "Gy": "m2 s-2",
    "Sv": "m2 s-2",
    "kat": "mol s-1",
}

# CURRENCIES

CURRENCIES_TABLE = {"currency": dict()}
