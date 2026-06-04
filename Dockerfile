# Use a lightweight Python base
FROM python:3.11-slim

# Hugging Face Spaces require a non-root user to run the app
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements and install them securely
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY --chown=user . .

# Expose the exact port Hugging Face expects
EXPOSE 7860

# Run Chainlit on 0.0.0.0 so the outside world can connect to it
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860", "-h"]