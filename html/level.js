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
    var NObjs = parseInt( getComputedStyle(document.getElementById(myId)).getPropertyValue('--number') );
    var found = parseInt( getComputedStyle(document.getElementById(myId)).getPropertyValue('--found') );
    var number = parseInt( getComputedStyle(document.getElementById(name)).getPropertyValue('--number') );
    console.log(name + ' ' + NObjs + ' ' + found + ' ' + number);

    // update found status
    if (found == 0){
        document.getElementById(myId).style.setProperty('--found', 1);
        document.getElementById(name).style.setProperty('--number', parseInt(number + 1));
        console.log('Made it in')
        if (parseInt(number + 1) >= NObjs){
            document.getElementById(name).style.setProperty('color', 'var(--green)');
        }
    }
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

// Adjust the sizes of some stuff to make it look nice.
setAspectRatio();
resetText();

var elements = document.getElementsByClassName("location");
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', findObj);
}