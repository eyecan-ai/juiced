import sys
import time
from pathlib import Path
from threading import Thread
from typing import Optional

from PySide6.QtCore import Property, QObject, QUrl, Signal
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication


# Shared objects must all derive from QObject
class MyClass(QObject):

    # Signal emitted every time the variable "foo" is changed.
    fooChanged = Signal()

    # Constructor, pretty standard, except for the "parent" kwarg.
    def __init__(self, foo: int, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._foo = foo

    # This is a special getter property for the "_foo" attribute.
    # Every time the signal passed to the "notify" argument is emitted, QML will
    # automatically update all properties binded to this value
    #
    # This property can be used from python transparently, just like any other
    # standard python properties (@property)
    @Property(int, notify=fooChanged)
    def foo(self) -> int:
        return self._foo

    # Setter part of the "foo" property
    @foo.setter
    def foo(self, value: int) -> None:

        # Very important: avoid setting when not necessary.
        # This also breaks potential binding loops explicitly,
        # instead of relying on Qt loop detection.
        if value != self._foo:

            # This is just a print for the sake of this example.
            print(f"python: Setting my_object.foo to {value}")

            # Update the attribute value
            self._foo = value

            # Emit the "fooChanged" signal.
            self.fooChanged.emit()


def gui() -> None:
    # Create app, engine and context
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    # This is a python object that both python and qml can see.
    # See MyClass (above) for more info
    my_object = MyClass(18)

    # Make "my_object" accessible from qml under the name "myObject"
    context.setContextProperty("myObject", my_object)

    # This is just an example to prove that the python->qml binding is working:
    # a python thread increments the value of my_object.foo every second, the GUI
    # should update automagically.
    def add_one_every_second():
        while True:
            time.sleep(1)
            my_object.foo = (my_object.foo + 1) % 100

    # Start the thread setting daemon=True to make it exit as the main thread exits.
    Thread(target=add_one_every_second, daemon=True).start()

    # Start the app
    this_folder = Path(__file__).parent
    engine.load(QUrl(str(this_folder / "main.qml")))
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


if __name__ == "__main__":
    gui()
