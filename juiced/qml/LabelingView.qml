import QtQuick
import QtQuick.Controls
import Qt.labs.qmlmodels

// Dynamically loaded labeling controls
Item {
    
    // The sample to label
    property var sample

    // The labeling criteria
    property var criteria

    // Enable/Disable edit mode
    property var enableEdit: false

    // The container for all the labeling controls
    ListView {
        anchors.fill: parent
        model: parent.criteria
        delegate: chooser
        spacing: 10
    }

    // Dynamically load delegates based on a specific model role (eg. "type")
    DelegateChooser {
        id: chooser

        // Choose delegate based on "type"
        role: "type"

        // Choice between a set of predefined classes
        DelegateChoice { 
            
            // When model.type == "choice"
            roleValue: "choice" 

            DelegateControl {
                entryName: modelData.name
                content: ComboBox {
                    id: comboBox
                    model: modelData.data.choices 

                    // Python -> QML
                    currentIndex: model.indexOf(sample.labels[modelData.name])

                    // QML -> Python
                    // Cannot use Binding, must use a signal handler
                    onCurrentValueChanged: {
                        if (enableEdit) {
                            sample.setLabel(modelData.name, comboBox.currentValue)
                        }
                    }
                }
            }
        }

        // Binary classification
        DelegateChoice { 

            // When model.type == "bool"
            roleValue: "bool"

            DelegateControl {
                entryName: modelData.name 
                content: Switch {
                    id: switch_

                    // Python -> QML
                    Binding {
                        target: switch_
                        property: "checked"
                        value: sample.labels[modelData.name]
                        delayed: true
                        restoreMode: Binding.RestoreNone
                    }

                    // QML -> Python
                    // Cannot use Binding, must use a signal handler
                    onCheckedChanged: {
                        if (enableEdit) {
                            sample.setLabel(modelData.name, switch_.checked)
                        }
                    }
                }
            } 
        }
    }
}