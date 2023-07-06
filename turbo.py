import argparse
import logging
import subprocess
import os

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
BRIGHTNESS_PATH = "/sys/class/backlight/panel0-backlight/brightness"

# Define the package name for the cooling app
COOLING_APP_PACKAGE = "https://cpu-cooler-master-phone-cooler.en.softonic.com/android"

# Define the log file
LOG_FILE = "turbo.log"

# Define the error codes
ERROR_CODE_GENERAL = 1
ERROR_CODE_NO_ROOT_ACCESS = 2
ERROR_CODE_NO_ADB_CONNECTIVITY = 3

# Define a function to execute an adb shell command
def adb_shell(command):
    try:
        subprocess.check_call(['adb', 'devices'])
        subprocess.check_call(['adb', 'shell'] + command.split())
        logging.info(f"Executed command '{command}' successfully")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error executing command '{command}': {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

# Define a function to check if the script is being executed with root privileges
def check_root_access():
    if os.geteuid() != 0:
        logging.error("The script must be executed with root privileges. Aborting.")
        raise SystemExit(ERROR_CODE_NO_ROOT_ACCESS)

# Define a function to check if the device is connected and accessible via ADB
def check_adb_connectivity():
    try:
        output = subprocess.check_output(['adb', 'devices'])
        if "device" not in output.decode():
            logging.error("The device is not connected or accessible via ADB. Aborting.")
            raise SystemExit(ERROR_CODE_NO_ADB_CONNECTIVITY)
    except subprocess.CalledProcessError as error:
        logging.error(f"Error checking ADB connectivity: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def install_dependencies():
    try:
        subprocess.check_call(['pkg', 'install', 'python', 'git', 'tsu'])
        subprocess.check_call(['pkg', 'install', 'adb'])
    except subprocess.CalledProcessError as error:
        logging.error(f"Error installing dependencies: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def enable_usb_debugging():
    try:
        adb_shell("settings put global adb_enabled 1")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error enabling USB debugging: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def install_turbo_script():
    try:
        subprocess.check_call(['git', 'clone', 'https://github.com/fkpwolf/turbo'])
        subprocess.check_call(['chmod', '+x', './turbo/turbo.sh'])
        adb_shell("tsudo ./turbo/turbo.sh")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error installing Turbo: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def disable_system_animations():
    try:
        adb_shell(f"settings put global {WINDOW_ANIMATION_SCALE_PATH} 0")
        adb_shell(f"settings put global {TRANSITION_ANIMATION_SCALE_PATH} 0")
        adb_shell(f"settings put global {ANIMATOR_DURATION_SCALE_PATH} 0")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error disabling system animations: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def set_charging_speed():
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
        raise SystemExit(ERROR_CODE_GENERAL)

def set_cpu_governor():
    try:
        adb_shell(f"echo performance > {CPUGOV_PATH}")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error setting CPU governor: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def optimize_memory():
    try:
        adb_shell("su -c 'echo 3 > " + DROP_CACHES_PATH + "'")
        logging.info("Memory optimized successfully.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error optimizing memory: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def customize_device_settings():
    print("Which device settings would you like to customize?")
    print("1. Screen resolution")
    print("2. Display brightness")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        print("Available resolutions:")
        print("1. 720p")
        print("2. 1080p")
        print("3. 1440p")
        resolution_choice = input("Enter the number for the resolution you want to set: ")
        if resolution_choice == "1":
            adb_shell("wm size 720x1280")
        elif resolution_choice == "2":
            adb_shell("wm size 1080x1920")
        elif resolution_choice == "3":
            adb_shell("wm size 1440x2560")
        else:
            print("Invalid choice.")
    elif choice == "2":
        brightness = input("Enter the brightness level (1-255): ")
        adb_shell(f"su -c 'echo {brightness} > {BRIGHTNESS_PATH}'")
    else:
        print("Invalid choice.")

def optimize_camera_settings():
    try:
        adb_shell(f"settings put global {CAMERA_PATH} 0")
        logging.info("Camera settings optimized successfully.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error optimizing camera settings: {error}")
        raise SystemExit(ERROR_CODE_GENERAL)

def optimize_audio_settings():
    print("Which audio settings would you like to optimize?")
    print("1. Speaker")
    print("2. Headphones")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        print("Available options:")
        print("1. Bass boost")
        print("2. Treble boost")
        print("3. Equalizer")
        audio_choice = input("Enter the number for the option you want to set: ")
        if audio_choice == "1":
            adb_shell("su -c 'echo 1 > /sys/class/misc/volume/boost'")
        elif audio_choice == "2":
            adb_shell("su -c 'echo 1 > /sys/class/misc/volume/treble_boost'")
        elif audio_choice == "3":
            adb_shell("su -c 'am start -n com.android.settings/com.android.settings.Settings\\$SoundSettingsActivity'")
        else:
            print("Invalid choice.")
    elif choice == "2":
        print("Available options:")
        print("1. Bass boost")
        print("2. Treble boost")
        print("3. Equalizer")
        audio_choice = input("Enter the number for the option you want to set: ")
        if audio_choice == "1":
            adb_shell("su -c 'echo 1 > /sys/class/misc/volume/headphone_boost'")
        elif audio_choice == "2":
            adb_shell("su -c 'echo 1 > /sys/class/misc/volume/headphone_treble_boost'")
        elif audio_choice == "3":
            adb_shell("su -c 'am start -n com.android.settings/com.android.settings.Settings\\$SoundSettingsActivity'")
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")

def optimize_gps_settings():
    print("Which GPS settings would you like to optimize?")
    print("1. Location accuracy")
    print("2. Battery usage")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        adb_shell("settings put secure location_mode 3")
    elif choice == "2":
        adb_shell("settings put secure location_mode 2")
    else:
        print("Invalid choice.")

def optimize_security_settings():
    print("Which security settings would you like to optimize?")
    print("1. Lock screen")
    print("2. App permissions")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        adb_shell("su -c 'am start -n com.android.settings/com.android.settings.Settings\\$LockScreenSettingsActivity'")
    elif choice == "2":
        adb_shell("su -c 'am start -n com.android.settings/com.android.settings.Settings\\$ManageAppPermissionsActivity'")
    else:
        print("Invalid choice.")

def optimize_accessibility_settings():
    print("Which accessibility settings would you like to optimize?")
    print("1. Display size")
    print("2. Font size")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        size = input("Enter the display size (0.5-2.0): ")
        adb_shell(f"settings put system {DISPLAY_SIZE_PATH} {size}")
    elif choice == "2":
        scale = input("Enter the font scale (0.5-2.0): ")
        adb_shell(f"settings put system {DISPLAY_DENSITY_PATH} {scale}")
    else:
        print("Invalid choice.")

def optimize_power_management():
    print("Which power management settings would you like to optimize?")
    print("1. Battery saver mode")
    print("2. Sleep mode")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        adb_shell("settings put global low_power 1")
    elif choice == "2":
        adb_shell("su -c 'input keyevent POWER'")
    else:
        print("Invalid choice.")

def optimize_display_settings():
    print("Which display settings would you like to optimize?")
    print("1. Night mode")
    print("2. Blue light filter")
    print("3. Dark theme")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        adb_shell("su -c 'am start -n com.android.settings/com.android.settings.Settings\\$TunerActivity'")
    elif choice == "2":
        adb_shell("settings put system night_display_activated 1")
    elif choice == "3":
        adb_shell("settings put secure ui_night_mode 2")
    else:
        print("Invalid choice.")

def optimize_input_settings():
    print("Which input settings would you like to optimize?")
    print("1. Typing accuracy")
    print("2. Input lag")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        adb_shell("settings put secure show_ime_with_hard_keyboard 1")
    elif choice == "2":
        adb_shell("su -c 'echo 1 > /proc/sys/kernel/hung_task_timeout_secs'")
    else:
        print("Invalid choice.")

def optimize_multitasking():
    print("Which multitasking settings would you like to optimize?")
    print("1. Background processes")
    print("2. Memory usage")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        adb_shell(f"settings put global {GAME_MODE_PATH} 1")
    elif choice == "2":
        adb_shell("su -c 'echo 1 > /proc/sys/vm/compact_memory'")
    else:
        print("Invalid choice.")

def optimize_app_performance():
    print("Which app performance settings would you like to optimize?")
    print("1. Clear app cache")
    print("2. Adjust app settings")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        package_name = input("Enter the package name of the app you want to clear the cache for: ")
        adb_shell(f"pm clear {package_name}")
    elif choice == "2":
        package_name = input("Enter the package name of the app you want to adjust the settings for: ")
        adb_shell(f"am start -n com.android.settings/.Settings -e package {package_name}")
    else:
        print("Invalid choice.")

# Define the main function
def main():
    # Set up logging
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Turbo: A script to optimize your Android device.")
    parser.add_argument("--install-dependencies", help="Install required dependencies", action="store_true")
    parser.add_argument("--enable-usb-debugging", help="Enable USB debugging", action="store_true")
    parser.add_argument("--install-turbo-script", help="Install the Turbo script", action="store_true")
    parser.add_argument("--disable-system-animations", help="Disable system animations", action="store_true")
    parser.add_argument("--set-charging-speed", help="Set charging speed to maximum", action="store_true")
    parser.add_argument("--set-cpu-governor", help="Set CPU governor to performance", action="store_true")
    parser.add_argument("--optimize-memory", help="Optimize memory usage", action="store_true")
    parser.add_argument("--customize-device-settings", help="Customize device settings", action="store_true")
    parser.add_argument("--optimize-camera-settings", help="Optimize camera settings", action="store_true")
    parser.add_argument("--optimize-audio-settings", help="Optimize audio settings", action="store_true")
    parser.add_argument("--optimize-gps-settings", help="Optimize GPS settings", action="store_true")
    parser.add_argument("--optimize-security-settings", help="Optimize security settings", action="store_true")
    parser.add_argument("--optimize-accessibility-settings", help="Optimize accessibility settings", action="store_true")
    parser.add_argument("--optimize-power-management", help="Optimize power management settings", action="store_true")
    parser.add_argument("--optimize-display-settings", help="Optimize display settings", action="store_true")
    parser.add_argument("--optimize-input-settings", help="Optimize input settings", action="store_true")
    parser.add_argument("--optimize-multitasking", help="Optimize multitasking settings", action="store_true")
    parser.add_argument("--optimize-app-performance", help="Optimize app performance settings", action="store_true")
    args = parser.parse_args()

    # Run the appropriate functions based on command line arguments
    if args.install_dependencies:
        install_dependencies()
    if args.enable_usb_debugging:
        enable_usb_debugging()
    if args.install_turbo_script:
        install_turbo_script()
    if args.disable_system_animations:
        disable_system_animations()
    if args.set_charging_speed:
        set_charging_speed()
    if args.set_cpu_governor:
        set_cpu_governor()
    if args.optimize_memory:
        optimize_memory()
    if args.customize_device_settings:
        customize_device_settings()
    if args.optimize_camera_settings:
        optimize_camera_settings()
    if args.optimize_audio_settings:
        optimize_audio_settings()
    if args.optimize_gps_settings:
        optimize_gps_settings()
    if args.optimize_security_settings:
        optimize_security_settings()
    if args.optimize_accessibility_settings:
        optimize_accessibility_settings()
    if args.optimize_power_management:
        optimize_power_management()
    if args.optimize_display_settings:
        optimize_display_settings()
    if args.optimize_input_settings:
        optimize_input_settings()
    if args.optimize_multitasking:
        optimize_multitasking()
    if args.optimize_app_performance:
        optimize_app_performance()

if __name__ == "__main__":
    main()