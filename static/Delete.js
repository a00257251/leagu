var rootUrl = "http://127.0.0.1:5000/rest/Users";
var Url = "http://127.0.0.1:5000/rest/Userss";
function updateDiv() {
    $("#ccc").load(window.location.reload());
}

var deleteUser = function (id) {
    console.log('deleteUser');
    $.ajax({
        type: 'DELETE',
        url: "http://127.0.0.1:5000/rest/Userss" + '/' + id,
        success: function (data, textStatus, jqXHR) {
            alert('Ticket deleted successfully');
            updateDiv();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('deleteUser error');
        }
    });
};


var updateUser = function (id) {
    console.log('updateUser');
    $.ajax({
        type: 'PUT',
        contentType: 'application/json',
        url: 'http://127.0.0.1:5000/rest/Users' + '/' + id,
        dataType: "json",
        data: formToJSON(id),
        success: function (data, textStatus, jqXHR) {
            alert('Ticket Update successfully');
            updateDiv();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('updateeUser error');
        }
    });
};


var formToJSON = function (id) {
    var userId = id;
    return JSON.stringify({
        "fname": $('#fname').val(),
        "lname": $('#lname').val(),
        "tel": $('#tel').val(),
        "uemail": $('#uemail').val(),
        "username": $('#username').val(),
        "upassword": $('#upassword').val()

    });
};


$(document).on('click', '#deleteuserr2', function () {
    $('.deleteUserButton').hide();
    $('#deleteuserr').show();
    $('#deleteuserr2').hide();
    $('.updateform').hide();
    $('#updateuserr').show();
    $('#updateuserr2').hide();
    $('.tds').show();
     $('.updateUserButton').hide();
});

$(document).on('click', '#deleteuserr', function () {
    $('.deleteUserButton').show();
    $('#deleteuserr').hide();
    $('#deleteuserr2').show();
       $('.updateform').hide();
    $('#updateuserr').show();
    $('#updateuserr2').hide();
    $('.tds').show();
     $('.updateUserButton').hide();
});

$(document).on('click', '#updateuserr2', function () {
    $('.updateform').hide();
    $('#updateuserr').show();
    $('#updateuserr2').hide();
    $('.tds').show();
     $('.updateUserButton').hide();
      $('.deleteUserButton').hide();
});

$(document).on('click', '#updateuserr', function () {
    $('.updateform').show();
    $('#updateuserr').hide();
    $('.tds').hide();
    $('#updateuserr2').show();
    $('.updateUserButton').show();
     $('.deleteUserButton').hide();

});

$(document).ready(function () {
    $('.deleteUserButton').hide();
    $('#deleteuserr2').hide();
    $('.updateform').hide();
    $('#updateuserr2').hide();
    $('.updateUserButton').hide();

});


$(document).on('click', '#sh', function () {
    $('.DD').show();
    $('#sh').hide();
    $('#ssh').show();
});

$(document).on('click', '#ssh', function () {
    $('.DD').hide();
    $('#sh').show();
    $('#ssh').hide();
});


