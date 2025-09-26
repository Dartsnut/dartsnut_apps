# Parameters Field & `conf.json` Introduction

This document explains the purpose of the `conf.json` configuration file and the Parameters Field for user input in Dartsnut apps.

## `conf.json` Overview

The "fields" in `conf.json` file stores configuration settings for each app. It defines available parameters, their types, default values, and constraints. Example:

```json
{
    ...
    ...
    "fields": [
        {
            "id": "city", 
            "name": "City",
            "type": "text",
            "desc": "The city name for the clock, e.g., New york",
            "default": ""
        },
        {
            "id": "temperature_unit", 
            "name": "Temperature Unit",
            "type": "dropdown",
            "desc": "Temperature unit to use",
            "options": [
                {
                    "display": "Celsius",
                    "value": "celsius"
                },
                {
                    "display": "Fahrenheit",
                    "value": "fahrenheit"
                }
            ],
            "default": "celsius"
        }
    ],
    ...
    ...
}
```

## How It Works

The `conf.json` file defines the parameters required by your Dartsnut app. When the app is launched, our smartphone application reads these definitions and presents a user-friendly input interface for each parameter type. Users enter their values, which are then passed to the app through our system.

Developers can access these user-provided parameters using the `pydartsnut` middleware module. Each parameter's value can be retrieved from a dictionary using its `id` as the key. For more details, refer to the [pydartsnut GitHub repository](https://github.com/Dartsnut/pydartsnut.git).

## Common Field Properties

Each field in the `fields` array should include the following basic properties:

- **id**: Unique identifier for the parameter. Must be unique across all fields.
- **name**: Display name shown in the Dartsnut app.
- **type**: Data type of the parameter (e.g., `text`, `dropdown`).
- **desc**: Short description displayed in the Dartsnut app.
- **default**: Default value shown to users in the Dartsnut app.

## Parameter Types

### 1. `text`
A text parameter allows users to input free-form text. It is commonly used for names, labels, or any string value. 
Example configuration:

```json
{
    "id": "city",
    "name": "City",
    "type": "text",
    "desc": "The city name for the clock, e.g., New York",
    "default": ""
}
```

Example field parameter:

```json
{
    "city": "Hongkong"
}
```

### 2. `color`
A color parameter enables users to select a color using a color picker in the Dartsnut app. The selected value is returned as a string in the `"#RRGGBB"` format. 
Example configuration:

```json
{
    "id": "background_color",
    "name": "Background Color",
    "type": "color",
    "desc": "Choose the background color for the app",
    "default": "#FFFFFF"
}
```

Example field parameter:

```json
{
    "background_color": "#123456"
}
```

### 3. `dropdown`
A dropdown parameter lets users select one option from a predefined list. Each option includes a display name (shown in the Dartsnut app) and a value (passed to the app). The `default` property should be set to one of the option values, not the display name. 
Example configuration:

```json
{
    "id": "temperature_unit",
    "name": "Temperature Unit",
    "type": "dropdown",
    "desc": "Temperature unit to use",
    "options": [
        {
            "display": "Celsius",
            "value": "celsius"
        },
        {
            "display": "Fahrenheit",
            "value": "fahrenheit"
        }
    ],
    "default": "celsius"
}
```

Example field parameter:

```json
{
    "temperature_unit": "celsius"
}
```

### 4. `toggle`
A toggle parameter provides a simple on/off switch for users. The value returned is typically a boolean (`true` or `false`). 
Example configuration:

```json
{
    "id": "show_seconds",
    "name": "Show Seconds",
    "type": "toggle",
    "desc": "Enable to display seconds on the clock",
    "default": false
}
```

Example field parameter:

```json
{
    "show_seconds": false
}
```

### 5. `number`
A number parameter allows users to input numeric values. You can specify constraints such as minimum, maximum. 
Example configuration:

```json
{
    "id": "refresh_interval",
    "name": "Refresh Interval",
    "type": "number",
    "desc": "Time in seconds between data refreshes",
    "default": 60,
    "min": 10,
    "max": 3600,
}
```

Example field parameter:

```json
{
    "refresh_interval": 120
}
```

### 6. `slider`
A slider parameter allows users to select a numeric value within a specified range using a slider control. You can define the minimum, maximum, and step values. 
Example configuration:

```json
{
    "id": "volume",
    "name": "Volume",
    "type": "slider",
    "desc": "Adjust the app's volume level",
    "default": 50,
    "min": 0,
    "max": 100,
    "step": 1
}
```

Example field parameter:

```json
{
    "volume": 50
}
```

### 7. `checkbox`
A checkbox parameter allows users to select multiple options from a predefined list. The value returned is an array of selected option values. 
Example configuration:

```json
{
    "id": "features",
    "name": "Features",
    "type": "checkbox",
    "desc": "Select the features to enable",
    "options": [
        {
            "display": "Alarm",
            "value": "alarm"
        },
        {
            "display": "Timer",
            "value": "timer"
        },
        {
            "display": "Stopwatch",
            "value": "stopwatch"
        }
    ],
    "default": ["alarm", "timer"]
}
```

Example field parameter:

```json
{
    "features": ["alarm", "timer"]
}
```

### 8. `location`

A `location` parameter allows users to input a location name, which uses autocomplete to help users select a proper location from a list. The value returned is an object containing the location's name, latitude, longitude, and timezone. Example configuration:
Example configuration:

```json
{
    "id": "city",
    "name": "City",
    "type": "location",
    "desc": "Input your city name",
    "default": {
        "name": "",
        "lat": 0.0,
        "lng": 0.0,
        "timezone": ""
    }
}
```

Example field parameter:

```json
{
    "city": {
        "name": "Hongkong",
        "lat": 22.302711,
        "lng": 114.177216,
        "timezone": "Asia/Hong_Kong"
    }
}
```

### 9. `image`

An `image` parameter allows users to submit an images through the Dartsnut app interface. Developers can specify the required aspect ratio for the image using the `aspectio` property (e.g., `"aspectio": [16,9]`). The app will guide users to crop their images to match the specified aspect ratio before uploading. The value returned is an object containing the temporary file path referencing the uploaded image and the crop box coordinate.
Example configuration:

```json
{
    "id": "cover_image",
    "name": "Cover Image",
    "type": "image",
    "desc": "Upload a cover image (16:9 aspect ratio)",
    "aspectio": "16:9",
    "default": ""
}
```

Example field parameter:

```json
{
    "cover_image": {
        "image": "temp_path_of_the_image",
        "cropbox": [0,0,1920,1080]
    }
}
```

## Extending Parameter Types

We are continuously improving the Dartsnut platform and will introduce more parameter types as necessary. If you need a specific parameter type that is not currently supported, please feel free to raise your request. Developers are encouraged to suggest new parameter types or features by contacting our team or submitting an issue on our [GitHub repository](https://github.com/Dartsnut/dartsnut_apps.git).