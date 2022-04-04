import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

// Generic item that can be zoomed with Ctrl+Wheel and dragged.
Item {
    id: root

    // Clip stuff outside of bounds
    clip: true

    // Acquire the focus when the mouse area contains the mouse
    focus: mouseArea.containsMouse

    // Assign anything to this property to make it zoomable/draggable
    property alias content: loader.sourceComponent

    // Mouse area that handles the zooming / dragging
    MouseArea{
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true

        // Dragging behavior
        drag.target: loader

        // Zooming behavior
        onWheel: (wheel)=>{
            if(wheel.modifiers & Qt.ControlModifier) {
                var datl = wheel.angleDelta.y / 120 / 10
                var speed = 1.1
                if (datl < 0)
                    speed = 1 / speed
                loader.x = mouseX + (loader.x - mouseX) * speed
                loader.y = mouseY + (loader.y - mouseY) * speed
                loader.width = loader.width * speed
                loader.height = loader.height * speed
            }
        }
    }
    
    // Loader used to dynamically load the content
    Loader { id: loader }
}