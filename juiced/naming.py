from dataclasses import dataclass


@dataclass(frozen=True)
class Naming:
    image: str = "image"
    criteria: str = "criteria"
    shape: str = "metadata.shape"
    labels: str = "metadata.labels"
