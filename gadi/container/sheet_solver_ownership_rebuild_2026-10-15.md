# Solver-owned sheet API int32 rebuild — 15 October 2026

Requested UW3 source: `3abcd3f3d7c87a81c1a6fb0d403b93f92a9d3ccd` on
`feature/topography-geoid-consolidation`. Build into a fresh source/install pair
using the existing `/g/data/m18/tg7098/containers/underworld3/uw3-int32-0fb244a7.sif`.
Keep PETSc, SIF, old prefixes and the home UW3 checkout unchanged.

The build template now imports installed UW3 before pytest collection, using the
bootstrap proven by the earlier e33878a6 validation. Serial/MPI gates include the
Poisson pool/volume/source-method tests alongside analytical and Stokes lifetime
regressions. The verifier checks both new solver methods and their private utility
origins inside the selected prefix, in addition to native/Python origins, int32,
parallel HDF5, canonical analytical cases and host Open MPI injection.

Commit and synchronize this operations repository and the benchmark repository
before submitting the build. Submit the models only after INSTALL_VALIDATED is
written by a successful build/validation job. The benchmark PBS runner pins both
sources and the image checksum and gives every job a distinct output directory.

Requested production checks are one h=1/32 free-slip delta case per geometry:

- Spherical Kramer degree 2/order 0/cos: 48 CPUs, 192 GB, express, six-hour cap.
  Stokes tolerance stays 1e-9; physical Poisson/self-gravity uses the existing
  full-ball h=1/32 parent mesh and tolerance 1e-10. This exercises both new methods.
- Annulus Kramer case1/wavenumber 2: 16 CPUs, 64 GB, express, two-hour cap.
  Stokes tolerance stays 1e-9; Poisson/self-gravity defaults stay 1e-10. Sixteen
  CPUs match the retained h=1/32 Stokes and gravity resource allocation.

These check implementation and analytical errors, not resolution sufficiency or
completion of the separate mean-correction/layered-velocity accuracy audits.
Job IDs, gates and measured results are added after execution. No int64 job is
requested.

## Completed installation gate

Build `181295353.gadi-pbs` exited 0 in 4:27, peak memory 5,151,168 KB.
235 serial tests passed (one skipped), and 70 passed on every MPI8 rank
(14 deselected per rank). Both new solver methods and utility origins pass.
The installation is validated at
`/g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-3abcd3f3-sheet-api-int32`.
Compact records are in `records/topography-geoid-3abcd3f3-sheet-api-int32/`.

Only after that gate passed, submitted spherical `181295591.gadi-pbs` and
annulus `181295592.gadi-pbs`, using immutable benchmark `ce1e003a33d23498060c007314df911c990629e6`
and operations `dcde75a90c8cb43e2acb5c93c2961d1533c5c19b` worktrees. Model completion
and accuracy are recorded separately in the benchmark repository.

## Poisson operator-initialization correction

Validated UW3 source `0b365d32fc9db44069faea753da118e3ff07315a` fixes the
sheet-correction helper when the homogeneous base Poisson solve converges in
zero Newton iterations, leaving its Jacobian unassembled. The helper assembles
the configured native Jacobian before the sheet correction in that case.
Source signs, mean correction and physical boundary data are unchanged.

The build runner's serial and MPI8 lists include
`test_1088_spherical_sheet_operator_initialization.py` (runner change
`055e899caacfabab34ffa9a015942bbd99bcf441`). Its four native component cases cover
Newton/`ksponly` and Dirichlet/Robin conditions, repeated signed/zero loads,
linearity and fixed fields/native handles. These are implementation checks;
physical spherical accuracy and measured memory improvement remain separate.

The next single batched rebuild uses express, eight CPUs, 32 GB and a one-hour
cap against the existing int32 SIF above. Fresh source and installation paths:

- `/scratch/m18/tg7098/uw3-container-builds/topography-geoid-0b365d32fc9d-sheet-jac-int32-src`
- `/g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-0b365d32fc9d-sheet-jac-int32`

Use a fresh independent shared clone on the feature branch, rather than moving
the home checkout or previous source branches. Preserve PETSc, SIF, old installs
and Gadi records. Deployment metadata, submitted job ID and final gates will be
added here after submission; no physical benchmark is submitted by the build.
