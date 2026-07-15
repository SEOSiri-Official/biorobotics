# Use a lightweight, standard Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency configuration and README first to leverage Docker caching
COPY pyproject.toml README.md ./

# Copy the source code
COPY src/ ./src/

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# Define the entrypoint to run the standard stdio server directly
ENTRYPOINT ["python", "src/main_mcp_server.py"]