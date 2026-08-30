"""
Simulation configuration parameters.

This module defines global settings used during simulation,
"""

HEARTBEAT_FREQUENCY: int = 1  # Hz
DATA_STREAM_FREQUENCY: int = 5  # Hz
REMOTE_ID_FREQUENCY: int = 5  # Hz
USE_NETWORK_SIM: bool = False

"""
UCI NOTE: To enable offboard (i.e. guided) mode, PX4 requires that setpoints
          be streamed at a frequency of >= 2 Hz.
          https://docs.px4.io/main/en/flight_modes/offboard#technical-summary
"""
SETPOINT_FREQUENCY: int = 2 # Hz