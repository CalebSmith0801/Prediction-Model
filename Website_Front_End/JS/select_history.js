function getHistory(){
	var d1 = document.getElementById('datepicker').value;
	var d2 = document.getElementById('datepicker2').value;
	var hr = document.getElementById('hours').value;
	var min = document.getElementById('minutes').value;
	var date1 = moment(d1,"MM/DD/YYYY").format("YYYY-MM-DD");
	var date2 = moment(d2,"MM/DD/YYYY").format("YYYY-MM-DD");
	
	var monthNames = [
    "Jan", "Feb", "Mar",
    "Apr", "May", "Jun", "Jul",
    "Aug", "Sep", "Oct",
    "Nov", "Dec"
	];

    if (isValidRange()){ if (d1==d2){
		var data = JSON.stringify([date1, date2]);


    	//$.post("../../server_side_php/select_history.php", data);

    	var xhr;
    	if (window.XMLHttpRequest)
    		xhr = new XMLHttpRequest(); // all browsers
    	else
    		xhr = new ActiveXObject("Microsoft.XMLHTTP") 	// for IE

    	var url = '../../server_side_php/select_history.php?d=' + data;  //----------------don't forget to change url to correct file directory
    	xhr.open('GET', url, true);
		xhr.onreadystatechange = function () {
			if (xhr.readyState===4 && xhr.status===200) {
				//console.log(xhr.responseText); //will have the php echo result
				var data = xhr.responseText.trim();
				data = json_parse(data);

		        var totalDrivers = [];
		        var thirtyMinDemand = [];
		        var time = [];
				for(var i in data) {
                    time.push(data[i].date_and_time);
                    totalDrivers.push(data[i].total_drivers);
					thirtyMinDemand.push(parseInt(data[i].thirty_min_drivers) + parseInt(data[i].total_drivers));
				}
				var chartdata = {
                    labels: time,
                    datasets: [
						{
							data: totalDrivers,
							fill: false,
							lineTension: 0.1,
							backgroundColor: "rgba(59, 89, 152, 0.75)",
							borderColor: "rgba(59, 89, 152, 1)",
							pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
							pointHoverBorderColor: "rgba(59, 89, 152, 1)",
							label: "Total Drivers"
						},

						{
							data: thirtyMinDemand,
							fill: false,
							lineTension: 0.1,
							backgroundColor: "rgba(29, 202, 255, 0.75)",
							borderColor: "rgba(29, 202, 255, 1)",
							pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
							pointHoverBorderColor: "rgba(29, 202, 255, 1)",
							label: "30 Minute Prediction"
						}
					]

				};
				
				var ChartContent = document.getElementById('select_history_chart_content');
				ChartContent.innerHTML = '<canvas id="select_history_canvas"></canvas>';

				ctx = $("#select_history_canvas").get(0).getContext("2d");        					
				var BarGraph = new Chart(ctx,{
					type: 'line',
					data: chartdata
				});
				
				var dateRange1 = new Date(d1);
				document.getElementById("selectLabel").innerHTML = monthNames[dateRange1.getMonth()] + ' ' + dateRange1.getDate() + ', ' + dateRange1.getFullYear();
			}
		}
		xhr.send();
	} 
	
	else {
		var data = JSON.stringify([date1, date2, hr, min]);


		//$.post("../../server_side_php/select_history.php", data);

		var xhr;
		if (window.XMLHttpRequest)
			xhr = new XMLHttpRequest(); // all browsers
		else
			xhr = new ActiveXObject("Microsoft.XMLHTTP") 	// for IE

		var url = '../../server_side_php/select_history_range.php?d=' + data;  //----------------don't forget to change url to correct file directory
		xhr.open('GET', url, true);
		xhr.onreadystatechange = function () {
			if (xhr.readyState===4 && xhr.status===200) {
				console.log(xhr.responseText); //will have the php echo result
				var data = JSON.parse(this.responseText);
				var totalDrivers = [];
				var thirtyMinDemand = [];
				var time = [];
				for(var i in data) {
					time.push(data[i].date_and_time);
					totalDrivers.push(data[i].total_drivers);
					thirtyMinDemand.push(parseInt(data[i].thirty_min_drivers) + parseInt(data[i].total_drivers));
				}
				var chartdata = {
					labels: time,
					datasets: [
						{
							data: totalDrivers,
							fill: false,
							lineTension: 0.1,
							backgroundColor: "rgba(59, 89, 152, 0.75)",
							borderColor: "rgba(59, 89, 152, 1)",
							pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
							pointHoverBorderColor: "rgba(59, 89, 152, 1)",
							label: "Total Drivers"
						},

						{
							data: thirtyMinDemand,
							fill: false,
							lineTension: 0.1,
							backgroundColor: "rgba(29, 202, 255, 0.75)",
							borderColor: "rgba(29, 202, 255, 1)",
							pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
							pointHoverBorderColor: "rgba(29, 202, 255, 1)",
							label: "30 Minute Prediction"
						}
					]

				};
				var ChartContent = document.getElementById('select_history_chart_content');
				ChartContent.innerHTML = '<canvas id="select_history_canvas"></canvas>';

				ctx = $("#select_history_canvas").get(0).getContext("2d");        					
				var LineGraph = new Chart(ctx,{
					type: 'bar',
					data: chartdata
				});
				
				var dateRange1 = new Date(d1);
				var dateRange2 = new Date(d2);
				document.getElementById("selectLabel").innerHTML = monthNames[dateRange1.getMonth()] + ' ' + dateRange1.getDate() + ', ' + dateRange1.getFullYear() + ' - ' + 
				monthNames[dateRange2.getMonth()] + ' ' + dateRange2.getDate() + ', ' + dateRange2.getFullYear() + ' @' + hr + ':' + min;
			}
		}
		xhr.send();
	}}	
}

function isValidRange(){
	if (d1 <= d2)
		return true;
	else
		return false;
}
