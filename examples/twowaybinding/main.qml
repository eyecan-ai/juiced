import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls

// Root Window Item
Window {
    id: appWindow
    title: "Two Way Binding"
    height: 50
    width: 300
    visible: true

    ColumnLayout {
        Text {
            // Text item with one Way binding: Python -> Qml
            // The "text" property is automatically updated whenever "myObject.foo"
            // is notified, i.e. when MyClass.fooChanged is emitted.
            text: myObject.foo 
        }
        Slider {
            // Slider item with two way binding: Python <-> Qml

            id: slider
            from: 0
            to: 100
            stepSize: 1.0
            
            // First part of the double binding: Python -> Qml
            // This is exactly like the previous "Text" item, it ensures that
            // the cursor position is always set to the value of "myObject.foo", 
            // so that if anything modifies it in the python side, it is also
            // modified here.
            value: myObject.foo

            // Second part of the double binding: Qml -> Python
            // This ensures that the value of "myObject.foo" is always equal to 
            // The slider cursor position. So if the user interacts with the cursor,
            // the value fo "myObject.foo" is automatically modified.
            Binding {
                target: myObject
                property: "foo"
                value: slider.value
            }

            // This is just a print for the sake of this example.
            onValueChanged: { 
                console.log("Setting my_object.foo to "+value)
            }
        }
    }
}