from __future__ import annotations

from math import pi
from pathlib import Path
from typing import Any, Dict, List, Optional

import pipelime
import pipelime.sequences.samples as plsamples
import pydash as py_
from pipelime.sequences.streams.underfolder import UnderfolderStream
from PySide6.QtCore import Property, QObject, Signal, Slot

from image_provider import PipelimeImageProvider
from juiced.criterion import Criterion, CriterionProxy
from juiced.naming import Naming


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
        return self._shape["angle"]

    @angle.setter
    def angle(self, value: float) -> None:
        if value != self.angle:
            self._shape["angle"] = value
            self.angleChanged.emit()
            self.dataChanged.emit()


class Sample(QObject):
    """A sample with an image, a region and labels"""

    itemChanged = Signal(int, str, str)
    labelsChanged = Signal()

    def __init__(self, sample: plsamples.Sample, parent: Dataset) -> None:
        super().__init__(parent)
        dname = parent.name
        naming = parent.naming
        self._naming = naming

        self._idx = sample.id
        self._image = f"image://pipelime/{dname}/{sample.id}/{naming.image}"
        self._labels = py_.get(sample, naming.labels)

        shape = py_.get(sample, naming.shape)
        if shape["type"] == "box":
            self._shape = OrientedBBox(shape, parent=self)
        else:
            raise NotImplementedError("I'm too lazy to implement this")

        self._shape.dataChanged.connect(self.onShapeChanged)
        self.labelsChanged.connect(self.onLabelsChanged)

    def onShapeChanged(self):
        self.itemChanged.emit(self._idx, self._naming.shape.split(".")[0], "dict")

    def onLabelsChanged(self):
        self.itemChanged.emit(self._idx, self._naming.labels.split(".")[0], "dict")

    @Property(str, constant=True)
    def image(self) -> str:
        return self._image

    @Property("QVariant", notify=labelsChanged)
    def labels(self) -> Dict[str, Any]:
        return self._labels

    @Slot(str, "QVariant")
    def setLabel(self, name: str, value: Any) -> None:
        if self._labels.get(name) != value:
            self._labels[name] = value
            self.labelsChanged.emit()

    @Property(OrientedBBox, constant=True)
    def shape(self) -> OrientedBBox:
        return self._shape


class Dataset(QObject):
    """A sequence of samples with a name"""

    def __init__(
        self,
        stream: UnderfolderStream,
        name: str,
        naming: Naming,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._stream = stream
        self._name = name
        self._naming = naming
        self._samples = [Sample(stream.get_sample(i), self) for i in range(len(stream))]

        criteria = py_.get(stream.get_sample(0), self._naming.criteria)
        self._criteria = [CriterionProxy(Criterion.parse_obj(x)) for x in criteria]

        for x in self._samples:
            x.itemChanged.connect(self.onItemChanged)
            for c in self._criteria:
                if c.name not in x.labels:
                    x.setLabel(c.name, c.default)

    @property
    def naming(self) -> Naming:
        return self._naming

    def onItemChanged(self, idx: int, name: str, format: str) -> None:
        """When an item is changed, automatically stream it to filesystem"""

        data, _ = self._stream.get_data(idx, name, format)
        self._stream.set_data(idx, name, data, format)

    @Property("QVariantList", constant=True)
    def samples(self) -> List[Sample]:
        return self._samples

    @Property(str, constant=True)
    def name(self) -> str:
        return self._name

    @Property("QVariantList", constant=True)
    def criteria(self) -> List[CriterionProxy]:
        return self._criteria


class Scene(QObject):
    """Root scene object"""

    def __init__(
        self,
        dataset: Path,
        naming: Optional[Naming] = None,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        if naming is None:
            naming = Naming()

        dataset_name = "dataset"
        stream = UnderfolderStream(dataset)
        PipelimeImageProvider.get_instance().add_dataset(stream.reader, dataset_name)
        self._dataset = Dataset(stream, dataset_name, naming)

    @Property(Dataset, constant=True)
    def dataset(self) -> Dataset:
        return self._dataset

    @Property(str, constant=True)
    def version(self) -> str:
        return f"Pipelime v{pipelime.__version__}"
