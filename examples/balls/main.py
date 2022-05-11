import sys
import time
from pathlib import Path
from threading import Thread
from typing import Optional

from PySide6.QtCore import Property, QObject, QUrl, Signal
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication


class Sphere(QObject):
    GRAVITY = 0.1
    DRAG = 0.995

    xChanged = Signal()
    yChanged = Signal()
    vxChanged = Signal()
    vyChanged = Signal()

    def __init__(
        self, x: float, y: float, radius: float, parent: Optional[QObject] = ...
    ) -> None:
        super().__init__(parent)
        self._x = x
        self._y = y
        self._radius = radius
        self._vx = 0
        self._vy = 0

    @Property(float, constant=True)
    def radius(self):
        return self._radius

    @Property(int, notify=xChanged)
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if value != self._x:
            self._x = value
            self.xChanged.emit()

    @Property(float, notify=vxChanged)
    def vx(self) -> float:
        return self._vx

    @vx.setter
    def vx(self, value: float) -> None:
        if value != self._vx:
            self._vx = value
            self.vxChanged.emit()

    @Property(int, notify=yChanged)
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if value != self._y:
            self._y = value
            self.yChanged.emit()

    @Property(float, notify=vyChanged)
    def vy(self) -> float:
        return self._vy

    @vy.setter
    def vy(self, value: float) -> None:
        if value != self._vy:
            self._vy = value
            self.vyChanged.emit()

    def update(self):
        self.vx = self.vx * Sphere.DRAG
        self.vy = (self.vy + Sphere.GRAVITY) * Sphere.DRAG
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)


class Scene(QObject):
    pauseChanged = Signal()

    # Constructor, pretty standard, except for the "parent" kwarg.
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._width = 500
        self._height = 500
        self._sphere = Sphere(250, 250, 25, parent=self)
        self._pause = False

    @Property(bool, notify=pauseChanged)
    def pause(self) -> bool:
        return self._pause

    @pause.setter
    def pause(self, value: bool) -> None:
        if value != self._pause:
            self._pause = value
            self.pauseChanged.emit()

    @Property(Sphere, constant=True)
    def sphere(self) -> int:
        return self._sphere

    @Property(int, constant=True)
    def width(self) -> int:
        return self._width

    @Property(int, constant=True)
    def height(self) -> int:
        return self._height

    def update(self):
        if not self.pause:
            self._sphere.update()
            if self._sphere.x < 0:
                self._sphere.vx = -self._sphere.vx
                self._sphere.x = 0

            elif self._sphere.x + self._sphere.radius * 2 > self._width:
                self._sphere.vx = -self._sphere.vx
                self._sphere.x = int(self._width - self._sphere.radius * 2)

            elif self._sphere.y < 0:
                self._sphere.vy = -self._sphere.vy
                self._sphere.y = 0

            elif self._sphere.y + self._sphere.radius * 2 > self._height:
                self._sphere.vy = -self._sphere.vy
                self._sphere.y = int(self._height - self._sphere.radius * 2)


def gui() -> None:
    # Create app, engine and context
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    # This is a python object that both python and qml can see.
    # See MyClass (above) for more info
    scene = Scene()

    # Make "my_object" accessible from qml under the name "myObject"
    context.setContextProperty("scene", scene)

    def gravity():
        while True:
            time.sleep(0.01)
            scene.update()

    # Start the thread setting daemon=True to make it exit as the main thread exits.
    Thread(target=gravity, daemon=True).start()

    # Start the app
    this_folder = Path(__file__).parent
    engine.load(QUrl.fromLocalFile(str(this_folder / "main.qml")))
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


if __name__ == "__main__":
    gui()
