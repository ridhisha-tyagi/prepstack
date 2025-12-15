from typing import Literal

GuidanceMode = Literal["on", "off"]

def say(message: str, guidance: GuidanceMode = "on"):
    """
    Print a message only when guidance == 'on'.
    Used across Analytica so users can toggle verbosity.
    """
    if guidance == "on":
        print(message)
