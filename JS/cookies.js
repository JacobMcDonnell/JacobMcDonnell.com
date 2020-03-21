function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}  
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
} 
function checkCookie() {
    var theme=getCookie("theme");
    if(theme == ""){
        setCookie("theme","PurpleAndDark",365);
        window.location.reload(false);
    }else if(theme == "GreenAndWhite"){
        document.getElementById("cssFile").href = "CSS/main.css";
    }else if(theme == "GreenAndDark"){
        document.getElementById("cssFile").href = "CSS/GreenAndDark.css";
    }else if(theme == "PurpleAndWhite"){
        document.getElementById("cssFile").href = "CSS/PurpleAndWhite.css";
    }else if(theme == "PurpleAndDark"){
        document.getElementById("cssFile").href = "CSS/PurpleAndDark.css";
    }
}
