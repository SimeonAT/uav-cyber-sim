from common import *

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")

  # Get the starting coordinates of the drone.
  send_command(conn, mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
               mavutil.mavlink.MAVLINK_MSG_ID_HOME_POSITION, 0, 0, 0, 0, 0, 0)
  home = get_message(conn, "HOME_POSITION")
  if home is None:
    raise Exception("Failed to get starting position of Drone")

  # Under the Global WGS84 standard, latitude and longitude are express in terms of 10**7.
  latitude = E7ToDeg(home.latitude)
  longitude = E7ToDeg(home.longitude)

  waypoints = []
  waypoints.append(
    Waypoint(0, 0, latitude + 0.0001, longitude + 0.0001, 2.5)
  )

  upload_mission(conn, waypoints)

  send_command(conn, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
  get_message(conn, "COMMAND_ACK")

  send_command(conn, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  0, 0, 0, 0, nan, nan, nan, 50)
  get_message(conn, "COMMAND_ACK")
  
  try:
    send_command(conn, mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)
    ack = get_message(conn, "COMMAND_ACK")
    if ack is None:
      raise Exception("Failed to receive ACK for MISSION_START command.")
    if ack.result != 0:
      raise Exception(f"COMMAND_ACK Error: {ack} with Status Code {ack.result}.")

    for waypoint in waypoints:
      get_message(conn, "MISSION_ITEM_REACHED",
                  condition = f"MISSION_ITEM_REACHED.seq == {waypoint.seq}")

  finally:
    print("Landing Drone.")
    send_command(conn, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)
    get_message(conn, "COMMAND_ACK")