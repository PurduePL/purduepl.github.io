function show(n) {
	var style = document.getElementById("seminar-schedule-old").style.display;
	if (style == "none"){
		document.getElementById("seminar-schedule-old").style.display = "table";
		document.getElementById("table-collapse-img").src = "assets/minimize.png";
	} else{
		document.getElementById("seminar-schedule-old").style.display = "none";
		document.getElementById("table-collapse-img").src = "assets/maximize.png";
	}
}
