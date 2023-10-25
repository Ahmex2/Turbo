import subprocess
import argparse
import logging

# Constants for package names and URLs
PACKAGES = ['python', 'git', 'tsu', 'adb']
TURBO_REPO = 'https://github.com/fkpwolf/turbo'

# Constants for device optimization settings
SETTINGS = {
    'window_animation_scale': '0.0',
    'transition_animation_scale': '0.0',
    'animator_duration_scale': '0.0',
    'wifi_scan_throttle_enabled': '0',
    'wifi_scan_interval': '180000',
    'wifi_idle_ms': '1800000',
}

def execute_adb_command(command):
    """Execute an adb shell command."""
    try:
        subprocess.run(['adb', 'devices'], check=True)
        subprocess.run(['adb', 'shell', command], shell=True, check=True)
        logging.info(f"Executed command '{command}' successfully")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error executing command '{command}': {error}")

def install_package(package_name):
    """Install a package using adb."""
    try:
        subprocess.run(['adb', 'shell', 'pm', 'install', package_name], check=True)
        logging.info(f"Installed package '{package_name}' successfully.")
        return True
    except subprocess.CalledProcessError as error:
        logging.error(f"Error installing package '{package_name}': {error}")
        return False

def enable_usb_debugging():
    """Enable USB debugging."""
    try:
        execute_adb_command("settings put global adb_enabled 1")
        logging.info("USB debugging enabled successfully.")
        return True
    except subprocess.CalledProcessError as error:
        logging.error(f"Error enabling USB debugging: {error}")
        return False

def install_turbo_script():
    """Install and execute the Turbo script for performance."""
    try:
        execute_adb_command(f"git clone {TURBO_REPO}")
        execute_adb_command("chmod +x ./turbo/turbo.sh")
        execute_adb_command("tsudo ./turbo/turbo.sh")
        logging.info("Turbo script installed and executed successfully.")
        return True
    except subprocess.CalledProcessError as error:
        logging.error(f"Error installing Turbo: {error}")
        return False

def optimize_device():
    """Optimize the device for better performance and stability."""
    try:
        for setting, value in SETTINGS.items():
            execute_adb_command(f"settings put global {setting} {value}")

        execute_adb_command("echo 1 > /sys/class/kgsl/kgsl-3d0/min_pwrlevel")
        execute_adb_command("echo 1 > /sys/class/kgsl/kgsl-3d0/max_pwrlevel")
        execute_adb_command("echo 20000000 > /sys/class/kgsl/kgsl-3d0/devfreq/adreno_min_freq")
        execute_adb_command("echo 50000000 > /sys/class/kgsl/kgsl-3d0/devfreq/adreno_max_freq")
        logging.info("Device optimization complete.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error optimizing device: {error}")

def main():
    """Main function for Android optimization."""
    parser = argparse.ArgumentParser(description="Optimize Android device for better performance and stability.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(filename='android_optimization.log', format='%(levelname)s: %(message)s', level=log_level)

    # Check and install required packages
    for package in PACKAGES:
        if not install_package(package):
            logging.error(f"Aborting due to missing dependency: {package}")
            return

    if not enable_usb_debugging():
        logging.error("Aborting due to USB debugging error.")
        return

    if not install_turbo_script():
        logging.error("Aborting due to Turbo installation error.")
        return

    optimize_device()
    logging.info("Optimization complete.")

if __name__ == '__main__':
    main()