import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    width: 400
    height: 300
    visible: true
    title: "Test"

    Column {
        anchors.centerIn: parent
        spacing: 10

        Button {
            text: "Click Me"
            onClicked: console.log("clicked")
        }

        TextField {
            placeholderText: "Type here"
        }
    }
}

