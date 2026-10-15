# Postprocessing docstrings: int32 installation — 15 October 2026

UW3 feature `e33878a6b64e575e1f165231dd974c5388e50e6f` documents the public
postprocessing APIs. All seven modified numerical source files have unchanged
executable ASTs relative to validated `f9ff7391`; signatures and numerical
behavior are unchanged. The isolated Mac build and focused Sphinx page pass.

Fresh Gadi source/install:

```text
Source:  /scratch/m18/tg7098/uw3-container-builds/topography-geoid-e33878a6-docs-int32-src
Install: /g/data/m18/tg7098/containers/underworld3/builds/topography-geoid-e33878a6-docs-int32
Image:   /g/data/m18/tg7098/containers/underworld3/uw3-int32-0fb244a7.sif
```

Build `181290547` compiled UW3 and passed 205 serial tests (one skipped), plus
serial/MPI8 package, native-origin, HDF5 and int32 checks. MPI pytest collection
then encountered a partially initialized UW3 import and stalled. Its logs were
preserved and that attempt stopped; it did not write a validation marker.

Validation-only job `181291617` reused the compiled package, importing UW3
before invoking pytest. The collection guard and host MPI injection remained
enabled/unchanged; no assertion or test selector was relaxed. All 53 selected
tests passed on each of eight ranks (14 deselected), and the installed docs
audit verified 20 public functions, 200 arguments, eight response classes and
exact source/package Python matches. The job exited 0 in 25 seconds and wrote
`INSTALL_VALIDATED`. The bootstrap, PBS continuation and compact results are
retained under `records/topography-geoid-e33878a6-docs-int32/`.

The original home source checkout remains on `time_for_loop_in_solver` at
`6c4b5794`; source changes were fetched without switching/resetting it. Earlier
installations, PETSc and SIFs are preserved. No benchmark model or int64 job
was submitted. The original collection failure remains a test-harness issue
to investigate separately; this record documents the successful explicit-import
gate and does not claim a general UW3 import fix.
