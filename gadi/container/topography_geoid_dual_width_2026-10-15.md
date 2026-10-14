# Feature rebuilds with PETSc int32 and int64 — 15 October 2026

The latest fetched `feature/topography-geoid-consolidation` revision is
`8541f559a1694e899c1acb375d0e884b251356cb`. It was compiled independently against
both existing SIFs. No PETSc/SIF rebuild or old-install replacement was performed;
the original home UW3 checkout stayed on `time_for_loop_in_solver`.

| Item | int32 | int64 |
| --- | --- | --- |
| Build job | `181264066.gadi-pbs` | `181264072.gadi-pbs` |
| Queue / CPUs / memory | express / 8 / 32 GB | express / 8 / 32 GB |
| Exit status / elapsed | 0 / 4:49 | 0 / 4:15 |
| Serial tests | 200 passed, 1 skipped | 200 passed, 1 skipped |
| MPI8 tests | 48 passed on each rank | 48 passed on each rank |
| PETSc version / index width | 3.25.4 / 32 bits | 3.25.4 / 64 bits |

Install prefixes:

```text
/g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-8541f559-20261015-dual-int32
/g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-8541f559-20261015-dual-int64
```

Corresponding images:

```text
/g/data/m18/tg7098/containers/underworld3/uw3-int32-0fb244a7.sif
/g/data/m18/tg7098/containers/underworld3/uw3-int64-0fb244a7.sif
```

Each build has its own fresh source checkout under
`/scratch/m18/tg7098/uw3-container-builds/topography-geoid-8541f559-20261015-dual-int{32,64}-src`.
No compiled artifacts are shared between these checkouts. The submission record
is `.../topography-geoid-8541f559-20261015-dual/submissions.json`.

The builder now accepts `PETSC_INT_BITS=32|64`, checks the selected image before
compiling and verifies the installed package/native extension origins, canonical
analytical cases, expected integer width, parallel HDF5 and MPI on one/eight ranks.
Host Open MPI 4.1.7 injection is used for MPI8. Both prefixes have the final
`INSTALL_VALIDATED` marker. The MPI selection deselects 14 existing expensive or
negative-control cases; they are not reported as MPI passes. The serial selection
covers all specified modules.

Complete provenance and test XML/runtime records are preserved under
`records/topography-geoid-8541f559-20261015-dual-int32/` and the matching int64
directory. The runtime-supported `UW_NO_USAGE_METRICS=1` disables telemetry in
these build/validation runs.

Use the matching image and package prefix together. For the benchmark runner,
set `PETSC_INT_BITS` explicitly when selecting int64; the existing int32 default
is preserved. Installation validation is not a high-resolution model accuracy
claim. No replacement Stokes model was submitted by this rebuild.
