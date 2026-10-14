# Layered sheet-load int32 rebuild — 15 October 2026

UW3 feature `f9ff739189956be64152b9c7582b8905eb02e0bb` extends the owned-facet
linear P2 radial-sheet adapter to fixed spatial viscosity. Velocity-, pressure-
and velocity-gradient-dependent viscosity remain rejected. Independent tests
cover force integrals, zero rotational moments and native residual/Jacobian
consistency with smooth and layered viscosity.

Gadi job **181268880.gadi-pbs** rebuilt the feature against the existing PETSc
3.25.4 int32 image. It exited 0 in 4:26, using express, 8 CPUs and 32 GB, with
peak memory 5.08 GB. Validation passed **205 serial tests** (one skipped) and
**53 tests on each MPI8 rank** (14 deselected on each rank).

```text
Source:  /scratch/m18/tg7098/uw3-container-builds/topography-geoid-f9ff7391-st7-sheet-int32-src
Install: /g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-f9ff7391-st7-sheet-int32
Image:   /g/data/m18/tg7098/containers/underworld3/uw3-int32-0fb244a7.sif
```

The package/native origins, index width, parallel HDF5 and host Open MPI
injection passed the runtime checks. The installation has `INSTALL_VALIDATED`.
Exact source/image/runtime/JUnit records are under
`records/topography-geoid-f9ff7391-st7-sheet-int32/`.

The original home checkout remains on `time_for_loop_in_solver`; older prefixes,
PETSc and both SIFs are preserved. No int64 build or job was submitted for this
update. Installation validation does not establish the full layered-model
convergence or analytical accuracy; those are separate benchmark gates.
