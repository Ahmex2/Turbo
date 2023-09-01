import argparse
import logging
import subprocess

# Define the paths for the Redmi Note 9S
WINDOW_ANIMATION_SCALE_PATH = "/settings/global/window_animation_scale"
TRANSITION_ANIMATION_SCALE_PATH = "/settings/global/transition_animation_scale"
ANIMATOR_DURATION_SCALE_PATH = "/settings/global/animator_duration_scale"
DROP_CACHES_PATH = "/proc/sys/vm/drop_caches"
CPUGOV_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
CAMERA_PATH = "/settings/global/camera_sound_forced"
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
    try:
        adb_shell(f"settings put global {WINDOW_ANIMATION_SCALE_PATH} 0")
        adb_shell(f"settings put global {TRANSITION_ANIMATION_SCALE_PATH} 0")
        adb_shell(f"settings put global {ANIMATOR_DURATION_SCALE_PATH} 0")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error disabling system animations: {error}")
        return False
    return True

def set_charging_speed():
    """Set charging speed to maximum (Universal)"""
    try:
        # Check if device is charging
        output = subprocess.check_output(['adb', 'shell', 'dumpsys', 'battery'])
        if "status: charging" in output.decode():
            # Set charging speed to maximum (Universal)
            adb_shell("su -c 'echo 1 > /sys/class/power_supply/*/input_current_limit'")
            logging.info("Charging speed set to maximum.")
        else:
            logging.warning("Device is not charging.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error setting charging speed: {error}")
        return False
    return True

def set_cpu_governor():
    """Set CPU governor to performance"""
    try:
        adb_shell(f"echo performance > {CPUGOV_PATH}")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error setting CPU governor: {error}")
        return False
    return True

def optimize_memory():
    """Optimize memory"""
    try:
        adb_shell("sync")
        adb_shell(f"echo 3 > {DROP_CACHES_PATH}")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error optimizing memory: {error}")
        return False
    return True

def disable_camera_sound():
    """Disable camera sound"""
    try:
        adb_shell(f"settings put global {CAMERA_PATH} 0")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error disabling camera sound: {error}")
        return False
    return True

def adjust_display_settings():
    """Adjust display settings"""
    try:
        adb_shell(f"settings put system {DISPLAY_SIZE_PATH} -3")
        adb_shell(f"settings put system {DISPLAY_DENSITY_PATH} 1.0")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error adjusting display settings: {error}")
        return False
    return True

def enable_game_mode():
    """Enable game mode"""
    try:
        adb_shell(f"settings put system {GAME_MODE_PATH} 1")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error enabling game mode: {error}")
        return False
    return True

def start_cooling_app():
    """Start the cooling app"""
    try:
        subprocess.check_call(['adb', 'shell', 'am', 'start', '-n', f"{COOLING_APP_PACKAGE}/.MainActivity"])
        logging.info("Cooling app started.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error starting cooling app: {error}")
        return False
    return True

def adjust_screen_brightness(brightness_level):
    """Adjust screen brightness"""
    try:
        adb_shell(f"settings put system screen_brightness {brightness_level}")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error adjusting screen brightness: {error}")
        return False
    return True

def disable_background_app_refresh():
    """Disable background app refresh"""
    try:
        adb_shell("settings put global app_background_process_limit 0")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error disabling background app refresh: {error}")
        return False
    return True

def enable_battery_saver_mode():
    """Enable battery saver mode"""
    try:
        adb_shell("settings put global low_power 1")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error enabling battery saver mode: {error}")
        return False
    return True

def restrict_app_background_data(package_name):
    """Restrict app background data"""
    try:
        adb_shell(f"cmd appops set {package_name} RUN_IN_BACKGROUND deny")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error restricting app background data: {error}")
        return False
    return True

def main():
    """Main function"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Optimize Android device for gaming.")
    parser.add_argument('-v', '--verbose', action='store_true', help="enable verbose logging")
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
    if not disable_system_animations():
        logging.error("Aborting due to system animations error.")
        return

    # Set charging speed to maximum (Universal)
    if not set_charging_speed():
        logging.warning("Skipping charging speed optimization.")

    # Set CPU governor to performance
    if not set_cpu_governor():
        logging.warning("Skipping CPU governor optimization.")

    # Optimize memory
    if not optimize_memory():
        logging.warning("Skipping memory optimization.")

    # Disable camera sound
    if not disable_camera_sound():
        logging.warning("Skipping camera sound optimization.")

    # Adjust display settings
    if not adjust_display_settings():
        logging.warning("Skipping display settings optimization.")

    # Enable game mode
    if not enable_game_mode():
        logging.warning("Skipping game mode optimization.")

    # Start the cooling app
    if not start_cooling_app():
        logging.warning("Skipping cooling app start.")

    # Adjust screen brightness (Please replace '<brightness_level>' with an appropriate value)
    if not adjust_screen_brightness("<brightness_level>"):
        logging.warning("Skipping screen brightness adjustment.")

    # Disable background app refresh
    if not disable_background_app_refresh():
        logging.warning("Skipping background app refresh optimization.")

    # Enable battery saver mode
    if not enable_battery_saver_mode():
        logging.warning("Skipping battery saver mode optimization.")

    # Restrict app background data (Please replace '<package_name>' with the appropriate package name)
    if not restrict_app_background_data("<package_name>"):
        logging.warning("Skipping app background data restriction.")

    logging.info("Optimization complete.")

if __name__ == '__main__':
    main()
