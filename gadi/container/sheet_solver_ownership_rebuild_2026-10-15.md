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
