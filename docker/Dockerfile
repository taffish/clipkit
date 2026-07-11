ARG CLIPKIT_VERSION=2.12.2
ARG CLIPKIT_TAG=v2.12.2
ARG CLIPKIT_COMMIT=fa656cb6532aa3fb4c22ecef3b44721c658e283d
ARG CLIPKIT_WHEEL_URL=https://files.pythonhosted.org/packages/e8/d7/e5920b04122002d77f9c3026d0fa0c94c24e276b6b1f02a0405039e0e10a/clipkit-2.12.2-py3-none-any.whl
ARG CLIPKIT_WHEEL_SHA256=b9074ba75ef0a1217b2c4c7aed36ca927c3664117d59f28a9844cc539c6c0630
ARG CLIPKIT_SDIST_URL=https://files.pythonhosted.org/packages/1d/cc/5cc05e2117f097ab8aab447b968d2d3f188b1fcc3c8c6b49d2c23ae4b2dc/clipkit-2.12.2.tar.gz
ARG CLIPKIT_SDIST_SHA256=bdc1e7f0d8da34e8a8622715de7203edf51da47d8163cc78799b923a7be0e2b4
ARG CLIPKIT_ECOMP_URL=https://raw.githubusercontent.com/JLSteenwyk/ClipKIT/v2.12.2/test.ecomp
ARG CLIPKIT_ECOMP_SHA256=f9f9b2a1084757586a797708a5198156347164516393462a04a5cd624d568065

FROM python:3.11-slim-bookworm AS builder

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
ENV LD_LIBRARY_PATH=/opt/clipkit/venv/lib/python3.11/site-packages/numpy.libs

RUN set -eux; \
    python -m venv /opt/clipkit/venv

ENV PATH=/opt/clipkit/venv/bin:${PATH}

RUN set -eux; \
    python -m pip install --no-cache-dir --upgrade \
      "pip==26.1.1" \
      "setuptools==82.0.1" \
      "wheel==0.47.0"

WORKDIR /tmp/build

RUN set -eux; \
    mkdir -p /tmp/wheels /opt/clipkit/share/doc/clipkit /opt/clipkit/share/licenses/clipkit; \
    download() { \
      url="$1"; output="$2"; attempt=1; \
      while [ "$attempt" -le 3 ]; do \
        if python -c 'import sys, urllib.request; urllib.request.urlretrieve(sys.argv[1], sys.argv[2])' "$url" "$output"; then return 0; fi; \
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
    python -m pip wheel --wheel-dir /tmp/wheels --only-binary=:all: \
      "biopython==1.87" \
      "numpy==1.26.4" \
      "zstandard==0.25.0"; \
    python -m pip install --no-cache-dir --no-index --find-links=/tmp/wheels \
      "clipkit==${CLIPKIT_VERSION}" \
      "biopython==1.87" \
      "numpy==1.26.4" \
      "zstandard==0.25.0"; \
    install -m 0644 clipkit-src/README.md /opt/clipkit/share/doc/clipkit/README.md; \
    install -m 0644 clipkit-src/PKG-INFO /opt/clipkit/share/doc/clipkit/PKG-INFO; \
    download "${CLIPKIT_ECOMP_URL}" /opt/clipkit/share/doc/clipkit/test.ecomp; \
    echo "${CLIPKIT_ECOMP_SHA256}  /opt/clipkit/share/doc/clipkit/test.ecomp" | sha256sum -c -; \
    install -m 0644 clipkit-src/LICENSE.md /opt/clipkit/share/licenses/clipkit/LICENSE.md; \
    python -m pip freeze | sort > /opt/clipkit/share/doc/clipkit/python-packages.txt; \
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
    } > /opt/clipkit/share/doc/clipkit/source.txt; \
    clipkit --version | grep -Fx "clipkit ${CLIPKIT_VERSION}" >/dev/null; \
    clipkit --help 2>&1 | grep -F "Usage: clipkit <input>" >/dev/null; \
    python -c "import Bio, clipkit, numpy, zstandard; from clipkit.version import __version__; assert __version__ == '${CLIPKIT_VERSION}'"; \
    find /opt/clipkit/venv -type f -name '*.so' -print0 | xargs -0 -r ldd > /tmp/clipkit-ldd.txt; \
    if grep -F "not found" /tmp/clipkit-ldd.txt; then exit 1; fi; \
    python -m pip uninstall -y pip setuptools wheel packaging; \
    find /opt/clipkit -type d -name '__pycache__' -prune -exec rm -rf '{}' +; \
    find /opt/clipkit -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

FROM python:3.11-slim-bookworm

ARG CLIPKIT_VERSION
ARG CLIPKIT_COMMIT
ENV PYTHONNOUSERSITE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LD_LIBRARY_PATH=/opt/clipkit/venv/lib/python3.11/site-packages/numpy.libs

COPY --from=builder /opt/clipkit /opt/clipkit

ENV PATH=/opt/clipkit/venv/bin:${PATH}

RUN set -eux; \
    command -v clipkit >/dev/null; \
    command -v python >/dev/null; \
    command -v python3 >/dev/null; \
    command -v bash >/dev/null; \
    command -v gzip >/dev/null; \
    command -v ldd >/dev/null; \
    clipkit --version | grep -Fx "clipkit ${CLIPKIT_VERSION}" >/dev/null; \
    clipkit --help 2>&1 | grep -F "Usage: clipkit <input>" >/dev/null; \
    grep -F "commit=${CLIPKIT_COMMIT}" /opt/clipkit/share/doc/clipkit/source.txt >/dev/null; \
    python -c "import Bio, clipkit, numpy, zstandard; from clipkit.version import __version__; assert __version__ == '${CLIPKIT_VERSION}'"; \
    find /opt/clipkit/venv -type f -name '*.so' -print0 | xargs -0 -r ldd > /tmp/clipkit-ldd.txt; \
    if grep -F "not found" /tmp/clipkit-ldd.txt; then exit 1; fi; \
    mkdir -p /tmp/clipkit-check; \
    cd /tmp/clipkit-check; \
    printf '>s1\nACGTACGT\n>s2\nACGTA-GT\n>s3\nACGTA-GT\n>s4\nACGTA-GT\n' > in.fa; \
    clipkit in.fa -m gappy -g 0.5 -o out.fa -of fasta --report_json report.json > run.log 2>&1; \
    test -s out.fa; \
    test -s report.json; \
    grep -F ">s1" out.fa >/dev/null; \
    grep -F "Trimmed alignment: out.fa" run.log >/dev/null; \
    python -c 'import json; data=json.load(open("report.json")); assert data["status"] == "completed"; assert data["mode"] == "gappy"'; \
    cp /opt/clipkit/share/doc/clipkit/test.ecomp in.ecomp; \
    clipkit in.ecomp -o ecomp.fa -of fasta -q; \
    test -s ecomp.fa; \
    cd /; \
    rm -rf /tmp/clipkit-check

WORKDIR /data

ENV TAFFISH_ENV=TAFFISH
ENV TAFFISH_NAME=clipkit
