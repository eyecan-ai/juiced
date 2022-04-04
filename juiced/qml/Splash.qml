import QtQuick
import QtQuick.Window

// Splash Screen shown when the App starts
Window {
    id: splash

    // Signal emitted when the splash timer times out
    signal timeout

    // Splash duration in mulliseconds
    property int timeoutInterval: 200

    // Make splash screen modal
    visible: true 
    modality: Qt.ApplicationModal
    flags: Qt.SplashScreen

    // Timer object that emits a single timeout signal after running once.
    Timer {
        interval: timeoutInterval; running: true; repeat: false
        onTriggered: {
            visible = false
            splash.timeout()
        }
    }
}