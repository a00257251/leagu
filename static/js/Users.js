var rootUrl = "http://127.0.0.1:5000/rest/Users";

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
        $('#UpcommingTable').append('<a href="#"><tr data-toggle="modal" data-target="#myModal"  onclick="findMatch(' + match.id + ')">'+
            '<td>' + match.userid  + '</td>' +
            '<td>' + match.desc  + '</td>' +
            '<td>' + match.chosenteam + '</td>' +
            '</td></tr>');

    })
};
$('#Upcomming_id').DataTable();


var findMatch = function (userid) {
    alert(userid);
    $.ajax({
        type: 'GET',
        url: rootUrl + '/' + userid,
        dataType: "json",
        success: renderMatch
    });
};

var renderMatch = function (data) {
console.log("response");
    $.each(data, function (index, match) {
        $('#TK').val(match.userid);
   })
};

$(document).ready(function () {
    findAllT();
});

