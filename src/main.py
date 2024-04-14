import atexit

from flask import Flask, Response, jsonify

from src.rpi.rpi_controller import RPiController

app = Flask(__name__)
rpi_controller = RPiController()


def create_response(response: dict) -> Response:
    return jsonify({"response": response})


def cleanup():
    rpi_controller._cleanup()


@app.route("/health")
def health() -> Response:
    return create_response({"status": "healthy"})


@app.route("/board_mode")
def get_board_mode():
    return create_response({"message": f"Board mode: '{rpi_controller._board_mode}'..."})


@app.route("/board_mode/<string:mode>")
def set_board_mode(mode: str):
    rpi_controller._set_board_mode(board_mode=mode)
    return create_response({"message": f"Setting board mode to '{mode}'..."})


@app.route("/pin/<int:pin>")
def get_pin(pin: int):
    return create_response({"message": f"Pin '{pin}' mode: '{rpi_controller._pins[pin]}'"})


@app.route("/pin/<int:pin>/output/<string:val>")
def set_pin(pin: int, val: str):
    val = {"off": "high", "on": "low"}[val]

    if not rpi_controller._check_pin(pin):
        rpi_controller._setup_pin(pin_number=pin, mode="out", initial=val)
    else:
        rpi_controller._output_pin(pin_number=pin, value=val)

    return create_response({"message": f"Setting pin '{pin}' to: {val}"})


atexit.register(cleanup)
