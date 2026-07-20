from common import *
import time

HertzToSeconds = lambda hertz : 1 / hertz

STREAM_RATE_HZ = 20
STREAM_RATE_SECONDS = HertzToSeconds(STREAM_RATE_HZ)

MESSAGE_FILTER = ["HEARTBEAT", "STATUSTEXT", "COMMAND_ACK"]

Armed = False
Mode_Set = False

def print_stream(connection):
  message = get_message(connection, blocking=False, printstd=False)
  if message and message.get_type() in MESSAGE_FILTER:
    print(message)
  return

if __name__ == "__main__":
  conn = mavutil.mavlink_connection(f'udpin:localhost:{ONBOARD_PORT}')

  conn.wait_heartbeat()
  print(f"Heartbeat from system {conn.target_system} component {conn.target_component}")

  start = time.time()
  while True:
    elapsed = time.time() - start
    print_stream(conn)

    setpoint_send(conn, x=0, y=0, z=-2.5)

    if not Mode_Set:
      send_command(conn, mavutil.mavlink.MAV_CMD_DO_SET_MODE, confirmation=0,
                   param1=209, param2=6, param3=0, param4=0, param5=0, param6=0, param7=0)
    
    # if not Armed:
    #   send_command(conn, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    if not Mode_Set or not Armed:
      ack = get_message(conn, "COMMAND_ACK", blocking=False, printstd=True)
      if ack:
        if ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE and \
          ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
          Mode_Set = True

        # if ack.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM and \
        #   ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        #   Armed = True

    time.sleep(STREAM_RATE_SECONDS)
