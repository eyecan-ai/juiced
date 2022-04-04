import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls

// Main window
Window {
    id: appWindow

    // Pick some properties from the configuration
    width: config.appWindow.width
    height: config.appWindow.height
    title: qsTr(config.appWindow.title)

    // Set the window to invisible until the splash screen has finished
    visible: false

    // Splash screen
    property var splashWindow: Splash {
        id: splash

        // Pick some properties from the configuration
        width: config.splashWindow.width
        height: config.splashWindow.height
        timeoutInterval: config.splashWindow.timeMillis
        color: config.splashWindow.color

        // Add an image with a text displaying the pipelime version 
        // On the bottom-right corner
        Image {
            id: image
            width: splash.width
            height: splash.height
            fillMode: Image.PreserveAspectFit
            source: "../images/eyecan_logo_downscaled.png"
            Text {
                text: scene.version
                color: config.eyecanColor
                x: parent.width - 10 - width
                y: parent.height - 10 - height
                font.pixelSize: 20
            }
        }

        // Close the splash and make the real window visislbe
        onTimeout: {
            appWindow.visible = true
            close()
        }
    }

    // Window content
    SampleViewer {
        anchors.fill: parent
    }
}