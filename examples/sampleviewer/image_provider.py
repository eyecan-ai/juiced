from __future__ import annotations

from traceback import print_exc
from typing import Any

import numpy as np
from pipelime.sequences.samples import SamplesSequence
from PySide6.QtCore import QSize
from PySide6.QtGui import QImage
from PySide6.QtQml import QQmlImageProviderBase
from PySide6.QtQuick import QQuickImageProvider


class PipelimeImageProvider(QQuickImageProvider):
    """QQuickImageProvider implementation for generic pipelime datasets.

    This class is a singleton that is capable of handling multiple pipelime datasets.

    To get the instance use the classmethod `get_instance`::

        provider = PipelimeImageProvider.get_instance()

    Before starting using this provider, you need to register it to the application
    engine, specifying a name for it. Example::

        engine = QQmlApplicationEngine()
        engine.addImageProvider("pipelime", provider)

    Datasets can be added by calling the `add_dataset` method, registering them with
    a given string identifier::

        dataset = UnderfolderReader(...)
        provider.add_dataset(dataset, "my_underfolder")

    To request pipelime images from qml, you need to use the following url::

        image://PROVIDER_NAME/DATASET_NAME/SAMPLE_INDEX/ITEM_NAME

    where:

        - `PROVIDER_NAME` is the name associated with this pipelime image provider when
        it was registered to the application engine.

        - `DATASET_NAME` is the name of the dataset from which to get the image, must be
        a dataset which was previously registered with `add_dataset`

        - `SAMPLE_INDEX` is the index of the sample containing the item to display

        - `ITEM_NAME` is the name of the image item to display

    """

    _instance: PipelimeImageProvider = None

    @classmethod
    def get_instance(cls) -> PipelimeImageProvider:
        if cls._instance is None:
            cls._instance = PipelimeImageProvider()
        return cls._instance

    def __init__(self) -> None:
        super().__init__(QQmlImageProviderBase.ImageType.Image)
        self._datasets = {}

    def add_dataset(self, dataset: SamplesSequence, id_: str) -> None:
        self._datasets[id_] = dataset

    def _sanitize_item(self, item: Any) -> np.ndarray:
        array: np.ndarray = item
        if len(array.shape) == 2:
            array = np.expand_dims(array, -1)
        if array.shape[2] == 1:
            array = np.stack([array[:, :, 0]] * 3, -1)
        if array.dtype == np.float32:
            array = (array - array.min()) / (array.max() - array.min()) * 255
        array = array.astype(np.uint8)
        return array

    def _to_qimage(self, array: np.ndarray) -> QImage:
        height, width = array.shape[:2]
        format_ = QImage.Format_ARGB32
        array = array.astype(np.uint32)
        r, g, b = [array[:, :, i] for i in range(3)]
        data = (255 << 24 | r << 16 | g << 8 | b).flatten()
        return QImage(data, width, height, format_)

    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        dataset, idx, key = id.split("/", maxsplit=3)
        try:
            item = self._datasets[dataset][int(idx)][key]
            array = self._sanitize_item(item)
        except:
            array = np.zeros((256, 256, 3), dtype=np.uint8)
            print_exc()
        qimg = self._to_qimage(array)
        return qimg
