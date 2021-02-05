'use strict'

function findObj(event){
    // play the bell sound for found objects
    var myAudio = new Audio('../sounds/click1.mp3');
    myAudio.play();

    // play the objects individual sound
    var myId = event.target.id;
    myAudio = new Audio(getComputedStyle(document.getElementById(myId)).getPropertyValue('--sound'));
    setTimeout(() => { myAudio.play(); }, 100);

    // get object properties
    var name = getComputedStyle(document.getElementById(myId)).getPropertyValue('--name');
    var number = getComputedStyle(document.getElementById(myId)).getPropertyValue('--number');
    var found = getComputedStyle(document.getElementById(myId)).getPropertyValue('--found');

    // update found status
    document.getElementById(myId).style.setProperty('--found', found + 1);

    // update color
    //getComputedStyle(document.getElementById(myId)).setProperty('--color', 'lightblue');
    document.getElementById(name).style.setProperty('font-weight', 'bolder');


}

function resetText(){
    textFit(document.getElementsByClassName('objBanner'), {alignHoriz: true, alignVert: true});
    window.addEventListener('resize', resetText);
}

function setAspectRatio() {
    var img = new Image();
    img.src = getComputedStyle(document.documentElement).getPropertyValue('--image');

    img.onload = function(){
        var width = img.width;
        var height = img.height;
        var aspectRatio = height / width;
        console.log("Aspect Ratio: " + aspectRatio)

        document.documentElement.style.setProperty('--aspectRatio', aspectRatio);
    }
}

/*
document.getElementById("loc1").addEventListener('click', playSound);
document.getElementById("loc2").addEventListener('click', playSound);
document.getElementById("loc3").addEventListener('click', playSound);
document.getElementById("loc4").addEventListener('click', playSound);
document.getElementById("loc5").addEventListener('click', playSound);
document.getElementById("loc6").addEventListener('click', playSound);
document.getElementById("loc7").addEventListener('click', playSound);
document.getElementById("loc8").addEventListener('click', playSound);
document.getElementById("loc9").addEventListener('click', playSound);
document.getElementById("loc10").addEventListener('click', playSound);
document.getElementById("loc11").addEventListener('click', playSound);
document.getElementById("loc12").addEventListener('click', playSound);
*/

// Adjust the sizes of some stuff to make it look nice.
setAspectRatio();
resetText();

var elements = document.getElementsByClassName("location");
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', findObj);
}