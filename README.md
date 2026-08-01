# UAV-CYBER-SIM

## A Networked Multi-UAV Simulation Framework for Coordination and Cybersecurity Research

UAV-CYBER-SIM is a modular, distributed simulator for evaluating coordinated multi-UAV operations, ground control logic, and cybersecurity vulnerabilities. It integrates ArduPilot, Gazebo, QGroundControl, and PyMAVLink to enable realistic mission execution, MAVLink communication, plan approval, and testing of system-level resilience.

---

## About



Unmanned aerial vehicles (UAVs) are expected to play an essential role in the future of air mobility. Small UAVs are already being deployed for tasks such as package delivery, surveillance, and disaster response. These missions increasingly involve complex requirements, including dynamic flight planning, multi-operator coordination, networked communications, and secure operations.

<p align="center">
  <img src="readme_media/scenario.png" alt="Simulation Scenario" style="width:100%; max-width:900px;"/>
  <br/>
  <em>Example multi-UAV simulation scenario: eight UAVs operated by four private ground stations using MAVLink over 5G. Each UAV broadcasts Remote ID locally and submits its flight plan for external approval and deconfliction.</em>
</p>

To support this evolving ecosystem, UAV-CYBER-SIM offers a comprehensive testbed for simulating and analyzing multi-UAV operations. Each UAV is managed by its own ground control station and follows a pre-approved mission plan, reflecting realistic operator behavior. The simulator also supports remote identification broadcasting, MAVLink message exchange, plan validation workflows, and adversarial testing through cyberattack simulation. This makes it well suited for research in autonomy, communication infrastructure, and secure operations across a wide range of application domains.


---


## Architecture Diagram

<p align="center">
  <img src="readme_media/architecture.png" alt="Simulation Scenario" style="width:100%; max-width:900px;"/>
  <br/>
  <em>System architecture overview: distributed multi-UAV simulation with separate processes connected via UDP/TCP. Shown for two operators, each managing two UAVs from remote ground control stations.</em>
</p>

---

## Demo Simulation Videos


<div align="center">
  <img src="https://github.com/4belito/uav-cyber-sim/blob/auto-mode/readme_media/qgc.gif?raw=true" style="width:100%; max-width:900px;" />
  <p><em>QGroundControl</em></p>
</div>

<br>

<div align="center">
  <img src="https://github.com/4belito/uav-cyber-sim/blob/auto-mode/readme_media/gazebo.gif?raw=true" style="width:100%; max-width:900px;" />
  <p><em>Gazebo</em></p>
</div>


---

## Installation Instructions

**Note:** The installation instructions for this fork has been modified, and is thus different from the original version shown in [`4belito/uav-cyber-sim`](https://github.com/4belito/uav-cyber-sim).

As of now, it is *not* recommended to build and run the Docker image and container for this fork using the VSCode `devcontainer` CLI.

1. Build the Docker image for [uli-net-sim](https://github.com/brycethebjorkman/uli-net-sim).

2. Clone our fork of [`ardupilot_gazebo`](https://github.com/SimeonAT/ardupilot_gazebo/tree/parallel-simulation). Navigate to the forked repository and checkout the commit to the `parallel-simulation` branch:
```shell
cd ardupilot_gazebo
git checkout parallel-simulation
```

3. Clone our fork of [`PX4-Autopilot`](https://github.com/SimeonAT/PX4-Autopilot). Navigate to the forked repository and checkout the commit to the `uav-cyber-sim` branch:
```shell
cd PX4-Autopilot
git checkout uav-cyber-sim
```

4. Navigate to the `.devcontainer` directory and build the Docker image:
```shell
cd .devcontainer
docker build --tag "uav-cyber-sim" .
```

5. After the image has been built, launch the container with the following command:
```shell
docker run -u ubuntu \
  --gpus all \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e __NV_PRIME_RENDER_OFFLOAD=1 \
  -e __GLX_VENDOR_LIBRARY_NAME=nvidia \
  --env="DISPLAY" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="/dev/dri:/dev/dri:ro" \
  --volume="[Path to directory containing `uav-cyber-sim` repository]:/home/ubuntu/uav-cyber-sim" \
  --volume="[Path to directory containing `ardupilot_gazebo` repository]:/home/ubuntu/ardupilot_gazebo" \
  --volume="[Path to directory containing `PX4-Autopilot` repository]:/home/ubuntu/PX4-Autopilot" \
  --name uav-cyber-sim -d uav-cyber-sim:latest
```
**Do not** launch the container through SSH; otherwise, Gazebo will not be able to render. You must run this command on the same device that is running `uav-cyber-sim`, and hence, the Gazebo simulation environment.

6. VS Code's 'Dev Containers' extension can be then used to attach to a running container in order to run the example Jupyter notebooks. 

**If you encounter "cannot connect to display" error, run the following on your host system:**
```shell
xhost +local:
```

---

## Wireshark and MAVLink

If you would like to inspect MAVLink packets on Wireshark:

1. Navigate to the `px4` directory, and run `make wireshark`. This will set up the [MAVLink Wireshark Lua plugin](https://mavlink.io/en/guide/wireshark.html).

2. Start up by Wireshark by running the `wireshark` command in the container. The Wirshark GUI will then be displayed on your host system. Refer to the [MAVLink documentation](https://mavlink.io/en/guide/wireshark.html#view-traffic-on-wireshark) on how to inspect MAVLink packets in Wireshark.

**If the Wirshark user interface does not appear, run the following on your host system:**
```shell
xhost +local:
```
---

## Citation
If you use this simulator, please cite the original paper:

```
@inproceedings{diaz2026uavsim,
  title={Networked Simulation for Cybersecurity Evaluation of Small Unmanned Aircraft Systems in Dense Urban Environments},
  author={Diaz-Gonzalez, Abel and others},
  booktitle={AIAA SciTech 2026},
  year={2026}
  doi={10.2514/6.2026-1797}
}
```

---