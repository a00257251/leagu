var rootUrl = "http://127.0.0.1:5000/rest/KK";

var findAllT = function () {
    $.ajax({
        type: 'GET',
        url: rootUrl,
        dataType: "json",
        success: renderTable
    });
};

var renderTable = function (data) {
    console.log("response");
    $.each(data, function (index, match) {
        $('#UpcommingTable').append('<a href="#"><tr data-toggle="modal" data-target="#myModal"  onclick="findMatch(' + match.Id + ')">'+
            '<td>' + match.home + '</td>' +
            '<td>' + match.time + '</td>' +
            '<td>' + match.date + '</td>' +
            '<td>' + match.away + '</td>' +
            '</td></tr>');

    })
};
$('#Upcomming_id').DataTable();


var findMatch = function (Id) {
    alert(Id);
    $.ajax({
        type: 'GET',
        url: rootUrl + '/' + Id,
        dataType: "json",
        success: renderMatch
    });
};

var renderMatch = function (data) {
console.log("response");
    $.each(data, function (index, match) {
        $('#Tea1').append('<option value="'+ match.home +'" selected>'+ match.home +'</option>');
        $('#Tea2').append('<option value="'+ match.away +'" selected>'+ match.away +'</option>');
        $('#Tea').append('<option value="'+ match.home +'" selected>'+ match.home +'</option>');
        $('#Tea').append('<option value="'+ match.away +'" selected>'+ match.away +'</option>');
   })

};

$(document).ready(function () {
    findAllT();
});

