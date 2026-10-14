"""Verify the installed native extensions, PETSc index width and MPI runtime."""
import json
import inspect
from pathlib import Path
import sys

import h5py
from mpi4py import MPI
import numpy as np
from petsc4py import PETSc
import underworld3 as uw
from underworld3.cython import generic_solvers

prefix = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2])
size = int(sys.argv[3])
assert Path(uw.__file__).resolve().is_relative_to(prefix)
assert Path(generic_solvers.__file__).resolve().is_relative_to(prefix)
assert np.dtype(PETSc.IntType).itemsize == 4
assert h5py.get_config().mpi
assert MPI.COMM_WORLD.size == size
assert hasattr(generic_solvers.SNES_Stokes_SaddlePt, "rotated_solver_type")
case_modules = {}
for cls, owner in (
    (uw.analytic.KramerCylindricalStokes, "cylindrical.kramer"),
    (uw.analytic.ThieulotCylindricalStokes, "cylindrical.thieulot"),
    (uw.analytic.KramerSphericalStokes, "spherical.kramer"),
    (uw.analytic.ThieulotSphericalStokes, "spherical.thieulot"),
    (uw.analytic.ZhongSphericalStokes, "spherical.zhong"),
):
    assert cls.__module__ == "underworld3.analytic." + owner
    origin = Path(inspect.getfile(cls)).resolve()
    assert origin.is_relative_to(prefix)
    case_modules[owner] = str(origin)
assert not hasattr(uw.analytic, "Zhong2008")
assert not hasattr(uw.analytic, "Zhong")
if size > 1:
    assert "4.1.7" in MPI.Get_library_version(), "Host MPI injection was not selected"
record = {
    "rank": MPI.COMM_WORLD.rank,
    "hostname": MPI.Get_processor_name(),
    "uw_module": uw.__file__,
    "uw_native_solver": generic_solvers.__file__,
    "petsc_version": PETSc.Sys.getVersion(),
    "petsc_integer_bits": 8 * np.dtype(PETSc.IntType).itemsize,
    "petsc_scalar_bits": 8 * np.dtype(PETSc.ScalarType).itemsize,
    "parallel_hdf5": h5py.get_config().mpi,
    "mpi_library": MPI.Get_library_version(),
    "analytic_case_modules": case_modules,
}
records = MPI.COMM_WORLD.gather(record, root=0)
if MPI.COMM_WORLD.rank == 0:
    output.write_text(json.dumps({"passed": True, "ranks": records}, indent=2) + "\n")
    print("VERIFIED_INSTALL:", json.dumps(record), flush=True)
