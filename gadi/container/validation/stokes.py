"""
Stokes flow test for Gadi parallel run.

Lid-driven cavity variant: top wall moves at (1, 0), bottom at (-1, 0),
left and right walls are free-slip. Uniform viscosity, no body force.
Verifies that mpi4py, petsc4py, h5py, and underworld3 all work correctly
in a multi-rank MPI context.

Usage:
    mpirun -n 4 python3 test_stokes_gadi.py
    # or via PBS job script: qsub gadi_job_uw3.sh
"""

import os
import json
import socket
from pathlib import Path
import h5py
import mpi4py.MPI as MPI
from petsc4py import PETSc
import underworld3 as uw
import numpy as np
import sympy

comm = MPI.COMM_WORLD

uw.pprint(f"==> Stokes flow test — {comm.size} MPI rank(s)")
uw.pprint(f"    underworld3: {uw.__version__}")

# ============================================================
# PARAMETERS
# ============================================================

res  = 16    # mesh resolution — quick test
visc = 1.0   # uniform viscosity

outputPath = os.environ["UW_VALIDATION_OUTPUT"]
if comm.rank == 0:
    os.makedirs(outputPath, exist_ok=True)
comm.Barrier()
hosts = comm.allgather(socket.gethostname())
if os.environ.get("UW_REQUIRE_TWO_NODES") == "1":
    assert len(set(hosts)) == 2, hosts

# ============================================================
# MESH
# ============================================================

mesh = uw.meshing.StructuredQuadBox(
    minCoords=(0.0, 0.0), maxCoords=(1.0, 1.0), elementRes=(res, res), qdegree=2
)

# ============================================================
# VARIABLES
# ============================================================

v = uw.discretisation.MeshVariable("U", mesh, mesh.dim, degree=2)
p = uw.discretisation.MeshVariable("P", mesh, 1,        degree=1)

# ============================================================
# STOKES SOLVER
# ============================================================

stokes = uw.systems.Stokes(mesh, velocityField=v, pressureField=p)
stokes.constitutive_model = uw.constitutive_models.ViscousFlowModel
stokes.constitutive_model.Parameters.viscosity = visc
stokes.bodyforce = sympy.Matrix([0, 0])

# Top:    vx =  1, vy = 0
# Bottom: vx = -1, vy = 0
# Left/Right: free-slip (no normal velocity, tangential stress-free)
stokes.add_dirichlet_bc(( 1.0, 0.0), "Top",    (0, 1))
stokes.add_dirichlet_bc((-1.0, 0.0), "Bottom", (0, 1))
stokes.add_dirichlet_bc((0.0,),      "Left",   (0,))
stokes.add_dirichlet_bc((0.0,),      "Right",  (0,))

stokes.tolerance = 1.0e-4
stokes.petsc_options["snes_converged_reason"] = None
stokes.petsc_options["snes_monitor_short"] = None

uw.pprint("==> Solving...")
stokes.solve()
assert stokes.snes.getConvergedReason() > 0
uw.pprint("==> Solve complete")

# ============================================================
# SANITY CHECK — max velocity should be nonzero
# ============================================================

with mesh.access(v):
    vmax_local = float(np.abs(v.data).max()) if v.data.shape[0] > 0 else 0.0

vmax = comm.allreduce(vmax_local, op=MPI.MAX)

uw.pprint(f"==> Max |velocity|: {vmax:.4e}")
assert np.isfinite(vmax) and vmax > 0
with mesh.access(v, p):
    samples = comm.gather(np.column_stack((v.coords.copy(), v.data.copy())), root=0)
    assert np.isfinite(v.data).all() and np.isfinite(p.data).all()
if comm.rank == 0:
    samples = np.concatenate(samples)
    samples = samples[np.lexsort((samples[:, 1], samples[:, 0]))]
    np.save(Path(outputPath) / "velocity.npy", samples)
    metrics = {"petsc_version": PETSc.Sys.getVersion(), "index_bits": np.dtype(PETSc.IntType).itemsize * 8, "numpy_version": np.__version__, "uw3_file": uw.__file__, "mpi_library": MPI.Get_library_version(), "hosts": hosts, "ranks": comm.size, "vmax": vmax, "snes_reason": int(stokes.snes.getConvergedReason())}
    (Path(outputPath) / "metrics.json").write_text(json.dumps(metrics, indent=2))

# Exercise collective write and read independently of the checkpoint format.
assert h5py.get_config().mpi
with h5py.File(Path(outputPath) / "parallel.h5", "w", driver="mpio", comm=comm) as f:
    ds = f.create_dataset("rank", (comm.size,), dtype="i8")
    ds[comm.rank] = comm.rank
comm.Barrier()
with h5py.File(Path(outputPath) / "parallel.h5", "r", driver="mpio", comm=comm) as f:
    assert np.array_equal(f["rank"][:], np.arange(comm.size))

# ============================================================
# SAVE — tests parallel HDF5 write via h5py
# ============================================================

if comm.rank == 0:
    os.makedirs(outputPath, exist_ok=True)

mesh.petsc_save_checkpoint(
    index=0,
    meshVars=[v, p],
    outputPath=outputPath,
)

uw.pprint(f"==> Output saved to {outputPath}/")
uw.pprint("==> All checks passed — mpi4py, petsc4py, h5py, underworld3 OK")
