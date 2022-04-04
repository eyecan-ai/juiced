import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: root

    property var sample
    property var criteria

    ListView {
        anchors.fill: parent
        model: root.criteria
        delegate: Text {
            text: modelData.name
        }
    }
}