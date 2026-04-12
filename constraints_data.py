from dataclasses import dataclass
import numpy as np

@dataclass
class ConstraintCurves:
    ws: np.ndarray
    tw_cruise: np.ndarray
    tw_climb: np.ndarray
    tw_turn: np.ndarray
    tw_ceiling: np.ndarray
    ws_stall: float