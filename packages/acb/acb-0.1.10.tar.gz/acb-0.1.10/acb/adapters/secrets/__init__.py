from acb.config import load_adapter
from acb.config import Settings


class SecretsBaseSettings(Settings):
    ...


secrets = load_adapter("secrets")
