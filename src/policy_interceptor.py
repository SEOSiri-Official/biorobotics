# src/policy_interceptor.py
import hmac
import hashlib
import json

# Secret cryptographic key used to sign authorized G-code commands
POLICY_SECRET_KEY = b"seosiri_bionics_secure_key_2026"

# Immutable hardware safety boundaries (The Policy Plane)
MIN_SAFE_ANGLE = 0.0
MAX_SAFE_ANGLE = 180.0
MIN_SAFE_FEEDRATE = 100.0
MAX_SAFE_FEEDRATE = 1500.0

def enforce_hardware_policy(gcode_command: str) -> dict:
    """
    Sovereign Policy Interceptor: Independently parses raw G-code strings 
    and validates them against physical safety boundaries. If safe, generates 
    a secure cryptographic signature.
    """
    cmd = gcode_command.strip()
    
    # Enforce basic standard protocol syntax
    if not cmd.startswith("G1"):
        return {"status": "REJECTED", "reason": "UNSUPPORTED_PROTOCOL_FORMAT", "command": cmd}
        
    x_idx = cmd.find("X")
    f_idx = cmd.find("F")
    
    if x_idx == -1:
        return {"status": "REJECTED", "reason": "MISSING_AXIS_PARAMETER", "command": cmd}
        
    try:
        # Extract parameters independently of the MCP tool's calculations
        angle_str = cmd[x_idx + 1:f_idx].strip() if f_idx != -1 else cmd[x_idx + 1:].strip()
        angle = float(angle_str)
        feedrate = float(cmd[f_idx + 1:].strip()) if f_idx != -1 else 1500.0
        
        # Enforce strict, un-bypassable physical limits
        if not (MIN_SAFE_ANGLE <= angle <= MAX_SAFE_ANGLE):
            return {"status": "REJECTED", "reason": f"ANGLE_LIMIT_VIOLATION: {angle}", "command": cmd}
            
        if not (MIN_SAFE_FEEDRATE <= feedrate <= MAX_SAFE_FEEDRATE):
            return {"status": "REJECTED", "reason": f"VELOCITY_LIMIT_VIOLATION: {feedrate}", "command": cmd}
            
        # Generate HMAC-SHA256 signature to authorize the movement envelope
        payload = f"{cmd}:{angle}:{feedrate}".encode('utf-8')
        signature = hmac.new(POLICY_SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        return {
            "status": "AUTHORIZED",
            "command": cmd,
            "target_angle": angle,
            "target_feedrate": feedrate,
            "signature": signature
        }
    except Exception as e:
        return {"status": "REJECTED", "reason": f"PARSING_ERROR: {str(e)}", "command": cmd}