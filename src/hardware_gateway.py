import json
# import serial # Uncomment when connecting real hardware

def send_to_robot(mcp_json_payload: str):
    data = json.loads(mcp_json_payload)
    x_val = data.get("vectors_meters", {}).get("x_axis_delta", 0)
    # Mapping SI meters to PWM representation
    pwm_value = int((x_val + 1.0) * 32768)
    command = f"X:{pwm_value};\n"
    print(f"Gateway: Sending to hardware -> {command}")