from jinja2 import Environment, FileSystemLoader
from pathlib import Path

PX4_MODELS_DIR = (
  Path.home() / "PX4-Autopilot" /  "Tools" /  "simulation" /
  "gazebo-classic" / "sitl_gazebo-classic" / "models"
)

""" The required variables for `iris.sdf.jinja` are:
      1. mavlink_tcp_port (default = 4560)
      2. mavlink_udp_port (default = 14560)
      3. serial_enabled (default = 0)
      4. serial_device (default = /dev/ttyACM0)
      5. serial_baudrate (default = 921600)
      6. hil_mode (default = 0)
"""
def create_drone_sdf(sdf_path):
  env = Environment(loader=FileSystemLoader(sdf_path))
  template = env.get_template("iris.sdf.jinja")
  return template.render({
    "mavlink_tcp_port": 4560,
    "mavlink_udp_port": 14560,
    "serial_enabled": 0,
    "serial_device": "/dev/ttyACM0",
    "serial_baudrate": 921600,
    "hil_mode": 0
  })

if __name__ == "__main__":
  create_drone_sdf(PX4_MODELS_DIR / "iris")