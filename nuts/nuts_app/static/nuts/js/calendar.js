/**
 * 
 */
$(document).ready(function() {
	
    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
        // put your options and callbacks here
    	header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,basicWeek,basicDay'
		},
		selectable: true,
		selectHelper: true,
		navLinks: true,
		editable: true,
		select: function(start, end) {
			var s = new Date(start) 
			s.setDate(s.getDate()+1);
			var startD = s.getMonth() + "/" + s.getDate() + "/" + s.getFullYear()
			var e = new Date(end)
			var endD = e.getMonth() + "/" + e.getDate() + "/" + e.getFullYear()
			window.wxc.xcConfirm('Do you want to create a nut from ' + startD + ' to ' + endD + "?","confirm",{onOk:function(){
				var st = Date.parse(start);
				var en = Date.parse(end);
				var form = $('#hidden_form');
				form.attr('action', "/nuts/create_range_plan");
				$('#start').val(st);
				$('#end').val(en);
				$(form).submit();
//				jQuery.post("/nuts/create_range_plan", {start: st, end: en});
//				window.location.href = "/nuts/create_range_plan/" + start + "/" + end;
			}});
			$('#calendar').fullCalendar('unselect');
		},
		eventSources: [

		               // your event source
		               {
		                   url: '/nuts/view_all_mine',
		                   type: 'GET',
		                   error: function() {
		                       alert('there was an error while fetching events!');
		                   },
		               }

		               // any other sources...

		           ],
		eventClick: function(calEvent, jsEvent, view) {
		               window.location.href = "/nuts/view-plan/" + calEvent.id;
		           },
		eventMouseover: function( event, jsEvent, view ) {
			$(this).css('cursor', 'pointer');
		},
		eventResize: function(event, delta, revertFunc) {
			var s = Date.parse(event.start);
			var e = Date.parse(event.end);
			var id = event.id;
			if(event.backgroundColor == 'LightSeaGreen') {
				window.wxc.xcConfirm("Cannot change the time range of other's nut!","warning");
	            revertFunc();
				return;
			}
			var showdate = event.end.subtract(1, 'days').format();
			event.end.add(1, 'days');
			window.wxc.xcConfirm("Do you want to change your nut's end time to " + showdate + "?","confirm",{onOk:function(){
				jQuery.post("/nuts/edit-plan-time", {id: id, start: s, end: e});
			}, onCancel:function(){
				revertFunc();
			}});
	    },
		eventDrop: function(event, delta, revertFunc, jsEvent, ui, view) {

	        //alert(event.title + " was dropped on " + event.start.format());
			var s = Date.parse(event.start);
			var e = Date.parse(event.end);
			var id = event.id;
			if(event.backgroundColor == 'LightSeaGreen') {
				window.wxc.xcConfirm("Cannot change the time range of other's nut!","warning");
	            revertFunc();
				return;
			}
			var showdate = event.end.subtract(1, 'days').format();
			event.end.add(1, 'days');
			window.wxc.xcConfirm("Do you want to change your nut's time period to start from " + event.start.format() + " and end at " + showdate + "?","confirm",{onOk:function(){
				jQuery.post("/nuts/edit-plan-time", {id: id, start: s, end: e});
			}, onCancel:function(){
				revertFunc();
			}});
	    }
    })

	$('.fc-center').css('color', 'rosybrown');
    
    
});
