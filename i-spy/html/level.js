'use strict'

// function for clicking on any object
function findObj(event){
    // play the bell sound for found objects
    var myAudio = new Audio('../sounds/click1.mp3');
    myAudio.play();

    // get object properties
    var myId = event.target.id;
    var name = getComputedStyle(document.getElementById(myId)).getPropertyValue('--name');
    var NObjs = parseInt( getComputedStyle(document.getElementById(myId)).getPropertyValue('--number') );
    var found = parseInt( getComputedStyle(document.getElementById(myId)).getPropertyValue('--found') );
    var number = parseInt( getComputedStyle(document.getElementById(name)).getPropertyValue('--number') );
    var Ntot = parseInt( getComputedStyle(document.getElementById('objBanner')).getPropertyValue('--Ntot') );
    var Nfound = parseInt( getComputedStyle(document.getElementById('objBanner')).getPropertyValue('--Nfound') );

    // play the objects individual sound
    if (found == parseInt(0)){
        var soundName = "";
        soundName += "--sound";
        soundName += String(parseInt(number + 1));
        console.log(soundName);
        myAudio = new Audio(getComputedStyle(document.getElementById(myId)).getPropertyValue(soundName));}
    else{
        var soundName = "";
        soundName += "--sound";
        soundName += String(parseInt(number));
        console.log(soundName);
        myAudio = new Audio(getComputedStyle(document.getElementById(myId)).getPropertyValue(soundName));}
    setTimeout(() => { myAudio.play(); }, 100);

    // update found status, update number of found obj, update color of text
    if (found == parseInt(0)){
        document.getElementById(myId).style.setProperty('--found', 1);
        document.getElementById(name).style.setProperty('--number', parseInt(number + 1));
        document.getElementById('objBanner').style.setProperty('--Nfound', parseInt(Nfound + 1));
        if (parseInt(number + 1) >= NObjs){
            document.getElementById(name).style.setProperty('font-weight', 'bolder');
        }
    }

    // check for a win
    if (parseInt(Nfound + 1) == Ntot){
        var newAudio = new Audio('../sounds/victory.mp3');
        setTimeout(() => { newAudio.play(); }, 2000);
    }

}

// resize the text inside the object banner
function resetText(){
    textFit(document.getElementById('objBanner'), {alignHoriz: true, alignVert: true});
    window.addEventListener('resize', resetText);
}

// resize the main image to preserve aspect ratio
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

// play the intro reading if banner is clicked
function playBanner() {
    var myAudio = new Audio('../sounds/theater/ispy-theater.mp3');
    myAudio.play();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////// Executions of functions /////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Adjust the sizes of some stuff to make it look nice.
setAspectRatio();
resetText();
textFit(document.getElementsByClassName('header'), {alignVert: true});

var elements = document.getElementsByClassName("location");
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', findObj);
}

var banner = document.getElementById('objBanner');
banner.addEventListener('click', playBanner);