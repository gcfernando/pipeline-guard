# Minimal image: just the tool. Mount your repo at /work to use it.
#   docker run --rm -v "$PWD:/work" ghcr.io/gcfernando/pipeline-guard:1.0.0 --root /work
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir build && python -m build --wheel

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl
# Run as a non-root user for safety
RUN useradd --create-home --uid 1000 guard
USER guard
WORKDIR /work
ENTRYPOINT ["pipeline-guard"]
CMD ["--help"]
