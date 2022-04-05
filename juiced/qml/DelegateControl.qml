import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

// A labeling delegate that can accept any control
RowLayout { 
    id: root

    // Set height to computed height
    height: content.height

    // Use all available width
    width: parent.width
    
    // The name of this delegate
    property var entryName

    // Assign any control to this property
    property alias content: loader.sourceComponent

    Text { 
        text: root.entryName 
        Layout.preferredWidth: 100
    }
    Loader { 
        id: loader 
        Layout.alignment: Qt.AlignRight
        Layout.fillWidth: true
    }

}