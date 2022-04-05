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

    // Property containing the selected sample index
    // Can be browsed with:
    // - A: previous
    // - D: next
    property var selected: 0

    // Window content
    RowLayout {
        anchors.fill: parent
        SampleViewer {
            id: viewer
            Layout.fillHeight: true
            Layout.preferredWidth: (appWindow.height + appWindow.width) / 2
            sample: scene.dataset.samples[appWindow.selected]
            enableDrag: true
        }
        LabelingView {
            id: labeling
            Layout.fillWidth: true
            Layout.fillHeight: true
            sample: scene.dataset.samples[appWindow.selected]
            criteria: scene.dataset.criteria
            enableEdit: true
        }
    }
    
    // Decorator that temporarely disables two-way bindings to avoid side-effects
    function withNoBindings(fn) {
        var prevEnableDrag = viewer.enableDrag
        var prevEnableEdit = labeling.enableEdit
        
        viewer.enableDrag = false
        labeling.enableEdit = false

        fn()

        viewer.enableDrag = prevEnableDrag
        labeling.enableEdit = prevEnableEdit
    }

    // Global keyboard shortcuts
    Shortcut {
        sequence: "A"
        function decrement() {
            appWindow.selected = appWindow.selected > 0 ? (appWindow.selected - 1) : scene.dataset.samples.length - 1
        }
        onActivated: { appWindow.withNoBindings(decrement) }
    }
    Shortcut {
        sequence: "D"
        function increment() {
            appWindow.selected = (appWindow.selected + 1) % scene.dataset.samples.length
        }
        onActivated: { appWindow.withNoBindings(increment) }
    }
    Shortcut {
        sequence: "Q"
        onActivated: { appWindow.close() }
    }
}