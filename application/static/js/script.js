$(document).ready(function(){
    $('.sidenav').sidenav();
    $(".tooltipped").tooltip();
    $('select').formSelect();
});

function delete_flash() {
    const flash = document.querySelector('.flash-message');
    flash.remove();
}

function check_if_delete_confirmed() {
    // modal appears

    $.ajax({
        url: "/",
        type: 'POST',
        data: {
            
        }
    });
}
