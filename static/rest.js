var rootUrl = "http://127.0.0.1:5000/rest/Massages";
var Url = "http://127.0.0.1:5000/rest/Massage";
var UrlR = "http://127.0.0.1:5000/rest/MassageR";

var findMatch = function (sender) {
    $('#name').val(sender);
    findMatch2(sender)

    $.ajax({
        type: 'GET',
        url: UrlR + '/' + sender,
        dataType: "json",
        success: allR
    });
};

var findMatch2 = function (sender) {

    $.ajax({
        type: 'GET',
        url: Url + '/' + sender,
        dataType: "json",
        success: all
    });
};


var all = function (data) {
    kiki = data;
     console.log("all");
 $.each(data, function (index, match) {
     v = match.timeDay;


 })

return (v,data)
}

var allR = function (data) {
    $('#ch').empty();
    riri = data;



    soso = {};
    soso['kiki'] = kiki;
    soso['riri'] = riri;
    console.log(soso);
    sos(soso)



}

var sos = function (data) {
    $('#ch').empty();
   data = soso;
   alert(data);
         console.log("sos");

         for (i in data){

         }

     $.each(soso, function (index, m) {

         RT = m.timeDayR;
         alert(RT)
           RC = m.commentR;
             RS = m.idR;
         ST = m.timeDay;
         SC = m.comment;
             SS = m.id;


        if (ST>RT){
         renderMatchsosoR(RT,RC,RS);
          renderMatchsoso(ST,SC,SS);
      }else {
          renderMatchsoso(ST,SC,SS);
    renderMatchsosoR(RT,RC,RS);}
  })
}

var renderMatchsosoR = function (RT,RC,RS) {
console.log("renderMatch");

$('#msgCon').show();


     $('#ch').prepend('<li class="right clearfix">' +
         '<span class="chat-img pull-right">' +
         '<img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />' +
         '</span>' +
         '<div class="chat-body clearfix">' +
         '<div class="header">' +
         '<strong id="sender" class="primary-font"></strong>' +
         '<small class="pull-right text-muted">' +
         '<i id="timeday" class="fa fa-clock-o fa-fw"></i> '+ RT +
         '<p class="DD btn btn-danger " onclick="deleteMassege('+ RS +')" >X</p>' +
         '</small>' +
         '</div>' +
         '<p>'
         + RC +
         '</p>' +
         '</div>');





};
var renderMatchsoso = function (ST,SC,SS) {
console.log("renderMatch");

$('#msgCon').show();


     $('#ch').prepend('<li class="left clearfix">' +
         '<span class="chat-img pull-left">' +
         '<img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />' +
         '</span>' +
         '<div class="chat-body clearfix">' +
         '<div class="header">' +
         '<strong id="sender" class="primary-font"></strong>' +
         '<small class="pull-right text-muted">' +
         '<i id="timeday" class="fa fa-clock-o fa-fw"></i> '+ ST +
         '<p class="DD btn btn-danger" onclick="deleteMassege('+ SS +')" hidden>X</p>' +
         '</small>' +
         '</div>' +
         '<p>'
         + SC +
         '</p>' +
         '</div>');





};




var renderMatch = function (data) {
console.log("renderMatch");

$('#msgCon').show();



    $.each(data, function (index, match) {

     $('#ch').prepend('<li class="left clearfix">' +
         '<span class="chat-img pull-left">' +
         '<img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />' +
         '</span>' +
         '<div class="chat-body clearfix">' +
         '<div class="header">' +
         '<strong id="sender" class="primary-font"></strong>' +
         '<small class="pull-right text-muted">' +
         '<i id="timeday" class="fa fa-clock-o fa-fw"></i> '+ match.timeDay +
         '<p class="DD btn btn-danger" onclick="deleteMassege('+ match.id +')" hidden>X</p>' +
         '</small>' +
         '</div>' +
         '<p>'
         + match.comment +
         '</p>' +
         '</div>');

   })



};







var renderMatch2 = function (data) {
console.log("renderMatch2");
$('#msgCon').show();

    $.each(data, function (index, match) {

     $('#ch').prepend('<li class="right clearfix">' +
         '<span class="chat-img pull-right">' +
         '<img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />' +
         '</span>' +
         '<div class="chat-body clearfix">' +
         '<div class="header">' +
         '<strong id="sender" class="primary-font"></strong>' +
         '<small class="pull-right text-muted">' +
         '<i id="timeday" class="fa fa-clock-o fa-fw"></i> '+ match.timeDayR +
         '<p class="DD btn btn-danger " onclick="deleteMassege('+ match.idR +')" >X</p>' +
         '</small>' +
         '</div>' +
         '<p>'
         + match.commentR +
         '</p>' +
         '</div>');

   })
    $(".DD").hide();
};

$(document).ready(function(){
	$(".DD").hide();
	$('#ssh').hide();
	$('#msgCon').hide();

});

function up() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    	location.reload();
      document.getElementById("ccc").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "http://127.0.0.1:5000/loginDash", true);
  xhttp.send();
}


function updateDiv()
{
    $( "#ccc" ).load(window.location.reload());
}

var deleteMassege=function(id) {
	console.log('deleteMassege');
	$.ajax({
		type: 'DELETE',
		url: rootUrl + '/' + id,
		success: function(data, textStatus, jqXHR){
			alert('Ticket deleted successfully');
			updateDiv();
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('deleteTicket error');
		}
	});
};





$(document).on('click','#sh', function(){
$('.DD').show();
$('#sh').hide();
$('#ssh').show();
});

$(document).on('click','#ssh', function(){
$('.DD').hide();
$('#sh').show();
$('#ssh').hide();
});


