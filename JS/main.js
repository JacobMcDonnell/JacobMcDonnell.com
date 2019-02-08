function searchDuck(event){
    var x = document.getElementById('Search').value;
    if (event.keyCode == 13 || event.which == 13) { 
        if (x == '/4chan'){
            document.getElementById("pLink").innerHTML = "4chan";
            document.getElementById("pLink").href = "https://4chan.org/";
            document.getElementById("pLinks").innerHTML = "4channel";
            document.getElementById("pLinks").href = "https://4channel.org/";
        } 
        else{location='https://duckduckgo.com/?q=' + encodeURIComponent(document.getElementById('Search').value);}}//13 = enter
}
function FocusOnInput(){
    document.getElementById("Search").focus();
}