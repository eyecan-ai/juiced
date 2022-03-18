from __future__ import annotations

from typing import Any, Dict, List, Optional

import pipelime
import pydash as py_
from pipelime.sequences.samples import Sample, SamplesSequence
from PySide6.QtCore import Property, QObject, Signal

from image_provider import PipelimeImageProvider


class OrientedBBox(QObject):
    """A generic shape that can be moved/resized/rotated on a 2D plane"""

    xChanged = Signal()
    yChanged = Signal()
    wChanged = Signal()
    hChanged = Signal()
    angleChanged = Signal()

    def __init__(self, shape: Dict[str, Any], parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._shape = shape

    @Property(float, notify=xChanged)
    def x(self) -> float:
        return self._shape["x"]

    @x.setter
    def x(self, value: float) -> None:
        if value != self.x:
            self._shape["x"] = value
            self.xChanged.emit()

    @Property(float, notify=yChanged)
    def y(self) -> float:
        return self._shape["y"]

    @y.setter
    def y(self, value: float) -> None:
        if value != self.y:
            self._shape["y"] = value
            self.yChanged.emit()

    @Property(float, notify=wChanged)
    def w(self) -> float:
        return self._shape["w"]

    @w.setter
    def w(self, value: float) -> None:
        if value != self.w:
            self._shape["w"] = value
            self.wChanged.emit()

    @Property(float, notify=hChanged)
    def h(self) -> float:
        return self._shape["h"]

    @h.setter
    def h(self, value: float) -> None:
        if value != self.h:
            self._shape["h"] = value
            self.hChanged.emit()

    @Property(float, notify=angleChanged)
    def angle(self) -> float:
        return self._shape["a"]

    @angle.setter
    def angle(self, value: float) -> None:
        if value != self.angle:
            self._shape["a"] = value
            self.angleChanged.emit()


class Region(QObject):
    """A region consisting of a shape and a dictionary of labels."""

    def __init__(
        self,
        labels: Dict[str, Any],
        shape: Dict[str, Any],
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._labels = labels

        if shape["type"] == "box":
            self._shape = OrientedBBox(shape, parent=self)
        else:
            raise NotImplementedError("I'm too lazy to implement this")

    @Property("QVariant", constant=True)
    def labels(self) -> Dict[str, Any]:
        return self._labels

    @Property("QVariant", constant=True)
    def shape(self) -> Dict[str, Any]:
        return self._shape


class Sample(QObject):
    """A sample with an image and a list of regions"""

    def __init__(self, sample: Sample, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        id_ = str(int(sample.id))  # BUG: id vs idx bug -> see pipelime 1.0 refactoring
        image_k = ["image"]  # Toy logic
        region_k = "metadata.regions"  # Toy logic
        dname = parent.name

        self._images = [f"image://pipelime/{dname}/{id_}/{x}" for x in image_k]
        self._regions = [
            Region(x["labels"], x["shape"], parent=self)
            for x in py_.get(sample, region_k)
        ]

    @Property("QVariantList", constant=True)
    def images(self) -> List[str]:
        return self._images

    @Property("QVariantList", constant=True)
    def regions(self) -> List[Region]:
        return self._regions


class Dataset(QObject):
    """A sequence of samples with a name"""

    def __init__(
        self, sseq: SamplesSequence, name: str, parent: Optional[QObject] = None
    ) -> None:
        super().__init__(parent)
        self._name = name
        self._samples = [Sample(x, parent=self) for x in sseq]

    @Property("QVariantList", constant=True)
    def samples(self) -> List[Sample]:
        return self._samples

    @Property(str, constant=True)
    def name(self) -> str:
        return self._name


class Scene(QObject):
    """Root scene object"""

    def __init__(self, sseq: SamplesSequence, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        dataset_name = "dataset"
        PipelimeImageProvider.get_instance().add_dataset(sseq, dataset_name)
        self._dataset = Dataset(sseq, dataset_name)

    @Property(Dataset, constant=True)
    def dataset(self) -> Dataset:
        return self._dataset

    @Property(str, constant=True)
    def version(self) -> str:
        return f"Pipelime v{pipelime.__version__}"
