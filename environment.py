import airsim
import os


# ==============================
# COLOR CODES
# ==============================

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ==============================
# ENVIRONMENT FUNCTIONS
# ==============================

def reset_weather(client):
    client.simEnableWeather(True)

    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.0)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.0)
    client.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0.0)
    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, 0.0)
    client.simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, 0.0)
    client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 0.0)

    client.simSetWind(airsim.Vector3r(0, 0, 0))


def clear_environment(client):
    reset_weather(client)
    print(GREEN + "Environment changed to CLEAR." + RESET)


def windy_environment(client):
    reset_weather(client)
    client.simSetWind(airsim.Vector3r(10, 10, 3))
    print(CYAN + "Environment changed to WINDY." + RESET)


def rainy_environment(client):
    reset_weather(client)
    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.7)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.2)
    client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 0.8)
    client.simSetWind(airsim.Vector3r(2, 2, 0))
    print(BLUE + "Environment changed to RAINY." + RESET)


def foggy_environment(client):
    reset_weather(client)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.7)
    client.simSetWind(airsim.Vector3r(1, 1, 0))
    print(WHITE + "Environment changed to FOGGY." + RESET)


def snowy_environment(client):
    reset_weather(client)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.2)
    client.simSetWeatherParameter(airsim.WeatherParameter.Snow, 0.7)
    client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 0.3)
    client.simSetWind(airsim.Vector3r(2, 1, 0))
    print(CYAN + "Environment changed to SNOWY." + RESET)


def dusty_environment(client):
    reset_weather(client)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.1)
    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, 0.7)
    client.simSetWind(airsim.Vector3r(4, 2, 0))
    print(YELLOW + "Environment changed to DUSTY." + RESET)


def storm_environment(client):
    reset_weather(client)
    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.9)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.5)
    client.simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, 0.4)
    client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 1.0)
    client.simSetWind(airsim.Vector3r(6, 4, 0))
    print(RED + "Environment changed to STORM." + RESET)


# ==============================
# MENU
# ==============================

def show_menu():
    print("\n" + MAGENTA + "========== AIRSIM ENVIRONMENT SELECTOR ==========" + RESET)
    print(GREEN + "1. Clear Environment" + RESET)
    print(CYAN + "2. Windy Environment" + RESET)
    print(BLUE + "3. Rainy Environment" + RESET)
    print(WHITE + "4. Foggy Environment" + RESET)
    print(CYAN + "5. Snowy Environment" + RESET)
    print(YELLOW + "6. Dusty Environment" + RESET)
    print(RED + "7. Storm Environment" + RESET)
    print(MAGENTA + "8. Exit Code" + RESET)
    print(MAGENTA + "=================================================" + RESET)


def main():
    print("Connecting to AirSim...")
    client = airsim.MultirotorClient()
    client.confirmConnection()

    print(GREEN + "Connected to AirSim successfully." + RESET)

    while True:
        show_menu()

        choice = input("\nEnter your choice: ")

        if choice == "1":
            clear_environment(client)

        elif choice == "2":
            windy_environment(client)

        elif choice == "3":
            rainy_environment(client)

        elif choice == "4":
            foggy_environment(client)

        elif choice == "5":
            snowy_environment(client)

        elif choice == "6":
            dusty_environment(client)

        elif choice == "7":
            storm_environment(client)

        elif choice == "8":
            print(MAGENTA + "Exiting environment selector." + RESET)
            print(YELLOW + "Current environment will remain active in Blocks." + RESET)
            break

        else:
            print(RED + "Invalid choice. Please select 1 to 8." + RESET)


if __name__ == "__main__":
    main()