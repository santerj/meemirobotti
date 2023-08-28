FROM almalinux/9-minimal:9.2-20230718

# Install dependencies with microdnf + create nonroot user
RUN \
    microdnf update -y && \
    microdnf install -y python3.11-3.11.2 && \
    microdnf install -y shadow-utils-2:4.9 && \
    useradd -u 1001 -r -s /sbin/nologin -c "Default Application User" default && \
    microdnf remove -y shadow-utils && \
    microdnf clean all

# Install Python dependencies
COPY requirements.txt /tmp/

RUN \
    /usr/bin/python3.11 -m venv /app/venv && \
    /app/venv/bin/python -m pip install --no-cache-dir --upgrade pip -r /tmp/requirements.txt && \
    chown -R default:default /app/venv

# Copy sources
COPY --chown=default:default src/ /app/

WORKDIR /app
USER 1001
ENTRYPOINT [ "/app/venv/bin/python" ]
CMD [ "main.py" ]
