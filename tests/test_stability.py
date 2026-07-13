# tests/test_stability.py
from src.core_math import compute_normalized_kinematic_intent

def test_math_determinism():
    """Ensure the math always returns the exact same value for the same input."""
    input_val = 50.0
    result = compute_normalized_kinematic_intent(input_val, "test")
    
    # Assert specific known value (0.462117...) from your previous successful run
    assert round(result['intent_vector'], 6) == 0.462117
    print("Stability Test Passed: Logic is deterministic.")

if __name__ == "__main__":
    test_math_determinism()