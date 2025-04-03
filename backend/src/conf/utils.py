import os


def load_bool(name, default):
    env_value = os.getenv(name, str(default)).lower()
    return env_value in ("true", "yes", "1", "y", "t")
