# Robot Hardware Configuration

This folder includes the pin mapping and hardware setup for controlling the robot actuators and peripherals.

## Pin Configuration

### Motor Driver Pins

| Motor   | Enable Pin | IN1  | IN2  |
|---------|------------|------|------|
| M1      | 21         | 22   | 23   |
| M2      | 5          | 18   | 19   |
| M3      | 15         | 0    | 2    |
| M4      | 17         | 16   | 4    |

### Servo Motor

- **Servo Pin**: `32`

## Hardware Components

1. **ESP32 Development Board**
2. **Motor Driver (L298N or similar)**
3. **DC Motors** (4 Motors for M1, M2, M3, M4)
4. **Servo Motor**
5. **Power Supply**: Ensure appropriate voltage and current for motors and ESP32.

## Wiring Diagram

- Connect the motor driver pins to the corresponding ESP32 pins as listed above.
- Attach the servo motor control pin to GPIO `32`.
- Power motors using an external power source for stable operation.
