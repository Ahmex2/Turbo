import subprocess
import argparse
import logging

# List of packages to be installed
PACKAGES = ['python', 'git', 'tsu', 'adb', 'com.termux']

# URL for the Turbo script repository
TURBO_REPO = 'https://github.com/fkpwolf/turbo'

# Settings to optimize device performance
SETTINGS = {
    'window_animation_scale': '0.0',
    'transition_animation_scale': '0.0',
    'animator_duration_scale': '0.0',
    'wifi_scan_throttle_enabled': '1',
    'wifi_scan_interval': '300000',
    'wifi_idle_ms': '1800000',
    'min_processor': '50',
    'max_processor': '100',
}

# Additional settings to further optimize device performance
ADDITIONAL_SETTINGS = {
    'force_hw_ui': 'true',
    'force_gpu_rendering': 'true',
    'force_4x_msaa': 'true',
    'lock_profiling': '1',
    'lock_resizing': '1',
    'lock_resizing_window': '1',
    'lock_freeform_window_management': '1',
    'wifi.supplicant_scan_interval': '180',
    'debug.enabletr=true': 'true',
    'video.accelerate.hw': 'true',      
    'audio.mixer': 'true',
  
}

# Function to execute ADB commands with improved error handling and feedback
def execute_adb_command(command):
    try:
        adb_devices = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        if 'device' in adb_devices.stdout:
            subprocess.run(['adb', 'shell', command], shell=True, check=True)
            logging.info(f"Successfully executed the command: '{command}'")
        else:
            logging.error("No devices found. Please connect your device and enable USB debugging.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Encountered an error executing the command '{command}': {error}")

# Function to install a package via ADB
def install_package(package_name):
    try:
        subprocess.run(['adb', 'shell', 'pm', 'install', package_name], check=True)
        logging.info(f"Successfully installed the package: '{package_name}'")
        return True
    except subprocess.CalledProcessError as error:
        logging.error(f"Encountered an error installing the package '{package_name}': {error}")
        return False

# Function to enable USB debugging
def enable_usb_debugging():
    try:
        execute_adb_command("settings put global adb_enabled 1")
        logging.info("USB debugging successfully enabled")
        return True
    except subprocess.CalledProcessError as error:
        logging.error(f"Encountered an error enabling USB debugging: {error}")
        return False

# Function to install the Turbo script
def install_turbo_script():
    try:
        execute_adb_command(f"git clone {TURBO_REPO}")
        execute_adb_command("chmod +x ./turbo/turbo.sh")
        execute_adb_command("tsudo ./turbo/turbo.sh")
        logging.info("Turbo script installed and executed successfully")
        return True
    except subprocess.CalledProcessError as error:
        logging.error(f"Encountered an error installing Turbo: {error}")
        return False

# Function to optimize device settings
def optimize_device():
    try:
        # Apply the settings to optimize device performance
        for setting, value in SETTINGS.items():
            execute_adb_command(f"settings put global {setting} {value}")

        logging.info("Device optimization completed successfully")
    except subprocess.CalledProcessError as error:
        logging.error(f"Encountered an error optimizing the device: {error}")

# Function to apply additional device-specific settings
def additional_device_settings():
    try:
        # Apply additional settings for further device optimization
        for setting, value in ADDITIONAL_SETTINGS.items():
            execute_adb_command(f"settings put global {setting} {value}")

        logging.info("Additional device-specific settings applied successfully")
    except subprocess.CalledProcessError as error:
        logging.error(f"Encountered an error applying additional device settings: {error}")

# Main function to run the optimization process
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Optimize Android device for better performance and stability")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
    args = parser.parse_args()
    
    # Set logging level based on the provided argument
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(filename='android_optimization.log', format='%(levelname)s: %(message)s', level=log_level)

    # Install required packages with improved error handling
    for package in PACKAGES:
        if not install_package(package):
            logging.error(f"Aborting due to a missing dependency: {package}")
            return

    # Enable USB debugging with improved error handling
    if not enable_usb_debugging():
        logging.error("Aborting due to USB debugging error")
        return

    # Install Turbo script with improved error handling
    if not install_turbo_script():
        logging.error("Aborting due to Turbo installation error")
        return
      
    # Optimize device settings
    optimize_device()

    # Apply additional device-specific settings
    additional_device_settings()

    logging.info("Optimization process completed")

# Execute the main function when the script is run directly
if __name__ == '__main__':
    main()
