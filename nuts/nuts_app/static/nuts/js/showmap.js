function show_map() {
	lat = 0.0;
	lng = 0.0;
	if (document.getElementById("lat").value != null) {
		lat = document.getElementById("lat").value;
	}
	if (document.getElementById("lng").value != null) {
		lng = document.getElementById("lng").value;
	}


    $("#show-places").mapsed({


		showOnLoad:
		[
			{
				//autoShow: true,
				canEdit: false,

				lat: lat,
				lng: lng,
			}

		]

	});

}

$(document).ready(function() {
        show_map();
});