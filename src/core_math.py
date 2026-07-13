import math
from typing import Dict, Any

def compute_normalized_kinematic_intent(bio_metric: float, operational_mode: str) -> Dict[str, Any]:
    # Using hyperbolic tangent for stability (result -1.0 to 1.0)
    normalized_signal = math.tanh(bio_metric / 100.0)
    return {
        "intent_vector": normalized_signal,
        "mode_context": operational_mode.upper()
    }