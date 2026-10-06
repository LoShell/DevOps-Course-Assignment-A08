FROM ubuntu:24.04
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY . /workspace/
WORKDIR /workspace/E3/fixtures/md-rd
RUN make clean && make -j2
CMD ["./bin/demo", "--version"]
