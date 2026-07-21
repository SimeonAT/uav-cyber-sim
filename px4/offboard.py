from common import *
import time

HertzToSeconds = lambda hertz : 1 / hertz

STREAM_RATE_HZ = 20
STREAM_RATE_SECONDS = HertzToSeconds(STREAM_RATE_HZ)

MESSAGE_FILTER = ["HEARTBEAT", "STATUSTEXT", "COMMAND_ACK", "LOCAL_POSITION_NED"]

Armed = False
Mode_Set = False

WAYPOINTS = [
  (0, 5, -2.5),
  (5, 5, -2.5),
  (5, 0, -2.5),
  (0, 0, -2.5)
]
WAYPOINT_REACHED_ACCURACY = 0.3

def filter_stream(connection):
  message = get_message(connection, blocking=False, printstd=False)
  # if message and message.get_type() in MESSAGE_FILTER:
  #   print(message)
  return message

def reached(current, waypoint):
  (x_c, y_c, z_c) = current
  (x_w, y_w, z_w) = waypoint
  dist = ((x_c - x_w)**2 + (y_c - y_w)**2 + (z_c - z_w)**2)**0.5
  return True if dist <= WAYPOINT_REACHED_ACCURACY else False

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")
  
  set_simulation(conn)
  waypoint_index = 0

  while True:
    waypoint = WAYPOINTS[waypoint_index]
    setpoint_send(conn, x=waypoint[0], y=waypoint[1], z=waypoint[2])

    if not Mode_Set:
      send_command(conn, mavutil.mavlink.MAV_CMD_DO_SET_MODE, confirmation=0,
                   param1=209, param2=6, param3=0, param4=0, param5=0, param6=0, param7=0)
    
    if not Armed:
      send_command(conn, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    message = filter_stream(conn)
    if not Mode_Set or not Armed:
      if message.get_type() == "COMMAND_ACK":
        if message.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE and \
          message.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
          Mode_Set = True

        if message.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM and \
          message.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
          Armed = True

    match message.get_type():
      case "LOCAL_POSITION_NED":
        if reached((message.x, message.y, message.z), waypoint):
          print(f"Reached Waypoint {waypoint}.")
          
          waypoint_index += 1
          if waypoint_index >= len(WAYPOINTS):
            print(f"Mission Complete.")
            break

      case _ : pass

    time.sleep(STREAM_RATE_SECONDS)
