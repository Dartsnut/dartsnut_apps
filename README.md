# Dartsnut Apps Repository

This repository helps developers create their own apps for Dartsnut hardware and serves as a central place to store official Dartsnut apps.

## Features

- Resources and examples for app development
- Tools to streamline deployment to Dartsnut hardware
- Collection of official Dartsnut apps

## Getting Started

To get started, you may want to check out the [Dartsnut Emulator repository](https://github.com/Dartsnut/dartsnut_emulator.git), which provides a virtual environment for testing and developing your apps before deploying them to actual hardware.

## Communicating with Dartsnut Hardware

To interact with Dartsnut hardware, use the [`pydartsnut`](https://github.com/Dartsnut/pydartsnut.git) module as a middleware. This module provides an easy-to-use API for sending and receiving data between your app and the hardware. Refer to the repository for installation instructions and usage examples.

## App Structure and Environment

Apps in this repository run in a Python virtual environment (`venv`) on Raspberry Pi devices. Each app should be organized as a folder containing a `main.py` file—this is the entry point that our system will execute. Developers can include additional resources (such as images, data files, or modules) within the same folder for use in their apps. This structure ensures easy deployment and management on Dartsnut hardware.

## App Configuration: `conf.json`

Each app must include a `conf.json` file in its folder to define essential information. Below is an example configuration:

```json
{
   "id": "",
   "type": "widget",
   "name": "Simple Local Digital Clock",
   "author": "PixelBoard Team",
   "version": "1.0.0",
   "description": "A simple local digital clock widget",
   "size": [64,32],
   "fields": [],
   "preview": []
}
```

- **id**: Unique identifier for your app (assigned manually).
- **type**: Must be either `widget` or `game`.
- **name**: Display name of your app.
- **author**: Name shown in the smartphone app and website.
- **version**: App version.
- **description**: Short description for display.
- **size**: App size. Widgets can use `[128,128]`, `[128,64]`, `[128,160]`, or `[64,32]` (for PixelDart). Games must use `[128,160]`.
- **fields**: Parameters for widgets (see sections below).
- **preview**: Preview images, base64 encode data.

Further details on hardware sizes and usage will be explained in later sections.

## Pre-installed Python Modules

For widget-type apps, the following Python modules are pre-installed:
- pillow
- requests
- opencv-python
- numpy

For game-type apps, you can also use:
- pygame
- asyncio

If you need additional Python modules for your app, please let us know and we will consider adding them to the environment.

## App Types: Widgets and Games

We support two types of apps: **widgets** and **games**.
- **Widgets:** Users can enter parameters for widgets through our smartphone app. We will introduce the format and usage of specific parameter types that developers can use in the sections below.
- **Games:** Users interact with games using special darts, as well as hardware buttons and Bluetooth joy-con controllers.

## Hardware Overview: PixelDart and PixelBoard

We now support two hardware platforms: **PixelDart** and **PixelBoard**.

- **PixelDart** features two displays: one at `128x128` and another at `64x32`.
- **PixelBoard** features a single `128x128` display.

For widgets designed for PixelDart, you can use two additional sizes: `[128,160]` and `[64,32]`. For apps with size `[128,160]`, the top portion `(0,0,128,128)` of your image will be shown on the `128x128` display, while the left bottom portion `(0,128,63,159)` will be shown on the `64x32` display.

Games for PixelDart can interact with our specially designed darts and have access to 6 hardware buttons: **Up**, **Down**, **Left**, **Right**, **A**, and **B**. Bluetooth joy-con controller support will be available soon.

## Widget Parameters

Widget apps can accept user-defined parameters to customize their behavior. These parameters are specified in the `fields` array of your app's `conf.json` file. Each parameter is defined as an object with a `type`, `name`, and other relevant attributes.

For detailed usage and examples of supported parameter types, please refer to the documentation in the `Parameters Field` folder of this repository. This section provides guidance on how to define parameters such as text inputs, numbers, choices, and more.

Consult the `Parameters Field` folder for a full list of supported types and configuration options.

## Official Widget Example

Developers can find our official widget example in the `Dartsnut Official Widgets` folder of this repository. This example demonstrates the recommended app structure, configuration, and usage of widget parameters. Use it as a reference when building your own apps.

## Contributing

Contributions are welcome! Please submit pull requests or open issues for suggestions and improvements.

## License

This project is licensed under the MIT License.

