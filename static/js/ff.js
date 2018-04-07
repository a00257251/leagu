var $ = function (id) {
    return document.getElementById(id);
};

var validation = function() {
    var names = document.getElementById("inputName").value;
    var users = document.getElementById("inputEmail").value;
    var passes = document.getElementById("inputPassword").value;

     if ((users == null) || (passes == null) || (names == null)){
         alert ("fuck you");
     }else {
        $(function() {
            $('#btnSignUp').click(function() {
                $.ajax({
                    url: '/signUp',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response) {
                        console.log(response);

                        window.open("google.ie");
                        alert('Wellcome');
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });
        });
     }
     window.open("google.ie");
     alert('Wellcome');
};

widow.onclick = function(){
    $("btnSignUp").onclick = validation;

    };