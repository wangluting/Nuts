function populateTodoList() {
    $.get("/nuts/get-todo")
        .done(function (data) {
            var parent = document.getElementById("TODO")
            for (var i = 0; i < data.nuts.length; i++) {
                nut = data.nuts[i];
                var new_nut = $(nut.html);
                var pre = new_nut.find('#nutPrivilege')
                if (pre.html() == 'Public') {
                    pre.html("&#9829");
                }
                else {
                    pre.html("&#9827");
                }
                new_nut.data("nut-id", nut.id);
                console.log(new_nut.html());
                parent.innerHTML += new_nut.html();
            }
        });
}

function populateDoingList() {
    $.get("/nuts/get-doing")
        .done(function (data) {
            var parent = document.getElementById("DOING")
            for (var i = 0; i < data.nuts.length; i++) {
                nut = data.nuts[i];
                var new_nut = $(nut.html);
                var pre = new_nut.find('#nutPrivilege')
                if (pre.html() == 'Public') {
                    pre.html("&#9829");
                }
                else {
                    pre.html("&#9827");
                }
                new_nut.data("nut-id", nut.id);
                parent.innerHTML += new_nut.html()
            }
        });
}

function populateDoneList() {
    $.get("/nuts/get-done")
        .done(function (data) {
            var parent = document.getElementById("DONE")
            for (var i = 0; i < data.nuts.length; i++) {
                nut = data.nuts[i];
                var new_nut = $(nut.html);
                var pre = new_nut.find('#nutPrivilege')
                if (pre.html() == 'Public') {
                    pre.html("&#9829");
                }
                else {
                    pre.html("&#9827");
                }
                new_nut.data("nut-id", nut.id);
                parent.innerHTML += new_nut.html()
            }
        });
}


$(document).ready(function () {
    // set time
    var today = new Date();
    document.getElementById("time").innerHTML = today.toDateString();

    populateTodoList();
    populateDoingList();
    populateDoneList();


  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});