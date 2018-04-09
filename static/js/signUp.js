var rootUrl="http://127.0.0.1:5000/rest/KK";

var $ = function (id){
    return document.getElementById(id);
};


var findMatch = function (id) {
alert(id);
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

$("Rhome").onclick = function ()
{
var home = document.getElementById(this);
alert(home)
}

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

var findAllT=function(){
	$.ajax({
		   type:'GET',
		   url: rootUrl,
		   dataType:"json",
		   success:renderTable
		   });
};
$(document).ready(function() {
    var table = $('#HomeResultTable').DataTable();

    $('button').click( function() {
        var data = table.$('input, select').serialize();
        alert(
            "The following data would have been submitted to the server: \n\n"+
            data.substr( 0, 120 )+'...'
        );
        return false;
    } );
} );
var renderTable = function (data) {
    console.log("response");
    $.each(data, function (index, match) {
        $('#ticketTable').append('<tr><td>' + match.Id + '</td>' +
            '<td>' + match.home + '</td>' +
            '<td>' + match.away + '</td>' +
            '</td><td id="' + match.Id + '"><a href="#">' + '<button type="button" id ="EB" class="btn btn-info btn-md" data-toggle="modal" data-target="#myModal" onclick="findById(' + match.id + ')">Edit</button>' +
            '</td></tr>');

});
$('#table_id').DataTable();

$(document).ready(function(){
	findAllT();
});


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
