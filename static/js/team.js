var rootUrl = "http://127.0.0.1:5000/rest/TT";

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
        $('#PLTable').append('<a href="#"><tr data-toggle="modal" data-target="#myModal"  onclick="findMatch(' + match.N + ')">'+
            '<td>' + match.N + '</td>' +
            '<td>' + match.Team +'</td>'+
            '<td>' + match.Pl  + '</td>' +
            '<td>' + match.W   + '</td>' +
            '<td>' + match.D   + '</td>' +
            '<td>' + match.L   + '</td>' +
            '<td>' + match.F   + '</td>' +
            '<td>' + match.A   + '</td>' +
            '<td>' + match.GD  + '</td>' +
            '<td>' + match.Pts + '</td>' +
            '</td></tr>');

    })
};
$('#PL_id').DataTable();


var findMatch = function (Team) {
    alert(Team);
    $.ajax({
        type: 'GET',
        url: rootUrl + '/' + Team,
        dataType: "json",
        success: renderMatch
    });
};

var renderMatch = function (data) {
console.log("response");
    $.each(data, function (index, match) {
        $('#Team').append('<option value="'+ match.Team +'" selected>'+ match.Team +'</option>');
   })
};

$(document).ready(function () {
    findAllT();
});

