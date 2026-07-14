# src/hardware_gateway.py
import sys

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

class GCodeSerialDriver:
    """
    Translates physical SI meter coordinates into standardized G-code blocks 
    and handles USB/Serial streaming to microcontrollers.
    """
    def __init__(self, port: str = "COM3", baudrate: int = 115200, mock_mode: bool = True):
        self.port = port
        self.baudrate = baudrate
        self.mock_mode = mock_mode or not SERIAL_AVAILABLE
        self.connection = None
        
        if self.mock_mode:
            print(f"[Driver] INITIALIZED IN MOCK MODE (No physical port required).")
        else:
            try:
                self.connection = serial.Serial(self.port, self.baudrate, timeout=2)
                print(f"[Driver] Connected to active microcontroller on {self.port}")
            except Exception as e:
                print(f"[Driver] Physical port connection failed ({e}). Defaulting to Mock Mode.")
                self.mock_mode = True

    def stream_coordinate(self, x_meters: float) -> str:
        """
        Converts SI metric vectors to millimeter precision G-code commands.
        Example: 0.04219 meters -> G1 X42.19 F1500 (Feedrate 1500 mm/min)
        """
        # Convert SI meters to standard millimeter format
        x_millimeters = round(x_meters * 1000.0, 3)
        gcode_command = f"G1 X{x_millimeters} F1500\n"
        
        if self.mock_mode:
            print(f"[Mock-Serial] Sent: {gcode_command.strip()}")
            return "ok"
        
        try:
            self.connection.write(gcode_command.encode('utf-8'))
            response = self.connection.readline().decode('utf-8').strip()
            print(f"[Serial Response] {response}")
            return response
        except Exception as e:
            print(f"[Driver Error] Failed to stream command: {e}")
            return "ERROR"