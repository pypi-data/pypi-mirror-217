"""
Pins in the Raspberry Pi GPIO header.
"""
from typing import Dict, TypedDict

from openoligo.hal.devices import DigitalSensor, Switch, Valve
from openoligo.hal.types import Board, NoSuchPinInPinout, Switchable, ValveRole, board
from openoligo.utils.singleton import Singleton


# Initialize fixed pinout
class FixedPinoutDict(TypedDict):
    """
    A dictionary of pinout that can not be configured by the library users.
    """

    waste: Valve
    waste_rxn: Valve
    prod: Valve
    branch: Valve
    rxn_out: Valve
    sol: Valve
    gas: Valve
    liquid_pressure: Switch
    air_pressure: Switch
    liquid_regulator_err: DigitalSensor
    air_regulator_err: DigitalSensor
    server_led: Switch
    runner_led: Switch


fixed_pinout: FixedPinoutDict = {
    "waste": Valve(gpio_pin=board.P7, role=ValveRole.OUTLET),
    "waste_rxn": Valve(gpio_pin=board.P5, role=ValveRole.OUTLET),
    "prod": Valve(gpio_pin=board.P8, role=ValveRole.OUTLET),
    "branch": Valve(gpio_pin=board.P12, role=ValveRole.BRANCH),
    "rxn_out": Valve(gpio_pin=board.P13, role=ValveRole.TRANSIT),
    "sol": Valve(gpio_pin=board.P3),
    "gas": Valve(gpio_pin=board.P10),
    "liquid_pressure": Switch(gpio_pin=board.P11),
    "air_pressure": Switch(gpio_pin=board.P29),
    "liquid_regulator_err": DigitalSensor(gpio_pin=board.P31),
    "air_regulator_err": DigitalSensor(gpio_pin=board.P33),
    "server_led": Switch(gpio_pin=board.P36),
    "runner_led": Switch(gpio_pin=board.P38),
}

reactants = {
    "ACT": Valve(gpio_pin=board.P18),
    "OXI": Valve(gpio_pin=board.P19),
    "CAP1": Valve(gpio_pin=board.P21),
    "CAP2": Valve(gpio_pin=board.P22),
    "DEB": Valve(gpio_pin=board.P23),
    "CLDE": Valve(gpio_pin=board.P24),
}


def list_configurable_pins() -> dict[str, Board]:
    """
    Returns a list of all configurable pins.
    These ar all pins in the board that are not part of the fiixed pinout.
    """
    fixed_pins = [sw.gpio_pin for sw in fixed_pinout.values()]  # type: ignore
    return [pin for pin in board if pin not in fixed_pins]  # type: ignore


class Pinout(metaclass=Singleton):
    """
    Pinout for the instrument.
    """

    def __init__(
        self,
        phosphoramidites: Dict[str, Valve],
    ):
        """
        Initialize the pinout.
        """
        self.fixed = fixed_pinout
        self.reactants = reactants

        self.phosphoramidites = phosphoramidites

        self.__pinout: Dict[str, Switchable] = {}
        self.init_pinout()

    def __add_pinout_safe(self, pin: Switchable, category: str, sub_category: str):
        """
        Check for duplicate pin usage.

        args:
            pin: Pin to check if its already in the pinout.
            category: Category of the pin. (Just for logging)
            sub_category: Sub category of the pin. (the name of the pin)
        """
        if pin in self.__pinout.values():
            raise ValueError(f"Pin {pin} is used twice in {category}.{sub_category}.")
        self.__pinout[sub_category.lower()] = pin

    def init_pinout(self):
        """
        Make sure no pin is used twice.
        """
        for key, switchables in self.__dict__.items():
            if key.startswith("_"):
                continue

            if isinstance(switchables, dict):
                for category, pin in switchables.items():
                    self.__add_pinout_safe(pin, key, category)
            else:
                self.__add_pinout_safe(switchables, self.__class__.__name__, key)

    def pins(self) -> dict[str, Switchable]:
        """
        Return a list of all pins in the pinout.
        """
        return self.__pinout

    def valves(self) -> dict[str, Valve]:
        """
        Return a list of all valves in the pinout.
        """
        return {k: v for k, v in self.__pinout.items() if isinstance(v, Valve)}

    def get(self, name: str) -> Switchable:
        """
        Return the switch/valve with the given name.

        args:
            name: Name of the pin.

        returns:
            The switch/valve with the given name.

        raises:
            KeyError: If the pin is not found.
        """
        try:
            return self.__pinout[name.lower()]
        except KeyError as exc:
            raise NoSuchPinInPinout(
                f"Pin {name} not found in pinout. \n\nAvailable pins are: {list(self.__pinout)}"
            ) from exc

    def get_error_sensors(self) -> dict[str, DigitalSensor]:
        """
        Return a dictionary of all error sensors with their names.
        """
        return {
            name: sensor for name, sensor in self.fixed.items() if isinstance(sensor, DigitalSensor)
        }

    def __repr__(self):
        """
        Return a string representation of the pinout.
        """
        return f"Pinout({self.__pinout})"
