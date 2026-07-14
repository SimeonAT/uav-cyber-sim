from pymavlink import mavutil

import time
from math import nan

ONBOARD_PORT = 14540
SLEEP_TIME_SECS = 1
TIMEOUT = None

class Waypoint:
  def __init__(self, seq, current, x, y, z):
    self.seq = seq
    self.frame = mavutil.mavlink.MAV_FRAME_LOCAL_ENU
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

def print_message(connection, message_names=None):
  message = connection.recv_match(type=message_names, blocking=True, timeout=TIMEOUT)
  if message:
    print(message)
  else:
    print(f"Failed to receive message: {message_names}")
  return message

def upload_mission(connection, waypoints):
  connection.mav.mission_count_send(connection.target_system, connection.target_component,
                                    len(waypoints))

  for waypoint in waypoints:
    print_message(connection, "MISSION_REQUEST")
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
      waypoint.param5,                       # Local X
      waypoint.param6,                       # Local Y
      waypoint.param7,                       # Local Z
      waypoint.mission_type                  # Mission Type
    )
  
  print_message(connection, "MISSION_ACK")
  return

def send_command(connection, command, confirmation, param1, param2, param3,
                 param4, param5, param6, param7):
  return connection.mav.command_long_send(connection.target_system, connection.target_component,
                                          command, confirmation, param1, param2, param3, param4,
                                          param5, param6, param7)

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")

  # Print the starting coordinates of the drone.
  send_command(conn, mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
               mavutil.mavlink.MAVLINK_MSG_ID_HOME_POSITION, 0, 0, 0, 0, 0, 0)
  print_message(conn, "HOME_POSITION")

  waypoints = []
  waypoints.append(Waypoint(0, 0, 42, -83, 10))
  waypoints.append(Waypoint(1, 0, 43, -90, 10))
  waypoints.append(Waypoint(2, 0, 42, -83, 5))

  upload_mission(conn, waypoints)

  send_command(conn, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
  print_message(conn, "COMMAND_ACK")

  send_command(conn, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  0, 0, 0, 0, nan, nan, nan, 50)
  print_message(conn, "COMMAND_ACK")

  time.sleep(10)

  send_command(conn, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)
  print_message(conn, "COMMAND_ACK")