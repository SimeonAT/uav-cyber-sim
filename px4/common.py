import os
os.environ['MAVLINK_DIALECT'] = 'development'
from pymavlink import mavutil
assert(mavutil.mavlink.__name__ == "pymavlink.dialects.v10.development")

from math import nan

ONBOARD_PORT = 14540
SLEEP_TIME_SECS = 1
TIMEOUT = None

E7ToDeg = lambda e7 : e7 / 10**7

class Waypoint:
  def __init__(self, seq, current, x, y, z):
    self.seq = seq
    self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
    self.mission_type = 0

    self.current = current
    self.auto = 1
    self.param1 = 0.0
    self.param2 = 2.00
    self.param3 = 20.00
    self.param4 = nan
    self.param5 = x
    self.param6 = y
    self.param7 = z
    return

def get_message(connection, message_names=None, condition=None):
  message = connection.recv_match(type=message_names, blocking=True, 
                                  timeout=TIMEOUT, condition=condition)
  if message:
    print(message)
  else:
    print(f"Failed to receive message: {message_names}")
  return message

def upload_mission(connection, waypoints):
  connection.mav.mission_count_send(connection.target_system, connection.target_component,
                                    len(waypoints))
  get_message(connection, "MISSION_REQUEST")

  for i in range(len(waypoints)):
    waypoint = waypoints[i]
    connection.mav.mission_item_send(
      connection.target_system,              # Target System
      connection.target_component,           # Target Component
      waypoint.seq,                          # Sequence
      waypoint.frame,                        # Frame
      waypoint.command,                      # Command
      waypoint.current,                      # Current
      waypoint.auto,                         # Autocontinue
      waypoint.param1,                       # Hold Time
      waypoint.param2,                       # Accept Radius
      waypoint.param3,                       # Pass Radius
      waypoint.param4,                       # Yaw
      waypoint.param5,                       # Local X / Latitude
      waypoint.param6,                       # Local Y / Longitude
      waypoint.param7,                       # Local Z / Altitude
      waypoint.mission_type                  # Mission Type
    )

    if i < len(waypoints) - 1:
      get_message(connection, "MISSION_REQUEST")
  
  get_message(connection, "MISSION_ACK")
  return

def send_command(connection, command, confirmation, param1, param2, param3,
                 param4, param5, param6, param7):
  return connection.mav.command_long_send(connection.target_system, connection.target_component,
                                          command, confirmation, param1, param2, param3, param4,
                                          param5, param6, param7)