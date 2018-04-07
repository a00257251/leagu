

var $ = function (id){
    return document.getElementById(id);
};


var signup=function () {
   $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
                window.location.href = "/login";
                alert('Wellcome');
                //if(response === 200) location.href = "Home.html"
            },
            error: function (error) {
                console.log(error);
            }
        });
};


//$(document).on('click','#btnSignUp', function(){
window.onclick = function()
{
    $("btnSignUp").onclick = function()
    {
        var x = document.getElementById("inputName").value;
        if (x !=="")
        {
            signup()

        }
        else
            {
             alert("Name must be filled out");
             return false;

        }
    }
};

document.onload = function()
{
   // findAllT();
    $.ajax({
        url: '/Fixtures',
        data: $('table').serialize(),
        type: 'GET',
        success: function (response) {
            console.log(response);
            window.location.href = "/login";
            alert('Wellcome');
            //if(response === 200) location.href = "Home.html"
        },
        error: function (error) {
            console.log(error);
        }
    });
};

var findAllT = function () {
    $.ajax({
        type: 'GET',
        url: rootUrl,
        dataType: "json",
        success: renderTable
    });
};

var renderTable = function (data) {
    list = data;
    console.log("response");
    $.each(list, function (index, match) {
        $('#ticketTable').append('<tr><td>' + match.id + '</td>' +
            '<td>' + match.home + '</td>' +
            '<td>' + match.away + '</td>' +
            '</td><td id="' + match.id + '"><a href="#">' + '<button type="button" id ="EB" class="btn btn-info btn-md" data-toggle="modal" data-target="#myModal" onclick="findById(' + match.id + ')">Edit</button>' +
            '</td></tr>');
    })
};


var findMatch = function (id) {

    $.ajax({
        type: 'GET',
         url: rootUrl + '/' + id,
        dataType: "json",
        success: renderList
        });
};

var renderList = function (data) {
    $('#Team1').val(data.home);
    $('#Team2').val(data.away);


};


// Get the elements with class="column"
var elements = document.getElementsByClassName("card");

// Declare a loop variable
var i;

// Grid View
function gridView() {
    for (i = 0; i < elements.length; i++) {
        elements[i].style.width = "50%";
    }
}
