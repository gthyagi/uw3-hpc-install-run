"""Compare nodal velocity from the same cavity benchmark and MPI rank count."""
import json
import sys
from pathlib import Path

import numpy as np

reference, candidate = (Path(p) for p in sys.argv[1:])
a, b = (np.load(p / "velocity.npy") for p in (reference, candidate))
assert a.shape == b.shape, (a.shape, b.shape)
np.testing.assert_allclose(a[:, :2], b[:, :2], rtol=0, atol=1e-10)
np.testing.assert_allclose(a[:, 2:], b[:, 2:], rtol=1e-3, atol=1e-5)
result = {"reference": str(reference), "candidate": str(candidate), "max_velocity_difference": float(np.max(np.abs(a[:, 2:] - b[:, 2:]))), "rtol": 1e-3, "atol": 1e-5}
(candidate / "comparison.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
