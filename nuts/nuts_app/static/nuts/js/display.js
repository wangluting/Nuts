// hide and display when content is too long

var plan_description = $(".plan_description");

plan_description.each(function(){    
    var content = $(this).html();        
    if(content.length < 150) return;
    
    $(this).html(
    	content.slice(0, 150)+'<span>... </span><a href="#" class="description_more">More</a>'+
        '<span style="display:none;">'+ content.slice(150, content.length)+
        ' <a href="#" class="description_hide">Hide</a></span>'
    );
}); 

$("body").on("click","a.description_more", function(){
    event.preventDefault();
    $(this).hide();
    $(this).prev().hide();
    $(this).next().show();        
});

$("body").on("click","a.description_hide", function(){
    event.preventDefault();
    $(this).parent().hide();
    $(this).parent().prev().show();
    $(this).parent().prev().prev().show();    
});

// when click one of the three labels, return all public plans/ plans that one follows/ plans from users one follows
$(".get_all").click(function(){
	$.ajax({  
		type: "GET",  
		url: "/nuts/get_all_public",  
		dataType: "json"
	})
	.done(function(data) {
			$(".tbody").html("");

            // like plan
            var like_plan_ids = data["user_like_plan_ids"];

			for (var i = 0; i < data.nuts.length; i++) {

				var nut = data.nuts[i];
				var newNut = $(".clone_plan").clone(true);


                // get the like status
                var status = "Like";
                if (like_plan_ids.indexOf(nut.id) >= 0) {
                    status = "Unlike";
                }
                // get how many people like this nut
                var like_num = nut.like_num;


				newNut.toggle();
				newNut.removeClass("clone_plan");
				newNut.find(".plan_img_link").attr("href", "/nuts/show-profile/" + nut.user_id + "/");
				newNut.find(".plan_title a").attr("href", "/nuts/view-plan/" + nut.id);
				newNut.find(".plan_img").attr("src", "/nuts/photo/" + nut.user_id + "/");
				newNut.find(".plan_author").attr("href", "/nuts/show-profile/" + nut.user_id + "/");
				newNut.find(".plan_title a").html(nut.title);
				newNut.find(".plan_author").html(nut.author);
				newNut.find(".plan_expire").html("expires: " + nut.expire_time);
				newNut.find(".plan_description").html(nut.description);
				newNut.find(".plan_time").html("posted on: " + nut.timestamp);


                // like plan
                newNut.find(".nut_id").attr("value", nut.id);
                newNut.find(".like_num").html(like_num);
                newNut.find(".like").html(status);


                // new set nut_id
                newNut.find(".plan").attr("id", nut.id);
                newNut.find(".comment_input").attr("id", "comment-field-" + nut.id);
                newNut.find(".comment_btn").attr("onclick", "addComment(" + nut.id + ")");

				var content = newNut.find(".plan_description").html();
			    if(content.length >= 150) { 		    
			    	newNut.find(".plan_description").html(
				    	content.slice(0, 150)+'<span>... </span><a href="#" class="description_more">More</a>'+
				        '<span style="display:none;">'+ content.slice(150, content.length)+
				        ' <a href="#" class="description_hide">Hide</a></span>'
				    );
			    }

                // new, comments
                comments_html = "";
                for (var j = 0; j < data.comments.length; j++) {
                    if (data.comments[j].nut_id == nut.id) {

                        var comment = data.comments[j];
                        // add all the comments for this nut
                        comments_html = comments_html
                        + '<img src="/nuts/photo/'+ comment.user_id + '/" ' + 'alt="' + comment.user + '" class="img-circle avatar">'
                        + '<div class="comment_body">'
                        + '<a href="/nuts/show-profile/' + comment.user_id + '/" class="plan_author">' + comment.username + ' </a>'
                        + '<span class="plan_time">' + comment.time + '</span>'
                        + '<p class="">' + comment.comment + '</p>'
                        + '</div>';
                    }

                }
                newNut.find(".comments").html(comments_html);
				
			    var row = "<tr><td>" + newNut.html() + "</tr></td>";
				$(".tbody").append(row);

				// console.log("----append-----");
			}

			
		if($(".get_eat").hasClass("active"))
			$(".get_eat").removeClass("active");
		if($(".get_follow").hasClass("active"))
			$(".get_follow").removeClass("active");
		$(".get_all").addClass("active");


		// initialize 6 nuts in a page manually here since the jquery init will only for once
		var tableRows = $(".tbody").find("tr");
        // must also reset first record number otherwise will not keep pace with other functions in jquery
        document.getElementsByTagName("tbody")[0].setAttribute("data-firstRecord", 0);
        tableRows.hide();
        tableRows.slice(0, 6).show();
        $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_paginate").show();
        if (tableRows.eq(0).is(":visible")) {
        	$(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_previous").hide();
        }
        if (tableRows.eq(tableRows.length - 1).is(":visible")) {
        	$(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_next").hide();
        }
	
    })
	.fail(function(data) {
		alert("fails to get public nuts!")
	})
});

// get all nuts one eat
$(".get_eat").click(function(){
	$.ajax({  
		type: "GET",  
		url: "/nuts/get_all_eat",  
		dataType: "json"
	})
	.done(function(data) {

			$(".tbody").html("");
            // like plan
            var like_plan_ids = data["user_like_plan_ids"];

			for (var i = 0; i < data.nuts.length; i++) {
				var nut = data.nuts[i];
				var newNut = $(".clone_plan").clone(true);

                // get the like status
                var status = "Like";
                if (like_plan_ids.indexOf(nut.id) >= 0) {
                    status = "Unlike";
                }
                // get how many people like this nut
                var like_num = nut.like_num;

				newNut.toggle();
				newNut.removeClass("clone_plan");
				newNut.find(".plan_img_link").attr("href", "/nuts/show-profile/" + nut.user_id + "/");
				newNut.find(".plan_title a").attr("href", "/nuts/view-plan/" + nut.id);
				newNut.find(".plan_img").attr("src", "/nuts/photo/" + nut.user_id + "/");
				newNut.find(".plan_author").attr("href", "/nuts/show-profile/" + nut.user_id + "/");
				newNut.find(".plan_title a").html(nut.title);
				newNut.find(".plan_author").html(nut.author);
				newNut.find(".plan_expire").html("expires: " + nut.expire_time);
				newNut.find(".plan_description").html(nut.description);
				newNut.find(".plan_time").html("posted on: " + nut.timestamp);

                // new set nut_id
                newNut.find(".plan").attr("id", nut.id);
                newNut.find(".comment_input").attr("id", "comment-field-" + nut.id);
                newNut.find(".comment_btn").attr("onclick", "addComment(" + nut.id + ")");

                // like plan
                newNut.find(".nut_id").attr("value", nut.id);
                newNut.find(".like_num").html(like_num);
                newNut.find(".like").html(status);

				if(nut.expires == "True")
					newNut.find(".label-danger").show();
				
				var content = newNut.find(".plan_description").html();
			    if(content.length >= 150) { 		    
			    	newNut.find(".plan_description").html(
				    	content.slice(0, 150)+'<span>... </span><a href="#" class="description_more">More</a>'+
				        '<span style="display:none;">'+ content.slice(150, content.length)+
				        ' <a href="#" class="description_hide">Hide</a></span>'
				    );
			    }

                // new, comments
                comments_html = "";
                for (var j = 0; j < data.comments.length; j++) {
                    if (data.comments[j].nut_id == nut.id) {

                        var comment = data.comments[j];
                        // add all the comments for this nut
                        comments_html = comments_html
                        + '<img src="/nuts/photo/'+ comment.user_id + '/" ' + 'alt="' + comment.user + '" class="img-circle avatar">'
                        + '<div class="comment_body">'
                        + '<a href="/nuts/show-profile/' + comment.user_id + '/" class="plan_author">' + comment.username + ' </a>'
                        + '<span class="plan_time">' + comment.time + '</span>'
                        + '<p class="">' + comment.comment + '</p>'
                        + '</div>';
                    }

                }
                newNut.find(".comments").html(comments_html);

			    var row = "<tr><td>" + newNut.html() + "</tr></td>";
				$(".tbody").append(row);

			}

		if($(".get_all").hasClass("active"))
			$(".get_all").removeClass("active");
		if($(".get_follow").hasClass("active"))
			$(".get_follow").removeClass("active");
		$(".get_eat").addClass("active");

        // initialize 6 nuts in a page manually here since the jquery init will only for once
        var tableRows = $(".tbody").find("tr");
        // must also reset first record number otherwise will not keep pace with other functions in jquery
        document.getElementsByTagName("tbody")[0].setAttribute("data-firstRecord", 0);
        tableRows.hide();
        tableRows.slice(0, 6).show();
        $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_paginate").show();
        if (tableRows.eq(0).is(":visible")) {
            $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_previous").hide();
        }
        if (tableRows.eq(tableRows.length - 1).is(":visible")) {
            $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_next").hide();
        }
		
	})
	.fail(function(data) {
		alert("fails to get public nuts!")
	})
});

$(".get_follow").click(function(){
	$.ajax({  
		type: "GET",  
		url: "/nuts/get_all_follow",  
		dataType: "json"
	})
	.done(function(data) {
			$(".tbody").html("");
            // like plan
            var like_plan_ids = data["user_like_plan_ids"];

			for (var i = 0; i < data.nuts.length; i++) {
				var nut = data.nuts[i];
				var newNut = $(".clone_plan").clone(true);

                // get the like status
                var status = "Like";
                if (like_plan_ids.indexOf(nut.id) >= 0) {
                    status = "Unlike";
                }
                // get how many people like this nut
                var like_num = nut.like_num;

				newNut.toggle();
				newNut.removeClass("clone_plan");
				newNut.find(".plan_img_link").attr("href", "/nuts/show-profile/" + nut.user_id + "/");
				newNut.find(".plan_title a").attr("href", "/nuts/view-plan/" + nut.id);
				newNut.find(".plan_img").attr("src", "/nuts/photo/" + nut.user_id + "/");
				newNut.find(".plan_author").attr("href", "/nuts/show-profile/" + nut.user_id + "/");
				newNut.find(".plan_title a").html(nut.title);
				newNut.find(".plan_author").html(nut.author);
				newNut.find(".plan_expire").html("expires: " + nut.expire_time);
				newNut.find(".plan_description").html(nut.description);
				newNut.find(".plan_time").html("posted on: " + nut.timestamp);

                // new set nut_id
                newNut.find(".plan").attr("id", nut.id);
                newNut.find(".comment_input").attr("id", "comment-field-" + nut.id);
                newNut.find(".comment_btn").attr("onclick", "addComment(" + nut.id + ")");

                // like plan
                newNut.find(".nut_id").attr("value", nut.id);
                newNut.find(".like_num").html(like_num);
                newNut.find(".like").html(status);

				if(nut.expires == "True")
					newNut.find(".label-danger").show();
				
				var content = newNut.find(".plan_description").html();
			    if(content.length >= 150) { 		    
			    	newNut.find(".plan_description").html(
				    	content.slice(0, 150)+'<span>... </span><a href="#" class="description_more">More</a>'+
				        '<span style="display:none;">'+ content.slice(150, content.length)+
				        ' <a href="#" class="description_hide">Hide</a></span>'
				    );
			    }

                // new, comments
                comments_html = "";
                for (var j = 0; j < data.comments.length; j++) {
                    if (data.comments[j].nut_id == nut.id) {

                        var comment = data.comments[j];
                        // add all the comments for this nut
                        comments_html = comments_html
                        + '<img src="/nuts/photo/'+ comment.user_id + '/" ' + 'alt="' + comment.user + '" class="img-circle avatar">'
                        + '<div class="comment_body">'
                        + '<a href="/nuts/show-profile/' + comment.user_id + '/" class="plan_author">' + comment.username + ' </a>'
                        + '<span class="plan_time">' + comment.time + '</span>'
                        + '<p class="">' + comment.comment + '</p>'
                        + '</div>';
                    }

                }
                newNut.find(".comments").html(comments_html);

			    var row = "<tr><td>" + newNut.html() + "</tr></td>";
				$(".tbody").append(row);

			}

		if($(".get_all").hasClass("active"))
			$(".get_all").removeClass("active");
		if($(".get_eat").hasClass("active"))
			$(".get_eat").removeClass("active");
		$(".get_follow").addClass("active");

        // initialize 6 nuts in a page manually here since the jquery init will only for once
        var tableRows = $(".tbody").find("tr");
        // must also reset first record number otherwise will not keep pace with other functions in jquery
        document.getElementsByTagName("tbody")[0].setAttribute("data-firstRecord", 0);
        tableRows.hide();
        tableRows.slice(0, 6).show();
        $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_paginate").show();
        if (tableRows.eq(0).is(":visible")) {
            $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_previous").hide();
        }
        if (tableRows.eq(tableRows.length - 1).is(":visible")) {
            $(".tbody").closest(".sp_wrapper").find(".sp_navigator .sp_next").hide();
        }
        
	})
	.fail(function(data) {
		alert("fails to get public nuts!")
	})
});

$(".get_profile").click(function(){
	$(".get_profile").addClass("active");
	$(".get_nuts").removeClass("active");
	$(".profile_block").show();
	$(".nuts").hide();
});

$(".get_nuts").click(function(){
	$(".get_profile").removeClass("active");
	$(".get_nuts").addClass("active");
	$(".profile_block").hide();
	$(".nuts").show();
});

$(".follow").click(function(){
	if($(".follow").html() == "Follow")
		var follow = "True";
	else
		var follow = "False";
	var id = $(event.target).parents(".container-fluid").find(".user_id").val();
	$.ajax({  
		type: "GET",  
		url: "/nuts/follow_user/" + follow + "/" + id,
	})
	.done(function(data) {		
		if($(".follow").html() == "Follow")
			$(".follow").html("Unfollow");
		else
			$(".follow").html("Follow");
	})
});

// bw: like plan
function like() {

    if($(event.target).html() == "Like")
        var like = "True";
    else
        var like = "False";

    var nut_id = $(event.target).parents(".plan").find(".nut_id").val();
    var like_num = parseInt($(event.target).parents(".plan").find(".like_num").html());

    // change like status
    // update number of people like this nut
    if($(event.target).html() == "Like") {
        $(event.target).html("Unlike");

        $(event.target).parents(".plan").find(".like_num").html(like_num+1);

    } else {
        $(event.target).html("Like");
        $(event.target).parents(".plan").find(".like_num").html(like_num-1);
    }
    
    // update database
    $.ajax({  
        type: "GET",  
        url: "/nuts/like_plan/" + like + "/" + nut_id,
    })
    .done(function(data) { 
        // console.log("do nothing");      
    })
}


function addComment(nut_id){

    var commentField = $("#comment-field"+"-"+nut_id);

    $.post("/nuts/add-comment", {comment: commentField.val(), nut_id: nut_id})
      .done(function(data) {

        user_id = data.user_id;
        username = data.username;
        time = data.time;

        var node = document.createElement("div");
        node.innerHTML = '<img src="/nuts/photo/'+ user_id + '/" ' + 'alt="' + username + '" class="img-circle avatar">'
                        + '<div class="comment_body">'
                        + '<a href="/nuts/show-profile/' + user_id + '/" class="plan_author">' + username + ' </a>'
                        + '<span class="plan_time">' + time + '</span>'
                        + '<p class="">' + commentField.val() + '</p>'
                        + '</div>';

        var commentlist = document.getElementById(nut_id).querySelector("#comments");

        commentlist.appendChild(node);

        commentField.val("").focus();

      });
}

$(document).ready(function() {
	$(".eat").click(function(){
		if($(".eat").html() == "Eat")
			var eat = "True";
		else
			var eat = "False";
		var id = $(event.target).parents(".container-fluid").find(".nut_id").val();
		$.ajax({  
			type: "GET",  
			url: "/nuts/eat_plan/" + eat + "/" + id,
		})
		.done(function(data) {

			if($(".eat").html() == "Eat") {
	            $(".eat").text("Uneat");
	            //console.log($('#number').html())
	            var cnt = parseInt($('#number').html()) + 1;
	            console.log(cnt)
	            $('#number').html(cnt);
	        }
	        else {
	            $(".eat").text("Eat");
	            console.log($('#number').html())

	            var cnt = parseInt($('#number').html()) - 1;
	            console.log(cnt)
	            $('#number').html(cnt);

	        }

		})
	});

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
