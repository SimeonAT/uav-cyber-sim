from pymavlink import mavutil
import mavtest

import time
from math import nan

ONBOARD_PORT = 14540
SLEEP_TIME_SECS = 1

def send_command(connection, command, confirmation, param1, param2, param3,
                 param4, param5, param6, param7):
  return conn.mav.command_long_send(connection.target_system, connection.target_component,
                                    command, confirmation, param1, param2, param3, param4,
                                    param5, param6, param7)

def ack(connection, message_names):
  ack = connection.recv_match(type=message_names, blocking=True)
  print(ack)
  return ack

if __name__ == "__main__":
  # Start a connection listening on a UDP port
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component})")

  # Arm command
  send_command(conn, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
  ack(conn, "COMMAND_ACK")

  # Takeoff command
  send_command(conn, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  0, 0, 0, 0, nan, 0, 0, 10)
  ack(conn, "COMMAND_ACK")

  # while True:
  #   message = conn.recv_match(blocking=True)
  #   print(message)
  #   time.sleep(SLEEP_TIME_SECS)