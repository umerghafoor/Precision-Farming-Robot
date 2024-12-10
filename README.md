# Precision-Farming-Robot

```shell
 .\mosquitto_pub.exe -t robot/control -h <BROKER_IP> -m JSON_MESSAGE
 .\mosquitto_sub.exe -t robot/control -h 192.168.240.180
```

## **Movmenents**

### 1. **Forward Movement**

```json
{"command": "FORWARD", "speed": 100, "continuous": true}
```

### 2. **Backward Movement**

```json
{"command": "BACKWARD", "speed": 100, "continuous": true}
```

### 3. **Turning Left**

```json
{"command": "LEFT", "speed": 100, "continuous": true}
```

### 4. **Turning Right**

```json
{"command": "RIGHT", "speed": 100, "continuous": true}
```

### 5. **Stopping the Motors**

```json
{"command": "STOP"}
```

### 6. **Controlling the Servo**

```json
{"command": "SERVO", "angle": 45}
```
