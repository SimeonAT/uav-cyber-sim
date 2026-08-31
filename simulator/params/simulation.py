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

""" 
This is the exact same type mask used in `exec_fn` in 
`planners/action/navigation.py`.
"""
SETPOINT_TYPE_MASK = int(0b110111111000)

""" The rate, in microseconds, to request a stream of Global Position messages from PX4.
    The value of this rate is the same as the default argument for the
    `msg_pos_interval` parameter in the `GoTo` class in `planners/action/navigation.py`.
"""
GLOBAL_POSITION_REQUEST_RATE_US = 100_000