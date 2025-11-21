import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class KeyManager:
    """
    Deterministic key derivation from a root seed using SHA-256.
    The function is purely functional and side-effect free.
    """

    seed: str

    def derive_key(self, name: str) -> str:
        payload = f"{self.seed}:{name}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
