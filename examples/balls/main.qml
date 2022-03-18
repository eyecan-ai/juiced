import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls

// Root Window Item
Window {
    id: appWindow
    title: "Balls"
    height: scene.height
    width: scene.width
    visible: true


    Rectangle{
        id: sphere
        x: scene.sphere.x
        y: scene.sphere.y
        width: scene.sphere.radius * 2
        height: scene.sphere.radius * 2
        radius: scene.sphere.radius
        color: "#ff0000"

        MouseArea {
            anchors.fill: parent
            drag.target: parent
            onPressed: {
                scene.pause = true
                scene.sphere.vx = 0
                scene.sphere.vy = 0
            }
            onReleased: { scene.pause = false }
            // onPositionChanged: { console.log("ciao") }
            onClicked: { parent.color = 'green' }
        }

        Binding {
            target: scene.sphere
            property: "x"
            value: sphere.x
            delayed: true
        }
        Binding {
            target: scene.sphere
            property: "y"
            value: sphere.y
            delayed: true
        }

    }
}