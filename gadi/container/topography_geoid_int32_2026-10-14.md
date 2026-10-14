# Topography/geoid feature installation — 2026-10-14

Installed `feature/topography-geoid-consolidation` at
`1c1b983b1e6dfac5ab5d6c63611ee2f2fdc78c93` using the existing image:

```text
/g/data/m18/tg7098/containers/underworld3/uw3-int32-0fb244a7.sif
SHA256: 9c4543d0362b08f5ba9f58559967b4bdb983beadb17c049fcae6af7c6e00a0bd
```

UW3 native extensions were rebuilt inside that SIF. PETSc and the SIF were not
rebuilt. The original `/home/565/tg7098/underworld3` working tree and other
installations remain unchanged. A separate fresh clone selects the requested
branch and prevents mixing int32/int64 compiled artifacts.

```text
Source: /scratch/m18/tg7098/uw3-container-builds/topography-geoid-1c1b983b-int32-src
Package: /g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-1c1b983b-int32/python
Validation marker: ../INSTALL_VALIDATED
Build job: 181249649.gadi-pbs, exit 0
Build log: /scratch/m18/tg7098/uw3-container-builds/topography-geoid-1c1b983b-int32.log
```

Validation confirms imports from the rebuilt package and native solver library,
PETSc 3.25.4, 32-bit PETSc indices, 64-bit scalars and MPI-enabled HDF5.
The selected serial suite passed 138 tests with one MPI-only skip. Six native
regressions passed on all eight MPI ranks with host OpenMPI 4.1.7 injected.
They cover analytical gravity/Zhong compatibility, solver communicator/chart
restrictions, independent load moments/RHS lifetime and rotated solver policy.
These are installation regressions, not Zhong resolution-accuracy acceptance.

The job used 4 min 13 s, peak memory 4.55 GiB and 1.12 service units. Compact
runtime/test evidence is in `records/topography-geoid-1c1b983b-int32/`. Normal
host MPI injection is unchanged; container-only MPI was used only for the
serial build/test phase.

Use the existing job template with `SIF` set to the path above and `EXTRA_PKGS`
set to the package directory. The benchmark repository's targeted refinement
runner uses the same injected-runtime setup. Requested Zhong runs start at
h=1/32 using historical resource allocations; no coarse Zhong models are
submitted by this installation job.

## Targeted model submissions

The benchmark repository on Gadi was fast-forwarded to
`72f95dbac71ffaa279204516124709924e93b22e`, matching the pushed Mac source.
Untracked `gadi_records/` was preserved. The saved container launcher was
adapted from `uw3-fault-representation-benchmarks` as requested.

The following h=1/32, degree-two, mid-depth jobs were submitted after successful
installation. Each requests 48 MPI ranks, 192 GB and four hours, using the
historical 1/32 resource settings and existing reusable meshes.

| Case | PBS job |
| --- | --- |
| Isoviscous control | `181250513.gadi-pbs` |
| Layered viscosity | `181250514.gadi-pbs` |

Submission is not a claim of numerical completion or accuracy acceptance.
Outputs and logs have distinct case/job paths under
`/scratch/m18/tg7098/uw3-mantle-convection-benchmarks/output/topography_geoid/consolidation_2026-10-14/gadi_int32/`.
The model scripts verify the benchmark commit before starting; keep that
checkout at the pinned revision while these jobs are queued/running. A later
source update should use an isolated checkout or wait for completion.
