"""A sourceless unittest driver loads its test's .pyc under manifest-only runfiles."""

import os
import subprocess
import sys

runfiles_dir = os.environ["RUNFILES_DIR"]
manifest = os.path.join(runfiles_dir, "MANIFEST")
unittest = os.path.join(runfiles_dir, "_main/venv-manifest-runfiles-1378/manifest_unittest_sourceless")

with open(manifest, encoding="utf-8") as f:
    entries = {line.partition(" ")[0] for line in f}
assert "_main/venv-manifest-runfiles-1378/manifest_unittest_test.py" not in entries, "source shipped beside sourceless bytecode"

# A decoy at the test's runfiles-relative path in the working directory must never be loaded.
decoy_cwd = os.path.join(os.environ["TEST_TMPDIR"], "decoy")
os.makedirs(os.path.join(decoy_cwd, "venv-manifest-runfiles-1378"), exist_ok=True)
with open(os.path.join(decoy_cwd, "venv-manifest-runfiles-1378", "manifest_unittest_test.py"), "w") as f:
    f.write("raise AssertionError('decoy source loaded from the working directory')\n")

env = {k: v for k, v in os.environ.items() if k != "RUNFILES_DIR"}
env["RUNFILES_MANIFEST_FILE"] = manifest
sys.exit(subprocess.run([unittest], cwd=decoy_cwd, env=env).returncode)
