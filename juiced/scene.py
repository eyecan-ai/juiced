from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import pipelime
import pipelime.sequences.samples as plsamples
import pydash as py_
from pipelime.sequences.streams.underfolder import UnderfolderStream
from PySide6.QtCore import Property, QObject, Signal

from image_provider import PipelimeImageProvider


class OrientedBBox(QObject):
    """A generic shape that can be moved/resized/rotated on a 2D plane"""

    xChanged = Signal()
    yChanged = Signal()
    wChanged = Signal()
    hChanged = Signal()
    angleChanged = Signal()

    dataChanged = Signal()

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
            self.dataChanged.emit()

    @Property(float, notify=yChanged)
    def y(self) -> float:
        return self._shape["y"]

    @y.setter
    def y(self, value: float) -> None:
        if value != self.y:
            self._shape["y"] = value
            self.yChanged.emit()
            self.dataChanged.emit()

    @Property(float, notify=wChanged)
    def w(self) -> float:
        return self._shape["w"]

    @w.setter
    def w(self, value: float) -> None:
        if value != self.w:
            self._shape["w"] = value
            self.wChanged.emit()
            self.dataChanged.emit()

    @Property(float, notify=hChanged)
    def h(self) -> float:
        return self._shape["h"]

    @h.setter
    def h(self, value: float) -> None:
        if value != self.h:
            self._shape["h"] = value
            self.hChanged.emit()
            self.dataChanged.emit()

    @Property(float, notify=angleChanged)
    def angle(self) -> float:
        return self._shape["a"]

    @angle.setter
    def angle(self, value: float) -> None:
        if value != self.angle:
            self._shape["a"] = value
            self.angleChanged.emit()
            self.dataChanged.emit()


class Sample(QObject):
    """A sample with an image, a region and labels"""

    itemChanged = Signal(int, str)

    def __init__(
        self, sample: plsamples.Sample, parent: Optional[QObject] = None
    ) -> None:
        super().__init__(parent)
        image_k = "image"  # TODO Toy logic
        labels_k = "metadata.labels"  # TODO Toy logic
        shape_k = "metadata.shape"  # TODO Toy logic
        dname = parent.name

        self._idx = sample.id
        self._image = f"image://pipelime/{dname}/{sample.id}/{image_k}"
        self._labels = py_.get(sample, labels_k)

        shape = py_.get(sample, shape_k)
        if shape["type"] == "box":
            self._shape = OrientedBBox(shape, parent=self)
        else:
            raise NotImplementedError("I'm too lazy to implement this")

        self._shape.dataChanged.connect(self.onShapeChanged)

    def onShapeChanged(self):
        self.itemChanged.emit(self._idx, "metadata")

    def onLabelsChanged(self):
        self.itemChanged.emit(self._idx, "metadata")

    @Property(str, constant=True)
    def image(self) -> str:
        return self._image

    @Property("QVariant", constant=True)
    def labels(self) -> Dict[str, Any]:
        return self._labels

    @Property("QVariant", constant=True)
    def shape(self) -> Dict[str, Any]:
        return self._shape


class Criterion(QObject):
    def __init__(
        self, name: str, data: Dict[str, Any], parent: Optional[QObject] = None
    ) -> None:
        super().__init__(parent)
        self._name = name
        self._data = data

    @Property(str, constant=True)
    def name(self) -> str:
        return self._name

    @Property("QVariant", constant=True)
    def data(self) -> Dict[str, Any]:
        return self._data


class Dataset(QObject):
    """A sequence of samples with a name"""

    def __init__(
        self, stream: UnderfolderStream, name: str, parent: Optional[QObject] = None
    ) -> None:
        super().__init__(parent)
        self._stream = stream
        self._name = name
        self._samples = [
            Sample(stream.get_sample(i), parent=self) for i in range(len(stream))
        ]

        criteria_k = "criteria"  # TODO: toy logic
        criteria = py_.get(stream.get_sample(0), criteria_k)
        criteria = sorted(list(criteria.items()), key=lambda x: x[0])
        self._criteria = [Criterion(name, data) for name, data in criteria]

        for x in self._samples:
            x.itemChanged.connect(self.onItemChanged)

    def onItemChanged(self, idx: int, name: str) -> None:
        data, _ = self._stream.get_data(idx, name, "dict")
        self._stream.set_data(idx, name, data, "dict")

    @Property("QVariantList", constant=True)
    def samples(self) -> List[Sample]:
        return self._samples

    @Property(str, constant=True)
    def name(self) -> str:
        return self._name

    @Property("QVariantList", constant=True)
    def criteria(self) -> List[Criterion]:
        return self._criteria


class Scene(QObject):
    """Root scene object"""

    def __init__(self, dataset: Path, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        dataset_name = "dataset"
        stream = UnderfolderStream(dataset)
        PipelimeImageProvider.get_instance().add_dataset(stream.reader, dataset_name)
        self._dataset = Dataset(stream, dataset_name)

    @Property(Dataset, constant=True)
    def dataset(self) -> Dataset:
        return self._dataset

    @Property(str, constant=True)
    def version(self) -> str:
        return f"Pipelime v{pipelime.__version__}"
