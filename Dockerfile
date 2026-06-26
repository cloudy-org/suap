# docker buildx build -t devgoldy/suap:latest .

FROM python:3.13.14-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.11.23 /uv /uvx /bin/

USER root
WORKDIR /app

# install all compilers and toolchains we'll need for all project types
RUN apt-get update && apt-get install -y --no-install-recommends \
    rustup \
    build-essential \
    nsis \
    gcc-mingw-w64-x86-64 \
    binutils-mingw-w64

RUN dpkg --add-architecture arm64

RUN apt-get install -y --no-install-recommends \
    libc6-dev-arm64-cross \
    gcc-aarch64-linux-gnu

# thank FUCK Debain stated including "rustup" in the apt repos in debain 13 🙏

RUN rustup toolchain install 1.89 --profile minimal \
    && rustup target add x86_64-unknown-linux-gnu \
    && rustup target add aarch64-unknown-linux-gnu \
    && rustup target add x86_64-pc-windows-gnu \
    && rustup default 1.89

COPY /suap ./suap
COPY pyproject.toml .

ENV UV_NO_DEV=1

COPY uv.lock .
RUN uv sync --locked

ENV SUAP_DOCKER=true

ENTRYPOINT ["uv", "run", "suap"]