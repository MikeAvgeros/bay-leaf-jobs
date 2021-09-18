/* jshint esversion: 8 */

$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
});

function delete_flash() {
    const flash = document.querySelector('.flash-message');
    flash.remove();
}
