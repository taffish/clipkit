ARG CLIPKIT_VERSION=2.12.0
ARG CLIPKIT_TAG=v2.12.0
ARG CLIPKIT_COMMIT=feb0a07903542f1b6b127b12d42065d93cd9f3e8
ARG CLIPKIT_WHEEL_URL=https://files.pythonhosted.org/packages/73/83/2039f07a32a84e0d094de1193f6091ad129be6daab0122c21ab97824fb92/clipkit-2.12.0-py3-none-any.whl
ARG CLIPKIT_WHEEL_SHA256=41bbc7637f34faaeb6d564496bdd41ccd7ce3465219c6b7a4291524520edd4de
ARG CLIPKIT_SDIST_URL=https://files.pythonhosted.org/packages/6e/7c/9b94457d9adcbda2227b75b094a12a0d28c02291d6d76264ddd0a7f70dcf/clipkit-2.12.0.tar.gz
ARG CLIPKIT_SDIST_SHA256=e6fa1aa08bff0bf3962c38622ac3193dc9fd7c7adb4341058b34288e97c9ce80
ARG CLIPKIT_ECOMP_URL=https://raw.githubusercontent.com/JLSteenwyk/ClipKIT/v2.12.0/test.ecomp
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
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONNOUSERSITE=1
ENV PIP_NO_CACHE_DIR=1
ENV LD_LIBRARY_PATH=/opt/clipkit/venv/lib/python3.11/site-packages/numpy.libs

RUN set -eux; \
    for attempt in 1 2 3; do \
      if apt-get -o Acquire::Retries=3 update \
       && apt-get -o Acquire::Retries=3 install -y --no-install-recommends \
            ca-certificates \
            curl \
            tar; then \
        break; \
      fi; \
      if [ "$attempt" = "3" ]; then exit 1; fi; \
      apt-get clean; \
      rm -rf /var/lib/apt/lists/*; \
      sleep 5; \
    done; \
    rm -rf /var/lib/apt/lists/*

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
    curl -fsSL -o "/tmp/wheels/clipkit-${CLIPKIT_VERSION}-py3-none-any.whl" "${CLIPKIT_WHEEL_URL}"; \
    echo "${CLIPKIT_WHEEL_SHA256}  /tmp/wheels/clipkit-${CLIPKIT_VERSION}-py3-none-any.whl" | sha256sum -c -; \
    curl -fsSL -o clipkit.tar.gz "${CLIPKIT_SDIST_URL}"; \
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
    curl -fsSL -o /opt/clipkit/share/doc/clipkit/test.ecomp "${CLIPKIT_ECOMP_URL}"; \
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
    python -c 'import Bio, clipkit, numpy, zstandard; from clipkit.version import __version__; assert __version__ == "2.12.0"'; \
    find /opt/clipkit/venv -type f -name '*.so' -print0 | xargs -0 -r ldd > /tmp/clipkit-ldd.txt; \
    if grep -F "not found" /tmp/clipkit-ldd.txt; then exit 1; fi

FROM python:3.11-slim-bookworm

ARG CLIPKIT_VERSION
ARG CLIPKIT_COMMIT
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONNOUSERSITE=1
ENV LD_LIBRARY_PATH=/opt/clipkit/venv/lib/python3.11/site-packages/numpy.libs

RUN set -eux; \
    for attempt in 1 2 3; do \
      if apt-get -o Acquire::Retries=3 update \
       && apt-get -o Acquire::Retries=3 install -y --no-install-recommends \
            bash \
            ca-certificates \
            gzip; then \
        break; \
      fi; \
      if [ "$attempt" = "3" ]; then exit 1; fi; \
      apt-get clean; \
      rm -rf /var/lib/apt/lists/*; \
      sleep 5; \
    done; \
    rm -rf /var/lib/apt/lists/*

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
    python -c 'import Bio, clipkit, numpy, zstandard; from clipkit.version import __version__; assert __version__ == "2.12.0"'; \
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
