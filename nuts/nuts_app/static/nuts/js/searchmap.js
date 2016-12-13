function search_map() {
    $("#search-for-places").mapsed({
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

function needmap() {
	  document.getElementById("search-for-places").className = "maps";
	  search_map();
}