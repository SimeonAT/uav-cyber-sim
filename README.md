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

As of now, it is **not** recommended that you build and run the Docker image and container using the VSCode `devcontainer` CLI.

1. Build the Docker image for [uli-net-sim](https://github.com/brycethebjorkman/uli-net-sim).

2. Navigate to the `.devcontainer` directory and build the Docker container:
```shell
cd .devcontainer
docker build --tag "uav-cyber-sim" .
```

3. After the container has been built, launch the container with the following command:
```shell
docker run -u ubuntu --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --volume="/dev/dri:/dev/dri:ro" --name uav-cyber-sim -d uav-cyber-sim:latest
```

4. VS Code's 'Dev Containers' extension can be then used to attach to a running container in order to run the example Jupyter notebooks. 

**If you encounter "cannot connect to display" error, run the following on your host system:**
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