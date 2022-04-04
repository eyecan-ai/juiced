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
    property var enableDrag: false

    Keys.onPressed: (event)=>{
        var prev_state = root.enableDrag
        root.enableDrag = false
        if (event.key == Qt.Key_A)
            selected = selected > 0 ? (selected - 1) : scene.dataset.samples.length - 1
        else if (event.key == Qt.Key_D) 
            selected = (selected + 1) % scene.dataset.samples.length
        event.accepted = true;
        root.enableDrag = prev_state
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
            source: root.sample.image
            fillMode: Image.PreserveAspectFit

            // Origin of the image RF
            property var paintedX: (width - paintedWidth) / 2
            property var paintedY: (height - paintedHeight) / 2

            Shape {
                id: shape
                property var region: root.sample.region

                // Transform: Image rf -> GUI rf
                x: region.shape.x * image.paintedWidth + image.paintedX
                y: region.shape.y * image.paintedHeight + image.paintedY
                width: region.shape.w * image.paintedWidth
                height: region.shape.h * image.paintedHeight
                rotation: region.shape.angle
                
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
                    PathLine { x: 0; y: shape.height }
                    PathLine { x: shape.width; y: shape.height }
                    PathLine { x: shape.width; y: 0 }
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
                    target: shape.region.shape
                    property: "x"
                    value: (shape.x - image.paintedX) / image.paintedWidth
                    delayed: true
                    when: image.paintedWidth > 0 && root.enableDrag
                    restoreMode: Binding.RestoreNone
                }
                Binding {
                    target: shape.region.shape
                    property: "y"
                    value: (shape.y - image.paintedY) / image.paintedHeight
                    delayed: true
                    when: image.paintedHeight > 0 && root.enableDrag
                    restoreMode: Binding.RestoreNone
                }
            }
        }
    }
}