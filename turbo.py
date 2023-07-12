#!/usr/bin/env python3

import argparse
import logging
import subprocess
import sys

# Define the paths for the device
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
        return False
    return True

def install_dependencies():
    """Install necessary dependencies"""
    try:
        subprocess.check_call(['pkg', 'install', 'python', 'git', 'tsu', 'adb'])
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
    """Set charging speed to maximum"""
    try:
        # Check if device is charging
        output = subprocess.check_output(['adb', 'shell', 'dumpsys', 'battery'])
        if "status: charging" in output.decode():
            # Set charging speed to maximum
            adb_shell("su -c 'echo 1 > /sys/class/power_supply/battery/input_current_limit'")
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
        adb_shell(f"am start -n {COOLING_APP_PACKAGE}/.MainActivity")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error starting cooling app: {error}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Optimize your device for gaming.')
    parser.add_argument('--device', type=str, required=True, help='Device ID')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Set the device ID for future commands
    subprocess.run(['adb', 'devices'])
    subprocess.run(['adb', '-s', args.device, 'root'])
    subprocess.run(['adb', '-s', args.device, 'remount'])
    subprocess.run(['adb', '-s', args.device, 'shell', 'setenforce', '0'])
    subprocess.run(['adb', '-s', args.device, 'shell', 'stop', 'perfprofd'])

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Enable USB debugging
    if not enable_usb_debugging():
        sys.exit(1)

    # Install the Turbo script
    if not install_turbo_script():
        sys.exit(1)

    # Disable system animations
    if not disable_system_animations():
        sys.exit(1)

    # Set charging speed to maximum
    if not set_charging_speed():
        sys.exit(1)

    # Set CPU governor to performance
    if not set_cpu_governor():
        sys.exit(1)

    # Optimize memory
    if not optimize_memory():
        sys.exit(1)

    # Disable camera sound
    if not disable_camera_sound():
        sys.exit(1)

    # Adjust display settings
    if not adjust_display_settings():
        sys.exit(1)

    # Enable game mode
    if not enable_game_mode():
        sys.exit(1)

    # Start the cooling app
    if not start_cooling_app():
        sys.exit(1)

    logging.info("Device optimization complete.")

if __name__ == '__main__':
    main()