import sys
from pathlib import Path

import click
from choixe.configurations import XConfig
from pipelime.sequences.readers.filesystem import UnderfolderReader
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from image_provider import PipelimeImageProvider
from scene import Scene

this_folder = Path(__file__).parent


@click.command()
@click.option("-i", "--input_folder", type=Path, default=this_folder / "minimnist")
def gui(input_folder: Path) -> None:
    # Create app, engine and context
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Load an xconfig from "config.yml" as a plain dictionary
    config = XConfig(this_folder / "config.yml").to_dict()

    # Setup scene
    sseq = UnderfolderReader(input_folder)
    scene = Scene(sseq)

    # Make "config" and "scene" accessible from qml
    context = engine.rootContext()
    context.setContextProperty("config", config)
    context.setContextProperty("scene", scene)

    # This is crucial: to load custom images in qml, you need to add an "ImageProvider"
    # Here we choose to use a "PipelimeImageProvider" which loads images from pipelime
    # samples sequences.
    provider = PipelimeImageProvider.get_instance()
    engine.addImageProvider("pipelime", provider)

    # Start the app
    engine.load(QUrl.fromLocalFile(str(this_folder / "qml" / "main.qml")))
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


if __name__ == "__main__":
    gui()
