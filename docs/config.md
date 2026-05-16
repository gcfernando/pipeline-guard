# Reference: `.pipeline-guard.toml`

Drop this file at the root of your repository. All keys are optional; values shown are the built-in defaults.

```toml
# Run all detected stages; collect all failures.
fail_fast = false

# Default Docker tag used by the docker stage.
docker_tag = "pipeline-guard-local:latest"

# Run only these stages (empty = all).
only = []

# Always skip these stages.
skip = []

[stages]
python = true
node   = true
dotnet = true
go     = true
rust   = true
docker = true
vulns  = true

[timeouts]
# Seconds. Every subprocess uses one of these.
install_s = 900
build_s   = 900
test_s    = 1800
scan_s    = 600
default_s = 600

[secrets]
enabled         = true
prefer_external = true
max_file_bytes  = 1_000_000
max_files       = 10_000

# fnmatch globs, relative to repo root
allowlist_paths = [
    # "tests/fixtures/**",
    # "docs/examples/**",
]

# Rule IDs from the built-in scanner. See secrets.py for the list.
allowlist_rules = [
    # "jwt",
]

# Verbatim strings to ignore (e.g. AWS docs example keys).
allowlist_strings = [
    # "AKIAIOSFODNN7EXAMPLE",
]

[output]
# When set, write these regardless of CLI flags.
# sarif_path = "pipeline-guard.sarif"
# junit_path = "pipeline-guard-junit.xml"
# log_path   = "pipeline-guard.log"
color = true
quiet = false
```
