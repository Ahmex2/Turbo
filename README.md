# Android Device Optimization Script

## Overview

This Python script optimizes an Android device for better performance and stability. It achieves this by installing necessary packages, enabling USB debugging, and executing various optimization commands, including applying settings to improve CPU performance and adjusting screen brightness.

## Usage

1. **Prerequisites**
   - Ensure that your Android device is connected to the computer via USB.
   - USB debugging must be enabled on your device.

2. **Script Execution**
   - Run the script directly using Python: `python script_name.py`

3. **Command-line Options**
   - `-v` or `--verbose`: Enable verbose logging for detailed information.

## Script Components

### Packages to be Installed
- List of packages: `com.termux`

### Turbo Script Repository
- Turbo script repository: [Turbo Repository](https://github.com/fkpwolf/turbo)

### Device Performance Optimization Settings
- General settings to optimize performance.
- Additional settings for further optimization.

### ADB Command Execution Functions
1. **execute_adb_command(command)**
   - Executes ADB commands with improved error handling.

2. **optimize_cpu_frequency()**
   - Optimizes CPU frequency for improved performance.

3. **adjust_screen_brightness()**
   - Adjusts screen brightness for better visibility.

### Main Functionality
- Parses command-line arguments for verbose logging.
- Installs required packages with improved error handling.
- Enables USB debugging with improved error handling.
- Installs Turbo script with improved error handling.
- Optimizes CPU frequency and adjusts screen brightness.
- Logs all actions and errors in 'android_optimization.log'.

## Example Usage
```bash
python turbo.py -v
```

Note: Ensure that ADB (Android Debug Bridge) is installed and available in the system's PATH.
