import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Shapes

// Panel Content
Item {
    id: root

    // Property binded to the selected sample
    property var sample

    // Enable/Disable dragging of regions shapes
    property var enableDrag: false

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
            source: root.sample.image
            fillMode: Image.PreserveAspectFit

            // Origin of the image RF
            property var paintedX: (width - paintedWidth) / 2
            property var paintedY: (height - paintedHeight) / 2

            Shape {
                id: viewShape
                property var shape: root.sample.shape

                // Transform: Image rf -> GUI rf
                x: shape.x * image.paintedWidth + image.paintedX
                y: shape.y * image.paintedHeight + image.paintedY
                width: shape.w * image.paintedWidth
                height: shape.h * image.paintedHeight
                rotation: shape.angle
                
                // Make a rectangle using a ShapePath
                // There is more than one way to do this. The one used here
                // Allows to draw any shape (not only rectangles) with some 
                // control over some details like fill/stroke styles. 
                ShapePath {
                    strokeWidth: 4
                    strokeColor: "white"
                    fillColor: "#4000206f"
                    strokeStyle: ShapePath.DashLine
                    dashPattern: [ 1, 3 ]
                    startX: 0; startY: 0
                    PathLine { x: 0; y: viewShape.height }
                    PathLine { x: viewShape.width; y: viewShape.height }
                    PathLine { x: viewShape.width; y: 0 }
                    PathLine { x: 0; y: 0 }
                }

                // Make the shapes draggable
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    drag.target: parent
                    enabled: root.enableDrag
                }

                // Two-way binding for x, and y. This just a tutorial example,
                // so I limited the GUI interation to the setting of x and y
                // properties.
                Binding {
                    target: viewShape.shape
                    property: "x"
                    value: (viewShape.x - image.paintedX) / image.paintedWidth
                    delayed: true
                    when: image.paintedWidth > 0 && root.enableDrag
                    restoreMode: Binding.RestoreNone
                }
                Binding {
                    target: viewShape.shape
                    property: "y"
                    value: (viewShape.y - image.paintedY) / image.paintedHeight
                    delayed: true
                    when: image.paintedHeight > 0 && root.enableDrag
                    restoreMode: Binding.RestoreNone
                }
            }
        }
    }
}