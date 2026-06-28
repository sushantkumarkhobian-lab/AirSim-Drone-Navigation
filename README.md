# AirSim Drone Navigation

Autonomous drone navigation, environment simulation, and flight analytics system built using **Microsoft AirSim**, **Python**, and **Unreal Engine**.

This project enables autonomous drone navigation through waypoints and predefined paths while collecting detailed flight analytics for performance evaluation and comparison. The system supports wind simulation, yaw control, time-synchronized flight, smooth takeoff and landing, automated reporting, and navigation performance comparison.

---

# Repository

```bash
git clone https://github.com/sushantkumarkhobian-lab/AirSim-Drone-Navigation.git
cd AirSim-Drone-Navigation
```

---

# Project Overview

The project is divided into three major modules:

## 1. Navigation Module (`navigation.py`)

Handles:

- Autonomous drone takeoff
- Waypoint navigation
- Square path navigation
- Rectangle path navigation
- Circular path navigation
- Yaw control
- Time-synchronized navigation
- Adaptive velocity control
- Wind compensation
- Smooth landing
- Flight analytics logging

---

## 2. Environment Module (`environment.py`)

Handles:

- Wind simulation
- Rain simulation
- Fog simulation
- Snow simulation
- Dust simulation
- Mixed weather simulation

Allows testing navigation performance under different environmental conditions.

---

## 3. Analysis Module (`analysis.py`)

Handles:

- Flight log comparison
- Performance analysis
- Automated reporting
- Radar chart generation
- Graph generation
- Navigation accuracy evaluation
- Controller performance comparison

---

# Features

## Navigation Features

✔ Autonomous Waypoint Navigation

✔ Square Path Navigation

✔ Rectangle Path Navigation

✔ Circular Path Navigation

✔ Time-Synchronized Flight

✔ Adaptive Velocity Control

✔ Wind Compensation

✔ Yaw Control

✔ Smooth Takeoff

✔ Smooth Landing

---

## Environment Features

✔ Wind Simulation

✔ Rain Simulation

✔ Fog Simulation

✔ Snow Simulation

✔ Dust Simulation

✔ Mixed Weather Simulation

---

## Analytics Features

✔ CSV Flight Logging

✔ Position Error Analysis

✔ Time Error Analysis

✔ Speed Analysis

✔ Battery Usage Estimation

✔ Path Efficiency Analysis

✔ Performance Comparison Reports

✔ Radar Chart Visualization

✔ Automated Winner Selection

---

# Technologies Used

- Python 3.11
- Microsoft AirSim
- Unreal Engine
- NumPy
- Pandas
- Matplotlib
- OpenCV
- MsgPack RPC

---

# Repository Structure

```text
AirSim-Drone-Navigation/
│
├── navigation.py
├── environment.py
├── analysis.py
│
├── config/
│   └── settings.json
│
├── requirements.txt
├── README.md
│
├── sample_data/
│   ├── advanced_drone_navigation_analytics1.csv
│   └── advanced_drone_navigation_analytics3.csv
│
├── sample_results/
    └── results13/

```

---

# Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/sushantkumarkhobian-lab/AirSim-Drone-Navigation.git
cd AirSim-Drone-Navigation
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```text
airsim==1.8.1
numpy==2.4.5
pandas==3.0.3
matplotlib==3.10.9
opencv-contrib-python==4.13.0.92
msgpack-rpc-python==0.4.1
```

---

# AirSim Setup

## Step 1: Download AirSim Blocks

Download AirSim Blocks from:

https://github.com/microsoft/AirSim/releases

Download:

```text
Blocks.zip
```

Extract the ZIP file.

---

## Step 2: Locate Blocks.exe

After extraction:

```text
Downloads
└── Blocks
    └── Blocks
        └── WindowsNoEditor
            └── Blocks
                └── Binaries
                    └── Win64
                        └── Blocks.exe
```

Example:

```text
C:\Users\<YourUsername>\Downloads\Blocks\Blocks\WindowsNoEditor\Blocks\Binaries\Win64\Blocks.exe
```

Launch:

```text
Blocks.exe
```

Wait for the simulation to load completely.

---

## Step 3: Configure AirSim

Create:

```text
Documents\AirSim\
```

Example:

```text
C:\Users\<YourUsername>\Documents\AirSim\
```

Copy:

```text
config/settings.json
```

from this repository into:

```text
Documents\AirSim\
```

Final structure:

```text
Documents
└── AirSim
    └── settings.json
```

---

## Step 4: Verify Connection

Launch:

```text
Blocks.exe
```

Run:

```bash
python navigation.py
```

Expected output:

```text
Connected!
Client Ver: 1
Server Ver: 1
```

The drone should arm automatically and perform takeoff.

---

# Navigation Modes

## Waypoint Navigation

Predefined mission:

```text
(0, 0, -5)
(10, 0, -5)
(10, 10, -5)
(0, 10, -5)
(0, 0, -5)
```

---

## Square Path Navigation

User Inputs:

- Height
- Side Length

Drone automatically generates a square trajectory.

---

## Rectangle Path Navigation

User Inputs:

- Height
- Length
- Breadth

Drone automatically generates a rectangular trajectory.

---

## Circular Path Navigation

User Inputs:

- Height
- Radius

Drone automatically generates a circular trajectory.

---

# Environment Simulation

Weather conditions can be enabled using `environment.py`.

Supported environments:

- Wind
- Rain
- Fog
- Snow
- Dust
- Mixed Environment

Example:

```python
windy_environment(client)
```

---

# Wind Configuration

Wind values are configured inside:

```text
config/settings.json
```

Example:

```json
"Wind": {
    "X": 8,
    "Y": 2,
    "Z": 0
}
```

Disable wind:

```json
"Wind": {
    "X": 0,
    "Y": 0,
    "Z": 0
}
```

---

# Running Navigation

Start AirSim Blocks.

Run:

```bash
python navigation.py
```

Menu:

```text
1 -> Waypoint Navigation
2 -> Path Navigation
3 -> Exit
```

Path Navigation Menu:

```text
1 -> Square Path
2 -> Rectangle Path
3 -> Circle Path
4 -> Back
```

Follow terminal prompts to configure the mission.

---

# Flight Analytics

The system automatically records:

- Target Position
- Actual Position
- Desired Time
- Actual Time
- Time Error
- Mission Elapsed Time
- Real World Clock Time
- Distance Travelled
- Average Speed
- Yaw Information
- Final Position Error
- Maximum Position Error
- Estimated Wind Disturbance
- Battery Usage Estimate
- Path Efficiency

Generated output files:

```text
advanced_drone_navigation_analytics1.csv
advanced_drone_navigation_analytics2.csv
advanced_drone_navigation_analytics3.csv
...
```

Each run automatically generates a new numbered CSV file.

---

# Running Analysis

Run:

```bash
python analysis.py
```

Example:

```text
Enter first file number: 1
Enter second file number: 3
```

Generated folder:

```text
results13/
```

---

# Analysis Outputs

## Reports

```text
clean_comparison_summary.csv
performance_scorecard.csv
analysis_report.txt
```

## Graphs

```text
actual_time_comparison.png
time_error_comparison.png
final_position_error_comparison.png
max_position_error_comparison.png
average_speed_comparison.png
battery_remaining_comparison.png
average_metric_comparison_bar.png
performance_radar_chart.png
```

---

# Example Workflow

1. Launch AirSim Blocks
2. Run `navigation.py`
3. Complete a flight mission
4. Generate flight CSV
5. Run another mission
6. Generate second flight CSV
7. Run `analysis.py`
8. Compare both flight logs
9. Review generated reports and graphs

---

# Sample Data and Results

The repository includes:

```text
sample_data/
```

Sample flight logs.

and

```text
sample_results/
```

Example comparison reports and generated graphs.

---

# Future Improvements

- Custom Unreal Engine Environments
- Multiple Drone Models
- Obstacle Avoidance
- Dynamic Path Planning
- Multi-Drone Coordination
- Advanced PID Controller Tuning
- Real-Time Dashboard Integration
- GPS-Based Navigation
- Real Drone Deployment

---

# Screenshot

<img width="1917" height="1079" alt="image" src="https://github.com/user-attachments/assets/73c3c069-3dc4-4c05-bdea-4b7e21d5feca" />

---

# Author

**Sushant Kumar Khobian**

B.E. Computer Science & Engineering (IoT, Blockchain & Cybersecurity)

Xavier Institute of Engineering

Mumbai, India
