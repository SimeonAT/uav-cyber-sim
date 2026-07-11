from pymavlink import mavutil
import mavtest

import time
from math import nan

ONBOARD_PORT = 14540
SLEEP_TIME_SECS = 1

# Start a connection listening on a UDP port
conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

conn.wait_heartbeat()
print(f"Heartbeat from system {conn.target_system} component {conn.target_component})")

# while True:
#   message = conn.recv_match(blocking=True)
#   print(message)
#   time.sleep(SLEEP_TIME_SECS)

conn.mav.command_long_send(conn.target_system, conn.target_component,
                           mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                           0, 0, 0, 0, nan, 0, 0, 10)