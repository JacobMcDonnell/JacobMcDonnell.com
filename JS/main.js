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
function dropdown(theID) {
  document.getElementById(theID).classList.toggle("show");
}
window.onclick = function(event) {	//when the user clicks anywhere else on the screen the menu disappears
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
