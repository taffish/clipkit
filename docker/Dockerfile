# Fixed identities detect source drift; they do not guarantee future availability.
# Docker Hub, PyPI and GitHub can remove artifacts or change their delivery service.
# If an input disappears or fails verification, review the official replacement and
# rebuild a new candidate; do not silently discard hashes or rewrite old releases.
ARG PYTHON_BASE=python:3.12.16-slim-bookworm@sha256:44cf1793efa7c7a476bb0f2cff81443f4a072c90c1cb127e2924933daa3e8c64
ARG CLIPKIT_VERSION=2.16.1
ARG CLIPKIT_TAG=v2.16.1
ARG CLIPKIT_COMMIT=4e2834c001fa2c82c5921ee7e52b4a58b59e3508
ARG CLIPKIT_WHEEL_URL=https://files.pythonhosted.org/packages/d2/79/ba7bd0ee4481a9ee6aa4a97558b95a9995f06db64cbc0516680fd8dca297/clipkit-2.16.1-py3-none-any.whl
ARG CLIPKIT_WHEEL_SHA256=08c27dd017852dded330a04946ec09f323c05215ef7aa8bfb1cfc59e946e6e85
ARG CLIPKIT_SDIST_URL=https://files.pythonhosted.org/packages/f3/25/54be4d568c05c48053b3f97529ad00c077be56da2415d84b5cbab3f28984/clipkit-2.16.1.tar.gz
ARG CLIPKIT_SDIST_SHA256=9de2b3273560618fa8624733ef2aaecc604deedeb5105c74af9ec12b5f4969a0
ARG CLIPKIT_ECOMP_URL=https://raw.githubusercontent.com/JLSteenwyk/ClipKIT/4e2834c001fa2c82c5921ee7e52b4a58b59e3508/test.ecomp
ARG CLIPKIT_ECOMP_SHA256=f9f9b2a1084757586a797708a5198156347164516393462a04a5cd624d568065

FROM ${PYTHON_BASE} AS builder

ARG CLIPKIT_VERSION
ARG CLIPKIT_TAG
ARG CLIPKIT_COMMIT
ARG CLIPKIT_WHEEL_URL
ARG CLIPKIT_WHEEL_SHA256
ARG CLIPKIT_SDIST_URL
ARG CLIPKIT_SDIST_SHA256
ARG CLIPKIT_ECOMP_URL
ARG CLIPKIT_ECOMP_SHA256
ENV PYTHONNOUSERSITE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV LD_LIBRARY_PATH=/opt/clipkit/venv/lib/python3.12/site-packages/numpy.libs

RUN set -eux; \
    python -m venv /opt/clipkit/venv

ENV PATH=/opt/clipkit/venv/bin:${PATH}

WORKDIR /tmp/build
COPY docker/requirements.lock /tmp/build/requirements.lock
COPY docker/apply-report-patch.py docker/report-regression.py /tmp/build/

RUN set -eux; \
    mkdir -p /tmp/wheels /opt/clipkit/share/doc/clipkit /opt/clipkit/share/licenses/clipkit; \
    download() { \
      url="$1"; output="$2"; attempt=1; \
      while [ "$attempt" -le 3 ]; do \
        if python -c 'import shutil, sys, urllib.request; response=urllib.request.urlopen(sys.argv[1], timeout=60); output=open(sys.argv[2], "wb"); shutil.copyfileobj(response, output)' "$url" "$output"; then return 0; fi; \
        rm -f "$output"; \
        if [ "$attempt" = 3 ]; then return 1; fi; \
        attempt=$((attempt + 1)); \
        sleep 2; \
      done; \
    }; \
    download "${CLIPKIT_WHEEL_URL}" "/tmp/wheels/clipkit-${CLIPKIT_VERSION}-py3-none-any.whl"; \
    echo "${CLIPKIT_WHEEL_SHA256}  /tmp/wheels/clipkit-${CLIPKIT_VERSION}-py3-none-any.whl" | sha256sum -c -; \
    download "${CLIPKIT_SDIST_URL}" clipkit.tar.gz; \
    echo "${CLIPKIT_SDIST_SHA256}  clipkit.tar.gz" | sha256sum -c -; \
    mkdir clipkit-src; \
    tar -xzf clipkit.tar.gz -C clipkit-src --strip-components=1; \
    python -m pip download --dest /tmp/wheels --only-binary=:all: --require-hashes --no-deps -r requirements.lock; \
    python -m pip install --no-cache-dir --no-index --find-links=/tmp/wheels --no-deps \
      "clipkit==${CLIPKIT_VERSION}" \
      "biopython==1.87" \
      "numpy==1.26.4" \
      "zstandard==0.25.0"; \
    python -m pip check; \
    python /tmp/build/apply-report-patch.py /opt/clipkit/venv/lib/python3.12/site-packages/clipkit/plot_report.py /opt/clipkit/share/doc/clipkit; \
    install -m 0644 /tmp/build/report-regression.py /opt/clipkit/share/doc/clipkit/report-regression.py; \
    install -m 0644 requirements.lock /opt/clipkit/share/doc/clipkit/requirements.lock; \
    install -m 0644 clipkit-src/README.md /opt/clipkit/share/doc/clipkit/README.md; \
    install -m 0644 clipkit-src/PKG-INFO /opt/clipkit/share/doc/clipkit/PKG-INFO; \
    download "${CLIPKIT_ECOMP_URL}" /opt/clipkit/share/doc/clipkit/test.ecomp; \
    echo "${CLIPKIT_ECOMP_SHA256}  /opt/clipkit/share/doc/clipkit/test.ecomp" | sha256sum -c -; \
    install -m 0644 clipkit-src/LICENSE.md /opt/clipkit/share/licenses/clipkit/LICENSE.md; \
    { \
      echo "name=ClipKIT"; \
      echo "version=${CLIPKIT_VERSION}"; \
      echo "tag=${CLIPKIT_TAG}"; \
      echo "commit=${CLIPKIT_COMMIT}"; \
      echo "wheel=${CLIPKIT_WHEEL_URL}"; \
      echo "wheel_sha256=${CLIPKIT_WHEEL_SHA256}"; \
      echo "source=${CLIPKIT_SDIST_URL}"; \
      echo "source_sha256=${CLIPKIT_SDIST_SHA256}"; \
      echo "ecomp=${CLIPKIT_ECOMP_URL}"; \
      echo "ecomp_sha256=${CLIPKIT_ECOMP_SHA256}"; \
      echo "repo=https://github.com/JLSteenwyk/ClipKIT"; \
      echo "local_patch=report-json-escape.patch (JSON embedding only)"; \
    } > /opt/clipkit/share/doc/clipkit/source.txt; \
    clipkit --version > /tmp/clipkit-version.txt; \
    grep -Fx "clipkit ${CLIPKIT_VERSION}" /tmp/clipkit-version.txt; \
    clipkit --help > /tmp/clipkit-help.txt 2>&1; \
    grep -F "Usage: clipkit <input>" /tmp/clipkit-help.txt; \
    grep -F "remove_stop_codons" /tmp/clipkit-help.txt; \
    grep -F "ambiguity_handling" /tmp/clipkit-help.txt; \
    python -c "import Bio, clipkit, numpy, zstandard; from clipkit.modes import AmbiguityHandling; from clipkit.version import __version__; assert __version__ == '${CLIPKIT_VERSION}'; assert AmbiguityHandling.missing.value == 'missing'"; \
    find /opt/clipkit/venv -type f -name '*.so' -print0 | xargs -0 -r ldd > /tmp/clipkit-ldd.txt; \
    if grep -F "not found" /tmp/clipkit-ldd.txt; then exit 1; fi; \
    python -m pip uninstall -y pip setuptools wheel packaging; \
    find /opt/clipkit -type d -name '__pycache__' -prune -exec rm -rf '{}' +; \
    find /opt/clipkit -type f -name '*.a' -delete; \
    find /opt/clipkit -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete; \
    python -c 'import importlib.metadata as m; rows = sorted("{}=={}".format(d.metadata["Name"], d.version) for d in m.distributions() if d.metadata["Name"]); open("/opt/clipkit/share/doc/clipkit/python-packages.txt", "w").write("\n".join(rows) + "\n")'

FROM ${PYTHON_BASE}

ARG CLIPKIT_VERSION
ARG CLIPKIT_COMMIT
ENV PYTHONNOUSERSITE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LD_LIBRARY_PATH=/opt/clipkit/venv/lib/python3.12/site-packages/numpy.libs

COPY --from=builder /opt/clipkit /opt/clipkit

ENV PATH=/opt/clipkit/venv/bin:${PATH}

# Keep build gates architecture-neutral and small. Rich HTML, API and large-MSA
# assertions run after the build on the actual native backends, not under QEMU.
RUN set -eux; \
    command -v clipkit >/dev/null; \
    command -v python >/dev/null; \
    command -v python3 >/dev/null; \
    command -v bash >/dev/null; \
    command -v gzip >/dev/null; \
    command -v ldd >/dev/null; \
    clipkit --version > /tmp/clipkit-version.txt; \
    grep -Fx "clipkit ${CLIPKIT_VERSION}" /tmp/clipkit-version.txt; \
    clipkit --help > /tmp/clipkit-help.txt 2>&1; \
    grep -F "Usage: clipkit <input>" /tmp/clipkit-help.txt; \
    grep -F "remove_stop_codons" /tmp/clipkit-help.txt; \
    grep -F "ambiguity_handling" /tmp/clipkit-help.txt; \
    grep -F "commit=${CLIPKIT_COMMIT}" /opt/clipkit/share/doc/clipkit/source.txt >/dev/null; \
    python -c "import Bio, clipkit, numpy, zstandard; from clipkit.modes import AmbiguityHandling; from clipkit.version import __version__; assert __version__ == '${CLIPKIT_VERSION}'; assert AmbiguityHandling.missing.value == 'missing'"; \
    find /opt/clipkit/venv -type f -name '*.so' -print0 | xargs -0 -r ldd > /tmp/clipkit-ldd.txt; \
    if grep -F "not found" /tmp/clipkit-ldd.txt; then exit 1; fi; \
    mkdir -p /tmp/clipkit-check; \
    cd /tmp/clipkit-check; \
    printf '>s1\nACGTACGT\n>s2\nACGTA-GT\n>s3\nACGTA-GT\n>s4\nACGTA-GT\n' > in.fa; \
    clipkit in.fa -m gappy -g 0.5 -o out.fa -of fasta --report_json report.json > run.log 2>&1 || { cat run.log; exit 1; }; \
    test -s out.fa; \
    test -s report.json; \
    grep -F ">s1" out.fa >/dev/null; \
    grep -F "Trimmed alignment: out.fa" run.log >/dev/null; \
    python -c 'import json; data=json.load(open("report.json")); assert data["status"] == "completed"; assert data["mode"] == "gappy"'; \
    cp /opt/clipkit/share/doc/clipkit/test.ecomp in.ecomp; \
    clipkit in.ecomp -o ecomp.fa -of fasta -q; \
    test -s ecomp.fa; \
    cd /; \
    rm -rf /tmp/clipkit-check; \
    rm -f /tmp/clipkit-version.txt /tmp/clipkit-help.txt /tmp/clipkit-ldd.txt

WORKDIR /data

ENV TAFFISH_ENV=TAFFISH
ENV TAFFISH_NAME=clipkit
