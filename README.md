
# Android Device Optimization and Media Capture Script

**Author:** Ahmed

This Python script is designed to optimize the performance of your Android device and capture media (photos or videos) using the device's camera. It offers a convenient way to enhance your Android experience and streamline media capture.

## Features

- **Performance Optimization:** The script optimizes your Android device for smoother performance by adjusting various settings, including animations, CPU governor, memory, display, and more.

- **USB Debugging:** It enables USB debugging, a necessary step for many advanced Android operations.

- **Turbo Script Installation:** The script installs the Turbo script, which can further enhance device performance.

- **Camera Capture:** Capture media using the device's camera. You can choose to capture photos or videos.

- **Additional Settings:** The script allows you to adjust screen brightness, disable background app refresh, enable battery saver mode, and restrict app background data.

- **Game Mode:** It enables the Android Game Mode for an optimized gaming experience.

## Usage

1. Ensure that your Android device is connected to your computer via USB debugging mode.

2. Run the script with Python by executing the following command in your terminal:

   
   python script_name.py [-v] [-m {photo,video}]
  

   - Use the `-v` or `--verbose` flag for verbose logging.
   - Use the `-m` or `--media` flag to specify whether to capture a 'photo' or 'video' (default is 'photo').

3. Follow the on-screen prompts as the script optimizes your device and captures media.

## Dependencies

Before using the script, ensure you have the following dependencies installed on your computer:

- Python
- Git
- tsu (Android root access)
- adb (Android Debug Bridge)

You can install these dependencies using the following command:

```bash
pkg install python git tsu adb
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the Android community and contributors for inspiration and useful tools.

Feel free to contribute to this project or report any issues you encounter. Enjoy optimizing your Android device and capturing great moments!


Please make sure to replace `script_name.py` with the actual name of your Python script. You can also replace the `LICENSE` section with the appropriate license information if needed.

