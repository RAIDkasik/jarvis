// function main() {
//         eel.settings()().then(data => {
//             document.body.style.color = data['text'];
//             document.querySelector(".name").style.color = data['name'];
//             if (data['background'][0] == "#"){
//                 document.querySelector("body").style.background = data['background'];
//             } else {
//                 document.querySelector("body").style.backgroundImage = 'url('+data['background']+')';
//             }

//             if (data['header'][0] == "#"){
//                 document.querySelector("header").style.background = data['header'];
//                 let menu = document.querySelectorAll(".menu");
//                 for (let i = 0; i < menu.length; i++){
//                     menu[i].style.background = data['header'];
//                 }
                
//             } else {
//                 document.querySelector("header").style.backgroundImage = 'url('+data['header']+')';
//                 let menu = document.querySelectorAll(".menu");
//                 for (let i = 0; i < menu.length; i++){
//                     menu[i].style.background = 'url('+data['header']+')';
//                 }        
//             }

//             return data; 
//         });
// }
// function main(){
//     eel.settings()().then(data => {
//         console.log(data['background']);
//         document.querySelector("body").style.setProperty('--background', data['background']);
//         document.querySelector("body").style.setProperty('--text', data['text']);
//         document.querySelector("header").style.setProperty('--header', data['header']);
//     });
// }
// main();
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function settings() {
    eel.settings()().then(data => {
        console.log(27);
        console.log(data);
        document.querySelector(".b").value = data['background'];
        document.querySelector(".h").value = data['header'];
        document.querySelector(".t").value = data['text'];
        document.querySelector(".n").value = data['name'];
        document.querySelector(".s").value = data['settings'];
        
    });
    return eel.settings();
}

$(document).on('click', '.menu', function(event) {
    let classes = event.target.className;
    console.log(classes);
    window.location.href = classes.split(" ")[1]+'.html';
});

$(document).on('click', '.links', function(event) {
    console.log(event.target.innerHTML);
    if (event.target.innerHTML == "ГЛАВНАЯ"){
        window.location.href = "main.html";
    }
    else{
        document.querySelector(".settings").style.opacity = "1";
        document.querySelector(".settings").style.transform = "translateX(90%)";
    }
});
$(document).on('click', '.close', function(event) {
    document.querySelector(".settings").style.opacity = "0";
    document.querySelector(".settings").style.transform = "translateX(150%)";
});


