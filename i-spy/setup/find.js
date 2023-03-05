'use strict'

function printMousePos(event) {
    let box = document.querySelector('.image');
    let width = box.offsetWidth;
    let height = box.offsetHeight;

    let x = event.clientX; let y = event.clientY;

    console.log("left: " + 100.0 * x / width + "%;\n\ttop: " + 100.0 * y / height + "%;\n");
}

function getMousePos(event){
    let x = event.clientX; let y = event.clientY;
    return [x, y];
}

document.addEventListener("click", printMousePos);