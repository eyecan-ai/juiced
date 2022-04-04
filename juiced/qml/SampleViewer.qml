import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Shapes

// Panel Content
Item {
    id: root

    // Property containing the selected sample index
    // Can be browsed with:
    // - A: previous
    // - D: next
    property var selected: 0
    Keys.onPressed: (event)=>{
        if (event.key == Qt.Key_A)
            selected = selected > 0 ? (selected - 1) : scene.dataset.samples.length - 1
        else if (event.key == Qt.Key_D) 
            selected = (selected + 1) % scene.dataset.samples.length
        event.accepted = true;
    }

    // Property binded to the selected sample
    property var sample: scene.dataset.samples[selected]
    
    // Make the content zoomable / draggable
    Zoomable {
        id: zoomable
        anchors.fill: parent
        
        // Anything assing to "content" is zoomable / draggable
        content: Image {
            id: image
            width: zoomable.width
            height: zoomable.height
            smooth: false
            antialiasing: false
            source: root.sample.images[0]
            fillMode: Image.PreserveAspectFit

            // Origin of the image RF
            property var paintedX: (width - paintedWidth) / 2
            property var paintedY: (height - paintedHeight) / 2

            // Repeater containing the dataset region boxes
            Repeater {
                id: repeater

                // Center in the painted region of the image (exluding padding)
                x: parent.paintedX
                y: parent.paintedY
                width: parent.paintedWidth
                height: parent.paintedHeight

                // Bind use the sample regions list as a model for the repeater
                model: root.sample.regions

                // For every element of the model instance a delegate Shape
                delegate: Shape {
                    id: shape

                    // Transform: Image rf -> GUI rf
                    x: modelData.shape.x * repeater.width + repeater.x
                    y: modelData.shape.y * repeater.height + repeater.y
                    width: modelData.shape.w * repeater.width
                    height: modelData.shape.h * repeater.height
                    rotation: modelData.shape.angle
                    
                    // Make a rectangle using a ShapePath
                    // There is more than one way to do this. The one used here
                    // Allows to draw any shape (not only rectangles) with some 
                    // control over some details like fill/stroke styles. 
                    ShapePath {
                        strokeWidth: 4
                        strokeColor: "white"
                        fillColor: "#8000206f"
                        strokeStyle: ShapePath.DashLine
                        dashPattern: [ 1, 3 ]
                        startX: 0; startY: 0
                        PathLine { x: 0; y: shape.height }
                        PathLine { x: shape.width; y: shape.height }
                        PathLine { x: shape.width; y: 0 }
                        PathLine { x: 0; y: 0 }
                    }

                    // Make the shapes draggable
                    MouseArea {
                        anchors.fill: parent
                        drag.target: parent
                    }

                    // Two-way binding for x, and y. This just a tutorial example,
                    // so I limited the GUI interation to the setting of x and y
                    // properties.
                    Binding {
                        target: modelData.shape
                        property: "x"
                        value: (shape.x - repeater.x) / repeater.width
                        delayed: true
                        when: repeater.width > 0
                    }
                    Binding {
                        target: modelData.shape
                        property: "y"
                        value: (shape.y - repeater.y) / repeater.height
                        delayed: true
                        when: repeater.width > 0
                    }
                }
            }
        }
    }
}