from common import *
import time

HertzToSeconds = lambda hertz : 1 / hertz

STREAM_RATE_HZ = 20
STREAM_RATE_SECONDS = HertzToSeconds(STREAM_RATE_HZ)

MESSAGE_FILTER = ["HEARTBEAT", "STATUSTEXT", "COMMAND_ACK"]

Armed = False
Mode_Set = False

def filter_stream(connection):
  message = get_message(connection, blocking=False, printstd=False)
  if message and message.get_type() in MESSAGE_FILTER:
    print(message)
  return message

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")
  
  set_simulation(conn)

  start = time.time()
  while True:
    elapsed = time.time() - start

    setpoint_send(conn, x=0, y=0, z=-2.5)

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

    time.sleep(STREAM_RATE_SECONDS)
