from jinja2 import Environment, FileSystemLoader
from pathlib import Path

PX4_MODELS = (
  Path.home() / "PX4-Autopilot" /  "Tools" /  "simulation" /
  "gazebo-classic" / "sitl_gazebo-classic" / "models"
)

def create_drone_sdf():
  env = Environment(loader=FileSystemLoader(PX4_MODELS / "iris"))
  template = env.get_template("iris.sdf.jinja")

  print(template)
  return

if __name__ == "__main__":
  create_drone_sdf()