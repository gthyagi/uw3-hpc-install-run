# Versioned Gadi container validation

Run from this directory on Gadi after synchronizing this Git checkout. The
scripts validate the int32/int64 `0fb244a7` SIF files in the user's m18 storage
and use tests from the matching detached UW3 source checkout. Results go to
`/scratch/m18/$USER/container-validation/20261005/runtime-0fb244a7/` for Level 1
and `two-nodes-0fb244a7/` alongside it for the two-node job. The matching test
source is `container-validation-source-0fb244a7` in the UW3 workspace. The
existing pytest overlays from the original validation are reused; they do not
replace UW3 in the corrected image. Override `UW_VALIDATION_ROOT`,
`UW_VALIDATION_SOURCE` or `UW_TEST_OVERLAY` when validating another revision.
The two-node script accepts `UW_INT32_SIF` and `UW_INT64_SIF` overrides.

1. `qsub -v VARIANT=int32 level1.pbs`
2. Submit int64 after int32 completes using `-W depend=afterany:JOBID`.
3. Submit `two_nodes.pbs` after int64 completes.

Level 1 uses the repository's level marker exclusions, four isolated pytest
workers and a separate test-only package overlay. The native Pixi installation
is activated read-only and never rebuilt. A small 16-by-16 structured cavity
Stokes benchmark runs with four MPI ranks in both environments; nodal velocities
are compared at rtol=1e-3 and atol=1e-5. These are validation tolerances, not a
claim of bitwise reproducibility. The benchmark asserts positive SNES convergence,
finite nonzero velocity, writes the UW3 checkpoint, and separately verifies a
collective HDF5 write/read round trip. JSON records imported UW3 and MPI paths.

The two-node job reserves two full normal-queue nodes (96 CPUs) but runs two
ranks, one per node. It repeats the benchmark and compares each container against
the native two-rank reference, then runs the existing MPI latency/bandwidth
benchmark. Check the reported hostnames, MPI library, exit codes and transport
performance; successful imports alone do not establish production readiness.

Host MPI injection follows `../gadi_container_job.sh`. MPI ranks must retain
launcher environment variables, so the wrapper does not use `--cleanenv`.
Python paths and thread limits are set explicitly for the container.
