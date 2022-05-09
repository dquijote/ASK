//Put in title readable date for human
var td_var = document.getElementsByClassName('td-timestamp');
for (var i = 0; i < td_var.length; i++){
    //     console.log(td_var[i].textContent);
    var date_from_stam = new Date(parseFloat(td_var[i].textContent)*1000);
    td_var[i].setAttribute('title', date_from_stam.toLocaleString());

}