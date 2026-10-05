#!/bin/bash
# Apply the same host MPI library injection as gadi_container_job.sh.
set -euo pipefail
sif=$1
shift
HOST_LIBS=/apps/openmpi/4.1.7/lib:/apps/openmpi-mofed5.8-pbs2021.1/4.1.7/lib
HOST_LIBS=$HOST_LIBS:/apps/ucx/1.17.0/lib:/apps/ucc/1.3.0/lib:/apps/hcoll/4.8.3228/lib
HOST_LIBS=$HOST_LIBS:/opt/pbs/default/lib:/half-root/usr/lib64:/half-root/lib64
exec singularity exec \
  --bind /half-root --bind /opt/pbs/default/lib --bind /apps \
  --bind /g/data/m18 --bind /g/data/n69 --bind /scratch/m18 --bind /scratch/n69 \
  --env LD_LIBRARY_PATH="$HOST_LIBS:/usr/local/lib" \
  --env PYTHONPATH="${UW_TEST_OVERLAY:-}:/usr/local/lib:/opt/venv/lib/python3.12/site-packages" \
  --env UW_VALIDATION_OUTPUT="${UW_VALIDATION_OUTPUT:-}" \
  --env UW_REQUIRE_TWO_NODES="${UW_REQUIRE_TWO_NODES:-0}" \
  --env UW_ENABLE_TELEMETRY=0 --env OMP_NUM_THREADS=1 --env OPENBLAS_NUM_THREADS=1 \
  --env UW_MESH_CACHE_DIR="${UW_MESH_CACHE_DIR:-.meshes}" \
  "$sif" /opt/venv/bin/python3 "$@"
