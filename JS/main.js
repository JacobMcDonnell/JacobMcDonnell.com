function searchDuck(event){
    var x = document.getElementById('Search').value;
    if (event.keyCode == 13 || event.which == 13) { 
        if (x == '/4chan'){
            fourChan()
        } 
        else if (x == '/help'){
            help()
        }
        else{location='https://duckduckgo.com/?q=' + encodeURIComponent(document.getElementById('Search').value);}}//13 = enter
}
function FocusOnInput(){
    document.getElementById("Search").focus();
}