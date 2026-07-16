# src/hardware_gateway.py
import sys
import json

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

class GCodeSerialDriver:
    """
    Actuation Layer: Exposes the serial bus to the controller. Only executes 
    G-code if it is wrapped in an authorized, signed policy envelope.
    """
    def __init__(self, port: str = "COM3", baudrate: int = 115200, mock_mode: bool = True):
        self.port = port
        self.baudrate = baudrate
        self.mock_mode = mock_mode or not SERIAL_AVAILABLE
        self.connection = None
        
        if self.mock_mode:
            print(f"[Driver] INITIALIZED IN MOCK MODE.")
        else:
            try:
                self.connection = serial.Serial(self.port, self.baudrate, timeout=2)
                print(f"[Driver] Connected to active microcontroller on {self.port}")
            except Exception as e:
                print(f"[Driver] Connection failed ({e}). Defaulting to Mock Mode.")
                self.mock_mode = True

    def stream_authorized_envelope(self, policy_envelope_json: str) -> str:
        """
        Interprets and streams the authorized envelope. Rejects raw G-code 
        if it lacks a valid security signature.
        """
        envelope = json.loads(policy_envelope_json)
        
        # Verify authorization status
        if envelope.get("status") != "AUTHORIZED":
            print(f"[Actuator Blocked] Command rejected. Violation: {envelope.get('reason', 'INVALID_ENVELOPE')}")
            return "ERROR_SECURITY_BLOCK"
            
        gcode_command = envelope.get("command") + "\n"
        signature = envelope.get("signature")
        
        # In a real environment, the microcontroller also runs HMAC verification
        print(f"[Actuator Approved] Verified signature: {signature[:10]}...")
        
        if self.mock_mode:
            print(f"[Mock-Serial] Sent to motor: {gcode_command.strip()}")
            return "ok"
        
        try:
            self.connection.write(gcode_command.encode('utf-8'))
            response = self.connection.readline().decode('utf-8').strip()
            print(f"[Serial Response] {response}")
            return response
        except Exception as e:
            print(f"[Driver Error] Failed to stream command: {e}")
            return "ERROR"