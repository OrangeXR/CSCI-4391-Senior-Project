function openChatWindow() {
    document.getElementById("chatBox").style.display = "block";
    localStorage.setItem("chatOpen", "true"); /* Stores status of chatwindow */
}

function closeChatWindow() {
    document.getElementById("chatBox").style.display = "none";
    localStorage.setItem("chatOpen", "false"); /* Stores status of chatwindow */
}

/* Source - https://stackoverflow.com/a/12767900
Posted by D.A.J. DEV, modified by community. See post 'Timeline' for change history
 Retrieved 2026-04-13, License - CC BY-SA 4.0
 */
/* This is for the loading of the recipe*/
function showLoading(){
    document.getElementById("loading-box").style.display = "flex"
}

//to get rid of the loader
// https://www.w3schools.com/jsref/prop_style_display.asp
//https://www.javascripttutorial.net/javascript-dom/javascript-domcontentloaded/
document.addEventListener("DOMContentLoaded", function () {
    console.log("Loaded Yay!");
    document.getElementById("loading-box").style.display = "none";
});
