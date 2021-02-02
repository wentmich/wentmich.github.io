'use strict'

function playSound(event){
    // play the bell sound for found objects
    var myAudio = new Audio('../sounds/click1.mp3');
    myAudio.play();

    // play the objects individual sound
    var myId = event.target.id;
    myAudio = new Audio(getComputedStyle(document.getElementById(myId)).getPropertyValue('--sound'));
    setTimeout(() => { myAudio.play(); }, 100);
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

setAspectRatio();

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