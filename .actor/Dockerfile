FROM apify/actor-python:3.13

COPY --from=ghcr.io/astral-sh/uv:0.6.17 /uv /uvx /bin/

# Configure git to use the provided GitHub token for private repositories
ARG APIFY_COMMON_REPO_TOKEN

# Install git to clone private repositories
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Configure git to use the provided GitHub token for private repositories
RUN git config --global url."https://${APIFY_COMMON_REPO_TOKEN}:@github.com/".insteadOf "https://github.com/"

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --no-dev --locked

# Create and run as a non-root user.
RUN useradd --create-home apify && \
    chown -R apify:apify ./
USER apify

CMD ["uv", "run", "--no-dev", "python3", "-m", "src"]
