
$(document).ready(function() {
	if($(".my_id").val() != null) 
		localStorage.setItem("my_id", $(".my_id").val());
	
	$(".message").click(function() {
		if($('#chat').css('display') == 'none' && $('.direct-chat-messages').children().length <= 2) {
			var room_id = localStorage.getItem("room_id")
			var other_id = localStorage.getItem("other_id")
			var other_username = localStorage.getItem("other_username")
			var my_id = localStorage.getItem("my_id");
			if(room_id === null)
				return;
			if(other_username === null) {
				alert("No chatting history!");
				return;
			}
			else
				var title = "Chat " + other_username + ":";
			$(".box-title").html(title);
			$.ajax({  
				type: "GET",  
				url: "/nuts/get_message",  
				dataType: "json",
				data: {'room_id': room_id},
			})
			.done(function(data) {
				var obj = jQuery.parseJSON(data);
				for(var i=0; i<obj.length; i++) {
					var fields = obj[i].fields;
					if(fields.sender_id == my_id) {
	            		var msg = $(".direct-chat-msg-mine").clone(true);
	            		msg.show();
	            		msg.find(".direct-chat-name").html(fields.sender_username);
	            		msg.find(".direct-chat-text").text(fields.message);
	            		msg.find(".direct-chat-timestamp").html(fields.timestamp);
	            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + fields.sender_id + "/");
	            		msg.removeClass("direct-chat-msg-mine");
	            		$(".direct-chat-messages").append(msg);
	            	}
	            	else if(fields.sender_id == other_id){
	            		var msg = $(".direct-chat-msg-other").clone(true);
	            		msg.show();
	            		msg.find(".direct-chat-name").html(fields.sender_username);
	            		msg.find(".direct-chat-text").text(fields.message);
	            		msg.find(".direct-chat-timestamp").html(fields.timestamp);
	            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + fields.sender_id + "/");
	            		msg.removeClass("direct-chat-msg-other");
	            		$(".direct-chat-messages").append(msg);
	            	}
				}

				var wtf = $(".direct-chat-messages");
				var height = wtf[0].scrollHeight;
				wtf.scrollTop(height);
		    })
		    .fail(function(data) {
				alert("cannot get messages!")
		    })
		}
		$("#chat").show();

		var wtf = $(".direct-chat-messages");
		var height = wtf[0].scrollHeight;
		wtf.scrollTop(height);
		
		socket = new WebSocket("ws://" + window.location.host);
		socket.onmessage = function (message) {
            // Decode the JSON
            console.log("Got websocket message " + message.data);
            var data = JSON.parse(message.data);
            // Handle errors
            if (data.error) {
                alert(data.error);
                return;
            }
            else if (data.message) {
            	if(data.id == my_id) {
            		var msg = $(".direct-chat-msg-mine").clone(true);
            		msg.show();
            		msg.find(".direct-chat-name").html(data.username);
            		msg.find(".direct-chat-text").text(data.message);
            		msg.find(".direct-chat-timestamp").html(new Date($.now()));
            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + data.id + "/");
            		msg.removeClass("direct-chat-msg-mine");
            		$(".direct-chat-messages").append(msg);
            	}
            	else if(data.id == other_id) {
            		var msg = $(".direct-chat-msg-other").clone(true);
            		msg.show();
            		msg.find(".direct-chat-name").html(data.username);
            		msg.find(".direct-chat-text").text(data.message);
            		msg.find(".direct-chat-timestamp").html(new Date($.now()));
            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + data.id + "/");
            		msg.removeClass("direct-chat-msg-other");
            		$(".direct-chat-messages").append(msg);
            	}


        		var wtf = $(".direct-chat-messages");
        		var height = wtf[0].scrollHeight;
        		wtf.scrollTop(height);
            } else {
                console.log("Cannot handle message!");
            }
        };
		// Call onopen directly if socket is already open
		if (socket.readyState == WebSocket.OPEN) socket.onopen();

		socket.onopen = function () {
            console.log("Connected to chat socket");
    		socket.send(JSON.stringify({
                "command": "join",
                "room": room_id
            }));
        };
        socket.onclose = function () {
            console.log("Disconnected from chat socket");
        }

	});

	$(".btn-hide").click(function() {
		$(".box-body").toggle();
		$(".box-footer").toggle();
		if($(".btn-hide i").hasClass("fa-minus")) {
			$(".btn-hide i").removeClass("fa-minus");
			$(".btn-hide i").addClass("fa-plus");
		}
		else {
			$(".btn-hide i").removeClass("fa-plus");
			$(".btn-hide i").addClass("fa-minus");
		}
	});

	$(".btn-remove").click(function() {
		$("#chat").hide();
	});

	$(".btn-message").click(function() {
		$("#chat").show();
		var title = "Chat " + $(".profile_username").html() + ":";
		$(".box-title").html(title);
		var other_id = $(".user_id").val();
		var my_id = localStorage.getItem("my_id");
		if(other_id < my_id)
			var room_id = other_id + "." + my_id;
		else
			var room_id = my_id + "." + other_id;

		if(room_id != localStorage.getItem("room_id")) {
			$(".direct-chat-msg:visible").remove();
		}


		localStorage.setItem("room_id", room_id);
		localStorage.setItem("other_id", other_id);
		localStorage.setItem("other_username", $(".profile_username").html());

		if($('.direct-chat-messages').children().length <= 2) {
			var room_id = localStorage.getItem("room_id")
			var other_id = localStorage.getItem("other_id")
			var other_username = localStorage.getItem("other_username")
			var my_id = localStorage.getItem("my_id");
			if(room_id === null)
				return;
			var title = "Chat " + other_username + ":";
			$(".box-title").html(title);
			$.ajax({
				type: "GET",
				url: "/nuts/get_message",
				dataType: "json",
				data: {'room_id': room_id},
			})
			.done(function(data) {
				var obj = jQuery.parseJSON(data);
				for(var i=0; i<obj.length; i++) {
					var fields = obj[i].fields;
					if(fields.sender_id == my_id) {
	            		var msg = $(".direct-chat-msg-mine").clone(true);
	            		msg.show();
	            		msg.find(".direct-chat-name").html(fields.sender_username);
	            		msg.find(".direct-chat-text").text(fields.message);
	            		msg.find(".direct-chat-timestamp").html(fields.timestamp);
	            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + fields.sender_id + "/");
	            		msg.removeClass("direct-chat-msg-mine");
	            		$(".direct-chat-messages").append(msg);
	            	}
	            	else if(fields.sender_id == other_id){
	            		var msg = $(".direct-chat-msg-other").clone(true);
	            		msg.show();
	            		msg.find(".direct-chat-name").html(fields.sender_username);
	            		msg.find(".direct-chat-text").text(fields.message);
	            		msg.find(".direct-chat-timestamp").html(fields.timestamp);
	            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + fields.sender_id + "/");
	            		msg.removeClass("direct-chat-msg-other");
	            		$(".direct-chat-messages").append(msg);
	            	}
				}
				var wtf = $(".direct-chat-messages");
				var height = wtf[0].scrollHeight;
				wtf.scrollTop(height);

		    })
		    .fail(function(data) {
				alert("cannot get messages!")
		    })
		}

		socket = new WebSocket("ws://" + window.location.host + "/chat/");
		socket.onmessage = function (message) {
            // Decode the JSON
            console.log("Got websocket message " + message.data);
            var data = JSON.parse(message.data);
            // Handle errors
            if (data.error) {
                alert(data.error);
                return;
            }
            else if (data.message) {
            	if(data.id == my_id) {
            		var msg = $(".direct-chat-msg-mine").clone(true);
            		msg.show();
            		msg.find(".direct-chat-name").html(data.username);
            		msg.find(".direct-chat-text").text(data.message);
            		msg.find(".direct-chat-timestamp").html(new Date($.now()));
            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + data.id + "/");
            		msg.removeClass("direct-chat-msg-mine");
            		$(".direct-chat-messages").append(msg);
            	}
            	else if(data.id == other_id) {
            		var msg = $(".direct-chat-msg-other").clone(true);
            		msg.show();
            		msg.find(".direct-chat-name").html(data.username);
            		msg.find(".direct-chat-text").text(data.message);
            		msg.find(".direct-chat-timestamp").html(new Date($.now()));
            		msg.find(".direct-chat-img").attr("src", "/nuts/photo/" + data.id + "/");
            		msg.removeClass("direct-chat-msg-other");
            		$(".direct-chat-messages").append(msg);
            	}

        		var wtf = $(".direct-chat-messages");
        		var height = wtf[0].scrollHeight;
        		wtf.scrollTop(height);
            } else {
                console.log("Cannot handle message!");
            }
        };
		// Call onopen directly if socket is already open
		if (socket.readyState == WebSocket.OPEN) socket.onopen();

		socket.onopen = function () {
            console.log("Connected to chat socket");
    		socket.send(JSON.stringify({
                "command": "join",
                "room": room_id
            }));
        };
        socket.onclose = function () {
            console.log("Disconnected from chat socket");
        }
	});

	$(".chat_send").click(function(event) {
		event.preventDefault();
		var msg = $(".chat_message").val()
		$(".chat_message").val('');
		socket.send(JSON.stringify({
            "command": "send",
            "room": localStorage.getItem("room_id"),
            "message": msg
        }));
	});

});