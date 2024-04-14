from __future__ import annotations

from typing import Dict

import RPi.GPIO as GPIO  # type: ignore
from src.helpers.general import print_system_msg


class RPiController:
    BOARD_MODES = {"bcm": GPIO.BCM, "board": GPIO.BOARD}
    PIN_MODES = {"in": GPIO.IN, "out": GPIO.OUT}
    VALUES = {"low": GPIO.LOW, "high": GPIO.HIGH}

    def __init__(self) -> None:
        print_system_msg("Initialising RPiController...")
        self._board_mode: str
        self._pins: Dict[int, str] = {}

    def _set_board_mode(self, board_mode: str) -> str:
        if board_mode not in self.BOARD_MODES.keys():
            print_system_msg(f"Invalid board mode '{board_mode}' provided!")
            return board_mode

        print_system_msg(f"Setting board mode to '{board_mode}'...")
        self._board_mode = board_mode
        GPIO.setmode(self.BOARD_MODES[self._board_mode])
        return board_mode

    def _cleanup(self) -> None:
        print_system_msg("Cleaning up GPIO...")
        for pin in self._pins:
            self._output_pin(pin_number=pin, value="high")

        GPIO.cleanup()

    def _setup_pin(self, pin_number: int, mode: str, initial: str) -> int:
        if pin_number in self._pins:
            print_system_msg(f"Pin '{pin_number}' has already been set up!")
            return pin_number

        print_system_msg(f"Setting up pin '{pin_number}' to '{initial}'...")
        val = self.VALUES[initial]
        GPIO.setup(pin_number, self.PIN_MODES[mode], initial=val)
        self._pins[pin_number] = val
        return pin_number

    def _output_pin(self, pin_number: int, value: str) -> None:
        print_system_msg(f"Setting pin '{pin_number}' to '{value}'...")
        GPIO.output(pin_number, self.VALUES[value])

    def _check_pin(self, pin_number: int):
        return pin_number in self._pins.keys()
