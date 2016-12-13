function edit_map() {
    $("#edit-places").mapsed({

		showOnLoad:
		[
			{
				//autoShow: true,
				canEdit: true,

				lat: document.getElementById("lat").value,
				lng: document.getElementById("lng").value,
			}

		],

        searchOptions: {
			enabled: true,
		},

		//findGeoOnLoad: true,

		onSelect: function(m, details) {
			/*
            var msg =
				"name: " + details.name +
				"<br/>street: " + details.street + ", " +
					details.area + ", " +
					details.town + ", " + details.postCode +
				"<br/>telNo: " + details.telNo +
				"<br/>website: " + details.website +
				"<br/>g+: " + details.url
			;
			m.showMsg("You selected ...", msg);
			*/
            document.getElementById("lat").value = details.lat;
            document.getElementById("lng").value = details.lng;
			return true;
		},

	});

}

$(document).ready(function() {
        edit_map();
});
