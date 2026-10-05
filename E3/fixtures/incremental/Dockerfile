FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       build-essential ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/E3/fixtures/incremental
COPY . /workspace/
RUN make clean && make -j2

CMD ["./bin/demo", "--version"]
