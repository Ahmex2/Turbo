import argparse
import logging
import subprocess

# Define the paths for performance optimization
WINDOW_ANIMATION_SCALE_PATH = "0.0"  # Set animation scales to 0 for faster performance
TRANSITION_ANIMATION_SCALE_PATH = "0.0"
ANIMATOR_DURATION_SCALE_PATH = "0.0"
DROP_CACHES_PATH = "/proc/sys/vm/drop_caches"
CPUGOV_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
DISPLAY_SIZE_PATH = "/settings/system/pointer_speed"
DISPLAY_DENSITY_PATH = "/settings/system/font_scale"
GAME_MODE_PATH = "/settings/system/game_mode"

# Define the package name for the cooling app
COOLING_APP_PACKAGE = "com.example.coolingapp"

def adb_shell(command):
    """Execute an adb shell command"""
    try:
        subprocess.check_call(['adb', 'devices'])
        subprocess.check_call(['adb', 'shell'] + command.split())
        logging.info(f"Executed command '{command}' successfully")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error executing command '{command}': {error}")

def install_dependencies():
    """Install necessary dependencies"""
    try:
        subprocess.check_call(['pkg', 'install', 'python', 'git', 'tsu'])
        subprocess.check_call(['pkg', 'install', 'adb'])
    except subprocess.CalledProcessError as error:
        logging.error(f"Error installing dependencies: {error}")
        return False
    return True

def enable_usb_debugging():
    """Enable USB debugging"""
    try:
        adb_shell("settings put global adb_enabled 1")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error enabling USB debugging: {error}")
        return False
    return True

def install_turbo_script():
    """Install the Turbo script"""
    try:
        subprocess.check_call(['git', 'clone', 'https://github.com/fkpwolf/turbo'])
        subprocess.check_call(['chmod', '+x', './turbo/turbo.sh'])
        adb_shell("tsudo ./turbo/turbo.sh")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error installing Turbo: {error}")
        return False
    return True

def disable_system_animations():
    """Disable system animations"""
    adb_shell(f"settings put global {WINDOW_ANIMATION_SCALE_PATH}")
    adb_shell(f"settings put global {TRANSITION_ANIMATION_SCALE_PATH}")
    adb_shell(f"settings put global {ANIMATOR_DURATION_SCALE_PATH}")

def set_charging_speed():
    """Set charging speed to maximum (Universal)"""
    try:
        # Check if the device is charging
        output = subprocess.check_output(['adb', 'shell', 'dumpsys', 'battery'])
        if "status: charging" in output.decode():
            # Set charging speed to maximum (Universal)
            adb_shell("su -c 'echo 1 > /sys/class/power_supply/*/input_current_limit'")
            logging.info("Charging speed set to maximum.")
        else:
            logging.warning("Device is not charging.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error setting charging speed: {error}")

def set_cpu_governor():
    """Set CPU governor to performance"""
    adb_shell(f"echo performance > {CPUGOV_PATH}")

def optimize_memory():
    """Optimize memory"""
    adb_shell("sync")
    adb_shell(f"echo 3 > {DROP_CACHES_PATH}")

def adjust_display_settings():
    """Adjust display settings"""
    adb_shell(f"settings put system {DISPLAY_SIZE_PATH} -3")
    adb_shell(f"settings put system {DISPLAY_DENSITY_PATH} 1.0")

def enable_game_mode():
    """Enable game mode"""
    adb_shell(f"settings put system {GAME_MODE_PATH} 1")

def start_cooling_app():
    """Start the cooling app"""
    try:
        subprocess.check_call(['adb', 'shell', 'am', 'start', '-n', f"{COOLING_APP_PACKAGE}/.MainActivity"])
        logging.info("Cooling app started.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error starting cooling app: {error}")

def capture_media(media_type):
    """Capture media (photo or video) using the camera"""
    try:
        if media_type == "photo":
            subprocess.check_call(['adb', 'shell', 'am', 'start', '-a', 'android.media.action.IMAGE_CAPTURE'])
            logging.info("Camera app started for photo capture.")
        elif media_type == "video":
            subprocess.check_call(['adb', 'shell', 'am', 'start', '-a', 'android.media.action.VIDEO_CAPTURE'])
            logging.info("Camera app started for video capture.")
        else:
            logging.warning("Invalid media type. Use 'photo' or 'video'.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error starting camera app for media capture: {error}")

def adjust_screen_brightness(brightness_level):
    """Adjust screen brightness"""
    adb_shell(f"settings put system screen_brightness {brightness_level}")

def disable_background_app_refresh():
    """Disable background app refresh"""
    adb_shell("settings put global app_background_process_limit 0")

def enable_battery_saver_mode():
    """Enable battery saver mode"""
    adb_shell("settings put global low_power 1")

def restrict_app_background_data(package_name):
    """Restrict app background data"""
    adb_shell(f"cmd appops set {package_name} RUN_IN_BACKGROUND deny")

def main():
    """Main function"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Optimize Android device and capture media (photo or video).")
    parser.add_argument('-v', '--verbose', action='store_true', help="enable verbose logging")
    parser.add_argument('-m', '--media', choices=['photo', 'video'], default='photo', help="capture 'photo' or 'video'")
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG if args.verbose else logging.INFO)

    # Install dependencies
    if not install_dependencies():
        logging.error("Aborting due to missing dependencies.")
        return

    # Enable USB debugging
    if not enable_usb_debugging():
        logging.error("Aborting due to USB debugging error.")
        return

    # Install Turbo script
    if not install_turbo_script():
        logging.error("Aborting due to Turbo installation error.")
        return

    # Disable system animations
    disable_system_animations()

    # Set charging speed to maximum (Universal)
    set_charging_speed()

    # Set CPU governor to performance
    set_cpu_governor()

    # Optimize memory
    optimize_memory()

    # Adjust display settings
    adjust_display_settings()

    # Enable game mode
    enable_game_mode()

    # Start the cooling app
    start_cooling_app()

    # Capture media (photo or video)
    capture_media(args.media)

    # Adjust screen brightness (Please replace '<brightness_level>' with an appropriate value)
    adjust_screen_brightness(100)

    # Disable background app refresh
    disable_background_app_refresh()

    # Enable battery saver mode
    enable_battery_saver_mode()

    # Restrict app background data (Please replace '<package_name>' with the appropriate package name)
    restrict_app_background_data("com.example.someapp")

    logging.info("Optimization and media capture complete.")

if __name__ == '__main__':
    main()
