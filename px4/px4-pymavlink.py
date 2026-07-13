from pymavlink import mavutil

import time
from math import nan

ONBOARD_PORT = 14540
SLEEP_TIME_SECS = 1

def send_command(connection, command, confirmation, param1, param2, param3,
                 param4, param5, param6, param7):
  return conn.mav.command_long_send(connection.target_system, connection.target_component,
                                    command, confirmation, param1, param2, param3, param4,
                                    param5, param6, param7)

def print_message(connection, message_names=None):
  message = connection.recv_match(type=message_names, blocking=True)
  print(message)
  return message

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component})")

  send_command(conn, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
  print_message(conn, message_names="COMMAND_ACK")

  send_command(conn, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  0, 0, 0, 0, nan, nan, nan, 50)
  print_message(conn, message_names="COMMAND_ACK")

  time.sleep(10)

  send_command(conn, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)
  print_message(conn)