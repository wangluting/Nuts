function populateAllList() {
    $.get("/nuts/view-all-plan")
        .done(function (data) {
            var list = $("#all-list");
            list.html('')
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
                console.log(pre.html())
                new_nut.data("nut-id", nut.id);
                list.prepend(new_nut);
            }
        });
}

$(document).ready(function () {

    populateAllList();


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
