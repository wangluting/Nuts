var level = [0,5,15,30,50,100,200,500,1000,2000,3000,6000,10000,18000,30000,60000,100000,300000,600000];

$(document).ready(function() {
	var point = $(".progress-bar-striped").html();
	var i=0;
	for(; i<18; i++)
		if(level[i] > point)
			break;
	$(".level").html("level " + i);
	$(".progress-bar-striped").html(point + "/" + level[i]);
	var percent = (point - level[i-1]) / (level[i] - level[i-1]) * 100;
	$(".progress-bar-striped").attr("style", "min-width: 7em; width: " + percent + "%;");
});