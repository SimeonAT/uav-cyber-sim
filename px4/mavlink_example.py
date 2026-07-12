"""
All of the code in this source file comes from the `mavlink_test.py` example shown in the
following YouTube tutorial: https://youtu.be/pAAN055XCxA?si=0zu3phLbdf67Ow4x
"""
import math
from pymavlink import mavutil

# Class for formatting the Mission Item.
class Mission_Item:
  def __init__(self, i, current, x, y, z):
    self.seq = i

    # Use Global Latitude and Logitude for position data
    self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT

    #Move to the waypoint
    self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

    self.current = current
    self.auto = 1
    self.param1 = 0.0
    self.param2 = 2.00
    self.param3 = 20.00
    self.param4 = math.nan
    self.param5 = x
    self.param6 = y
    self.param7 = z

     #The MAV_MISSION_TYPE value for MAV_MISSION_TYPE_MISSION
    self.mission_type = 0
    return


""" Move the Drone """
def arm(the_connection):
  print("-- Arming")
  the_connection.mav.command_long_send(the_connection.target_system,
                                       the_connection.target_component,
                                       mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                       0, 1, 0, 0, 0, 0, 0, 0, 0)
  ack(the_connection, "COMMAND_ACK")
  return

""" Takeoff the Drone """
def takeoff(the_connection):
  print("Takeoff INITIATED")
  the_connection.mav.command_long_send(the_connection.target_system,
                                       the_connection.target_component,
                                       mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                       0, 0, 0, 0, math.nan, 0, 0, 0, 0)
  ack(the_connection, "COMMAND_ACK")
  return

""" Upload the mission items to the drone """
def upload_mission(the_connection, mission_items):
  n = len(mission_items)
  print("-- Sending Message Out")
  the_connection.mav.mission_count_send(the_connection.target_system,
                                        the_connection.target_component,
                                        n, 0)
  ack(the_connection, "MISSION_REQUEST")

  for waypoint in mission_items:
    print("-- Creating a Waypoint")
    the_connection.mav.mission_item_send(
      the_connection.target_system,          # Target System
      the_connection.target_component,       # Target Component
      waypoint.seq,                          # Sequence
      waypoint.frame,                        # Frame
      waypoint.command,                      # Command
      waypoint.current,                      # Curent
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
  
    if waypoint != mission_items[n - 1]:
      ack(the_connection, "MISSION_REQUEST")
  
  ack(the_connection, "MISSION_ACK")
  return

""" Send message for the drone to return to the launch point. """
def set_return(the_connection):
  print("-- Set Return to Launch")
  the_connection.mav.command_long_send(the_connection.target_system,
                                       the_connection.target_component,
                                       mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0)
  ack(the_connection, "COMMAND_ACK")
  return

""" Start Mission """
def start_mission(the_connection):
  print("--- Mission Start")
  the_connection.mav.command_long_send(the_connection.target_system,
                                       the_connection.target_component,
                                       mavutil.mavlink.MAV_CMD_MISSION_START,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0)
  ack(the_connection, "COMMAND_ACK")
  return

""" Acknowledgement from the Drone """
def ack(the_connection, keyword):
  print(" -- Message Read " + str(
    the_connection.recv_match(type=keyword, blocking=True)
  ))
  return

""" Main Function """
if __name__ == "__main__":
  print("-- Program Started")
  the_connection = mavutil.mavlink_connection("udpin:localhost:14540")

  while the_connection.target_system == 0:
    print("-- Checking Heartbeat")
    the_connection.wait_heartbeat()
    print(f"Heartbeat from system (system {the_connection.target_system} component {the_connection.target_component})")

  mission_waypoints = []
  mission_waypoints.append(Mission_Item(0, 0, 42, -83, 10))
  mission_waypoints.append(Mission_Item(1, 0, 43, -90, 10))
  mission_waypoints.append(Mission_Item(2, 0, 42, -83, 5))

  upload_mission(the_connection, mission_waypoints)
  
  arm(the_connection)

  takeoff(the_connection)

  start_mission(the_connection)

  for mission_item in mission_waypoints:
    print(" -- Message Read " + str(
      the_connection.recv_match(
        type="MISSION_ITEM_REACHED", 
        condition = f"MISSION_ITEM_REACHED.seq == {mission_item.seq}",
        blocking = True
      )
    ))