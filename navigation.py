import airsim
import time
import csv
import math
from datetime import datetime
import os


# ==============================
# CONFIGURATION
# ==============================

base_name = "advanced_drone_navigation_analytics"

counter = 1

while os.path.exists(f"{base_name}{counter}.csv"):
    counter += 1

CSV_FILE = f"{base_name}{counter}.csv"

BASE_SPEED_LIMIT = 6.0
MIN_SPEED = 0.2

CONTROL_DT = 0.05

KP_POSITION = 0.8
KD_DAMPING = 0.4

WIND_ADAPT_GAIN = 0.35
WIND_COMP_GAIN = 0.8

FINAL_HOLD_TIME = 0.0
BATTERY_START = 100.0

TAKEOFF_HEIGHT = 5.0
TAKEOFF_TIME = 5.0
LANDING_TIME = 6.0


# ==============================
# MENU FUNCTIONS
# ==============================

def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Enter a value greater than 0.")
                continue

            return value

        except ValueError:
            print("Invalid input. Enter a number.")


def get_navigation_mode():
    print("\n========== DRONE NAVIGATION MENU ==========")
    print("1. Waypoint Navigation")
    print("2. Path Navigation")
    print("3. Exit")
    print("==========================================")

    return input("Select option: ")


def get_path_type():
    print("\n========== PATH NAVIGATION MENU ==========")
    print("1. Square Path")
    print("2. Rectangle Path")
    print("3. Circle Path")
    print("4. Back")
    print("=========================================")

    return input("Select path type: ")


# ==============================
# PATH GENERATION
# ==============================

def generate_square_path(height, side_length):
    z = -abs(height)

    return [
        ((0, 0, z), 5, 0),
        ((side_length, 0, z), 5, 90),
        ((side_length, side_length, z), 5, 180),
        ((0, side_length, z), 5, 270),
        ((0, 0, z), 5, 360)
    ]


def generate_rectangle_path(height, length, breadth):
    z = -abs(height)

    return [
        ((0, 0, z), 5, 0),
        ((length, 0, z), 5, 90),
        ((length, breadth, z), 5, 180),
        ((0, breadth, z), 5, 270),
        ((0, 0, z), 5, 360)
    ]


def generate_circle_path(height, radius, total_time, points=120):
    z = -abs(height)
    waypoints = []

    segment_time = total_time / points

    for i in range(points + 1):
        angle = 2 * math.pi * i / points

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        yaw = math.degrees(angle) % 360

        waypoints.append(((x, y, z), segment_time, yaw))

    return waypoints


def get_waypoints_from_user():
    mode = get_navigation_mode()

    if mode == "1":
        return [
            ((10, 0, -5), 5, 90),
            ((10, 10, -5), 5, 180),
            ((0, 10, -5), 5, 270),
            ((0, 0, -5), 5, 360)
        ], "Waypoint Navigation"

    elif mode == "2":
        path_type = get_path_type()

        if path_type == "1":
            height = get_float("Enter height for square path in meters: ")
            side = get_float("Enter square side length in meters: ")

            return generate_square_path(height, side), "Square Path Navigation"

        elif path_type == "2":
            height = get_float("Enter height for rectangle path in meters: ")
            length = get_float("Enter rectangle length in meters: ")
            breadth = get_float("Enter rectangle breadth in meters: ")

            return generate_rectangle_path(height, length, breadth), "Rectangle Path Navigation"

        elif path_type == "3":
            height = get_float("Enter height for circle path in meters: ")
            radius = get_float("Enter circle radius in meters: ")
            total_time = get_float("Enter total time for circle path in seconds: ")

            return generate_circle_path(height, radius, total_time), "Circle Path Navigation"

        elif path_type == "4":
            return get_waypoints_from_user()

        else:
            print("Invalid option.")
            return get_waypoints_from_user()

    elif mode == "3":
        return None, "Exit"

    else:
        print("Invalid option.")
        return get_waypoints_from_user()


# ==============================
# HELPER FUNCTIONS
# ==============================

def real_date():
    return datetime.now().strftime("%Y-%m-%d")


def real_time():
    return datetime.now().strftime("%H:%M:%S")


def real_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_position(client):
    state = client.getMultirotorState()
    pos = state.kinematics_estimated.position

    return pos.x_val, pos.y_val, pos.z_val


def get_velocity(client):
    state = client.getMultirotorState()
    vel = state.kinematics_estimated.linear_velocity

    return vel.x_val, vel.y_val, vel.z_val


def distance_3d(x1, y1, z1, x2, y2, z2):
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2 +
        (z2 - z1) ** 2
    )


def clamp_velocity(vx, vy, vz):
    speed = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

    if speed > BASE_SPEED_LIMIT:
        scale = BASE_SPEED_LIMIT / speed

        vx *= scale
        vy *= scale
        vz *= scale

    return vx, vy, vz


def estimate_battery_usage(distance, avg_speed, position_error):
    return (distance * 0.15) + (avg_speed * 0.4) + (position_error * 0.25)


# ==============================
# TIME-SYNCED ADAPTIVE MOVEMENT
# ==============================

def timed_move_to_waypoint(client, target_x, target_y, target_z, desired_time):
    start_time = time.time()

    start_x, start_y, start_z = get_position(client)

    prev_x = start_x
    prev_y = start_y
    prev_z = start_z

    total_distance = 0
    max_error = 0

    estimated_wind_x = 0
    estimated_wind_y = 0
    estimated_wind_z = 0

    velocity_sum_x = 0
    velocity_sum_y = 0
    velocity_sum_z = 0

    control_steps = 0

    while True:
        now = time.time()

        elapsed = now - start_time
        remaining_time = desired_time - elapsed

        if remaining_time <= 0:
            break

        current_x, current_y, current_z = get_position(client)
        current_vx, current_vy, current_vz = get_velocity(client)

        error_x = target_x - current_x
        error_y = target_y - current_y
        error_z = target_z - current_z

        position_error = math.sqrt(
            error_x ** 2 +
            error_y ** 2 +
            error_z ** 2
        )

        max_error = max(max_error, position_error)

        moved = distance_3d(
            prev_x,
            prev_y,
            prev_z,
            current_x,
            current_y,
            current_z
        )

        total_distance += moved

        required_vx = error_x / max(remaining_time, CONTROL_DT)
        required_vy = error_y / max(remaining_time, CONTROL_DT)
        required_vz = error_z / max(remaining_time, CONTROL_DT)

        drift_x = current_vx - required_vx
        drift_y = current_vy - required_vy
        drift_z = current_vz - required_vz

        estimated_wind_x = (
            (1 - WIND_ADAPT_GAIN) * estimated_wind_x +
            WIND_ADAPT_GAIN * drift_x
        )

        estimated_wind_y = (
            (1 - WIND_ADAPT_GAIN) * estimated_wind_y +
            WIND_ADAPT_GAIN * drift_y
        )

        estimated_wind_z = (
            (1 - WIND_ADAPT_GAIN) * estimated_wind_z +
            WIND_ADAPT_GAIN * drift_z
        )

        vx = (
            (KP_POSITION * required_vx) -
            (KD_DAMPING * current_vx) -
            (WIND_COMP_GAIN * estimated_wind_x)
        )

        vy = (
            (KP_POSITION * required_vy) -
            (KD_DAMPING * current_vy) -
            (WIND_COMP_GAIN * estimated_wind_y)
        )

        vz = (
            (KP_POSITION * required_vz) -
            (KD_DAMPING * current_vz) -
            (WIND_COMP_GAIN * estimated_wind_z)
        )

        vx, vy, vz = clamp_velocity(vx, vy, vz)

        velocity_sum_x += vx
        velocity_sum_y += vy
        velocity_sum_z += vz

        control_steps += 1

        command_duration = min(CONTROL_DT, remaining_time)

        client.moveByVelocityAsync(
            vx,
            vy,
            vz,
            command_duration
        ).join()

        prev_x = current_x
        prev_y = current_y
        prev_z = current_z

    if FINAL_HOLD_TIME > 0:
        client.moveByVelocityAsync(
            0,
            0,
            0,
            FINAL_HOLD_TIME
        ).join()

    end_time = time.time()

    actual_time = end_time - start_time

    final_x, final_y, final_z = get_position(client)

    final_error = distance_3d(
        final_x,
        final_y,
        final_z,
        target_x,
        target_y,
        target_z
    )

    total_distance += distance_3d(
        prev_x,
        prev_y,
        prev_z,
        final_x,
        final_y,
        final_z
    )

    avg_vx = velocity_sum_x / control_steps if control_steps else 0
    avg_vy = velocity_sum_y / control_steps if control_steps else 0
    avg_vz = velocity_sum_z / control_steps if control_steps else 0

    return {
        "actual_x": final_x,
        "actual_y": final_y,
        "actual_z": final_z,
        "actual_time": actual_time,
        "final_error": final_error,
        "max_error": max_error,
        "total_distance": total_distance,
        "estimated_wind_x": estimated_wind_x,
        "estimated_wind_y": estimated_wind_y,
        "estimated_wind_z": estimated_wind_z,
        "avg_vx": avg_vx,
        "avg_vy": avg_vy,
        "avg_vz": avg_vz,
        "control_steps": control_steps
    }


# ==============================
# SMOOTH TAKEOFF
# ==============================

def smooth_takeoff(client):
    print("\nSmooth takeoff started...")

    start_time = time.time()

    start_x, start_y, start_z = get_position(client)

    client.takeoffAsync().join()

    result = timed_move_to_waypoint(
        client,
        start_x,
        start_y,
        -abs(TAKEOFF_HEIGHT),
        TAKEOFF_TIME
    )

    end_time = time.time()

    return {
        "start_time": start_time,
        "end_time": end_time,
        "duration": end_time - start_time,
        "start_x": start_x,
        "start_y": start_y,
        "start_z": start_z,
        "actual_x": result["actual_x"],
        "actual_y": result["actual_y"],
        "actual_z": result["actual_z"],
        "target_x": start_x,
        "target_y": start_y,
        "target_z": -abs(TAKEOFF_HEIGHT),
        "error": result["final_error"],
        "distance": result["total_distance"],
        "control_steps": result["control_steps"]
    }


# ==============================
# SMOOTH LANDING
# ==============================

def smooth_landing(client):
    print("\nSmooth landing started...")

    start_time = time.time()

    start_x, start_y, start_z = get_position(client)

    result = timed_move_to_waypoint(
        client,
        start_x,
        start_y,
        -0.5,
        LANDING_TIME
    )

    client.landAsync().join()

    end_time = time.time()

    final_x, final_y, final_z = get_position(client)

    return {
        "start_time": start_time,
        "end_time": end_time,
        "duration": end_time - start_time,
        "start_x": start_x,
        "start_y": start_y,
        "start_z": start_z,
        "target_x": start_x,
        "target_y": start_y,
        "target_z": 0,
        "actual_x": final_x,
        "actual_y": final_y,
        "actual_z": final_z,
        "error": abs(final_z - 0),
        "distance": result["total_distance"],
        "control_steps": result["control_steps"]
    }


# ==============================
# LOG SPECIAL PHASES
# ==============================

def add_phase_log(
    trajectory_data,
    mission_name,
    phase_name,
    phase_result,
    battery_level
):
    duration = phase_result["duration"]

    avg_speed = (
        phase_result["distance"] / duration
        if duration > 0
        else 0
    )

    trajectory_data.append([
        mission_name,
        phase_name,
        phase_result["target_x"],
        phase_result["target_y"],
        phase_result["target_z"],
        round(phase_result["actual_x"], 3),
        round(phase_result["actual_y"], 3),
        round(phase_result["actual_z"], 3),
        round(duration, 3),
        round(duration, 3),
        0,
        round(duration, 3),
        datetime.fromtimestamp(phase_result["start_time"]).strftime("%Y-%m-%d"),
        datetime.fromtimestamp(phase_result["start_time"]).strftime("%H:%M:%S"),
        datetime.fromtimestamp(phase_result["end_time"]).strftime("%Y-%m-%d"),
        datetime.fromtimestamp(phase_result["end_time"]).strftime("%H:%M:%S"),
        datetime.fromtimestamp(phase_result["end_time"]).strftime("%Y-%m-%d %H:%M:%S"),
        round(phase_result["distance"], 3),
        round(phase_result["distance"], 3),
        round(avg_speed, 3),
        0,
        0,
        round(phase_result["error"], 3),
        round(phase_result["error"], 3),
        0,
        0,
        0,
        0,
        0,
        0,
        phase_result["control_steps"],
        100,
        0,
        round(battery_level, 2)
    ])


# ==============================
# MISSION FUNCTION
# ==============================

def run_mission(client, waypoints, mission_name):
    client.enableApiControl(True)
    client.armDisarm(True)

    trajectory_data = []

    battery_level = BATTERY_START

    takeoff_result = smooth_takeoff(client)

    add_phase_log(
        trajectory_data,
        mission_name,
        "TAKEOFF",
        takeoff_result,
        battery_level
    )

    mission_start_time = time.time()

    current_x, current_y, current_z = get_position(client)

    for index, (waypoint, desired_time, target_yaw) in enumerate(
        waypoints,
        start=1
    ):
        target_x, target_y, target_z = waypoint

        print("\n===================================")
        print("Mission:", mission_name)
        print("Waypoint:", index)
        print("Target:", waypoint)
        print("Yaw:", round(target_yaw, 2))
        print("Desired Segment Time:", desired_time, "sec")

        yaw_start = time.time()

        if mission_name not in ["Circle Path Navigation", "Spiral Climb Navigation"]: 
            client.rotateToYawAsync(target_yaw, timeout_sec=0.5).join()

        yaw_end = time.time()

        yaw_time = yaw_end - yaw_start

        segment_start_time = time.time()

        result = timed_move_to_waypoint(
            client,
            target_x,
            target_y,
            target_z,
            desired_time
        )

        segment_end_time = time.time()

        actual_x = result["actual_x"]
        actual_y = result["actual_y"]
        actual_z = result["actual_z"]

        actual_time_taken = segment_end_time - segment_start_time

        mission_elapsed_time = segment_end_time - mission_start_time

        direct_distance = distance_3d(
            current_x,
            current_y,
            current_z,
            target_x,
            target_y,
            target_z
        )

        avg_speed = (
            result["total_distance"] / actual_time_taken
            if actual_time_taken > 0
            else 0
        )

        battery_used = estimate_battery_usage(
            result["total_distance"],
            avg_speed,
            result["final_error"]
        )

        battery_level = max(
            0,
            battery_level - battery_used
        )

        path_efficiency = 0

        if result["total_distance"] > 0:
            path_efficiency = (
                direct_distance / result["total_distance"]
            ) * 100

        time_error = actual_time_taken - desired_time

        trajectory_data.append([
            mission_name,
            index,
            target_x,
            target_y,
            target_z,
            round(actual_x, 3),
            round(actual_y, 3),
            round(actual_z, 3),
            desired_time,
            round(actual_time_taken, 3),
            round(time_error, 3),
            round(mission_elapsed_time, 3),
            datetime.fromtimestamp(segment_start_time).strftime("%Y-%m-%d"),
            datetime.fromtimestamp(segment_start_time).strftime("%H:%M:%S"),
            datetime.fromtimestamp(segment_end_time).strftime("%Y-%m-%d"),
            datetime.fromtimestamp(segment_end_time).strftime("%H:%M:%S"),
            datetime.fromtimestamp(segment_end_time).strftime("%Y-%m-%d %H:%M:%S"),
            round(direct_distance, 3),
            round(result["total_distance"], 3),
            round(avg_speed, 3),
            round(target_yaw, 2),
            round(yaw_time, 3),
            round(result["final_error"], 3),
            round(result["max_error"], 3),
            round(result["estimated_wind_x"], 3),
            round(result["estimated_wind_y"], 3),
            round(result["estimated_wind_z"], 3),
            round(result["avg_vx"], 3),
            round(result["avg_vy"], 3),
            round(result["avg_vz"], 3),
            result["control_steps"],
            round(path_efficiency, 2),
            round(battery_used, 2),
            round(battery_level, 2)
        ])

        print("Reached Waypoint:", index)
        print("Actual Position:", round(actual_x, 2), round(actual_y, 2), round(actual_z, 2))
        print("Actual Segment Time:", round(actual_time_taken, 3), "sec")
        print("Real World Time:", datetime.fromtimestamp(segment_end_time).strftime("%Y-%m-%d %H:%M:%S"))
        print("Time Error:", round(time_error, 3), "sec")
        print("Final Position Error:", round(result["final_error"], 3), "m")
        print("Battery Remaining:", round(battery_level, 2), "%")

        current_x = actual_x
        current_y = actual_y
        current_z = actual_z

    landing_result = smooth_landing(client)

    add_phase_log(
        trajectory_data,
        mission_name,
        "LANDING",
        landing_result,
        battery_level
    )

    return trajectory_data


# ==============================
# SAVE CSV
# ==============================

def save_csv(trajectory_data):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Mission_Name",
            "Waypoint_No_or_Phase",
            "Target_X",
            "Target_Y",
            "Target_Z",
            "Actual_X",
            "Actual_Y",
            "Actual_Z",
            "Desired_Time_Seconds",
            "Actual_Time_Taken_Seconds",
            "Time_Error_Seconds",
            "Mission_Elapsed_Time_Seconds",
            "Segment_Start_Date",
            "Segment_Start_Clock",
            "Segment_End_Date",
            "Segment_End_Clock",
            "Real_World_End_DateTime",
            "Direct_Distance_m",
            "Total_Distance_Travelled_m",
            "Average_Speed_mps",
            "Yaw_Degrees",
            "Yaw_Rotation_Time_Seconds",
            "Final_Position_Error_m",
            "Max_Position_Error_m",
            "Estimated_Wind_X",
            "Estimated_Wind_Y",
            "Estimated_Wind_Z",
            "Average_Commanded_Velocity_X",
            "Average_Commanded_Velocity_Y",
            "Average_Commanded_Velocity_Z",
            "Control_Steps",
            "Path_Efficiency_Percent",
            "Battery_Used_Percent",
            "Battery_Remaining_Percent"
        ])

        writer.writerows(trajectory_data)

    print("\n===================================")
    print("CSV saved as:", CSV_FILE)


# ==============================
# MAIN
# ==============================

def main():
    waypoints, mission_name = get_waypoints_from_user()

    if waypoints is None:
        print("Exiting code.")
        return

    print("\nConnecting to AirSim...")

    client = airsim.MultirotorClient()
    client.confirmConnection()

    trajectory_data = run_mission(
        client,
        waypoints,
        mission_name
    )

    save_csv(trajectory_data)

    client.armDisarm(False)
    client.enableApiControl(False)

    print("Mission Complete")


if __name__ == "__main__":
    main()