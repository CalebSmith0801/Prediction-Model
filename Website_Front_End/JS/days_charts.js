$(document).ready(function(){
	//javaScript code for producing seven charts on history.html
	//yesterday
	var monthNames = [
    "Jan", "Feb", "Mar",
    "Apr", "May", "Jun", "Jul",
    "Aug", "Sep", "Oct",
    "Nov", "Dec"
  ];

$.ajax({
          url: "../../server_side_php/days_chart.php",
          method: "GET",
          success: function(data1){
                 
									data1 = data1.trim();
                  data1 = json_parse(data1);

                  var totalDrivers = [];
                  var thirtyMinDemand = [];
                  var time = [];

                  for(var i in data1) {
                            time.push(data1[i].date_and_time);
                            totalDrivers.push(data1[i].total_drivers);
                            thirtyMinDemand.push(parseInt(data1[i].thirty_min_drivers) + parseInt(data1[i].total_drivers));

                          }

                  var chartdata = {
                    labels: time,
                    datasets: [
                      {
                          data: totalDrivers,
                          fill: false,
                          lineTension: 0.1,
                          backgroundColor: "#4DA430",
                          borderColor: "#4DA430",
                          pointHoverBackgroundColor: "#4DA430",
                          pointHoverBorderColor: "#4DA430",
                          label: "Total Drivers"
                    },

                    {
                          data: thirtyMinDemand,
                          fill: false,
                          lineTension: 0.1,
                          backgroundColor: "#FEEA0D",
                          borderColor: "#FEEA0D",
                          pointHoverBackgroundColor: "#FEEA0D",
                          pointHoverBorderColor: "#FEEA0D",
                          label: "30 Minute Prediction"
                    }
                  ]

                };

                var x = $("#d1Chart");
				var chartDate = new Date(time[0]);
				
				document.getElementById("d1Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

                var LineGraph = new Chart(x,{
                  type: 'line',
                  data: chartdata
                });
              },
                error : function(data) {}
              });
//day before yesterday (2days ago)

$.ajax({
        url: "../../server_side_php/days_two_chart.php",
        method: "GET",
        success: function(data2){
                data2 = json_parse(data2);

                var totalDrivers = [];
                var thirtyMinDemand = [];
                var time = [];

                for(var i in data2) {
                          time.push(data2[i].date_and_time);
                          totalDrivers.push(data2[i].total_drivers);
                          thirtyMinDemand.push(parseInt(data2[i].thirty_min_drivers) + parseInt(data2[i].total_drivers));

                        }

                var chartdata = {
                  labels: time,
                  datasets: [
                    {
                        data: totalDrivers,
                        fill: false,
                        lineTension: 0.1,
                        backgroundColor: "#FE0D69",
                        borderColor: "#FE0D69",
                        pointHoverBackgroundColor: "#FE0D69",
                        pointHoverBorderColor: "#FE0D69",
                        label: "Total Drivers"
                  },

                  {
                        data: thirtyMinDemand,
                        fill: false,
                        lineTension: 0.1,
                        backgroundColor: "#D20DFE",
                        borderColor: "#D20DFE",
                        pointHoverBackgroundColor: "#D20DFE",
                        pointHoverBorderColor: "#D20DFE",
                        label: "30 Minute Prediction"
                  }
                ]

              };

              var x2 = $("#d2Chart");
			  var chartDate = new Date(time[0]);
				
				document.getElementById("d2Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

              var LineGraph = new Chart(x2,{
                type: 'line',
                data: chartdata
              });
            },
              error : function(data) {}
            });
//3days ago
$.ajax({
				url: "../../server_side_php/days_three_chart.php",
				method: "GET",
				success: function(data3){
								
								data3 = json_parse(data3);

								var totalDrivers = [];
								var thirtyMinDemand = [];
								var time = [];

								for(var i in data3) {
													time.push(data3[i].date_and_time);
													totalDrivers.push(data3[i].total_drivers);
													thirtyMinDemand.push(parseInt(data3[i].thirty_min_drivers) + parseInt(data3[i].total_drivers));

												}

								var chartdata = {
									labels: time,
									datasets: [
										{
												data: totalDrivers,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#0DF9FE",
												borderColor: "#0DF9FE",
												pointHoverBackgroundColor: "#0DF9FE",
												pointHoverBorderColor: "#0DF9FE",
												label: "Total Drivers"
									},

									{
												data: thirtyMinDemand,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#61FE0D",
												borderColor: "#61FE0D",
												pointHoverBackgroundColor: "#61FE0D",
												pointHoverBorderColor: "#61FE0D",
												label: "30 Minute Prediction"
									}
								]

							};

							var z = $("#d3Chart");
							var chartDate = new Date(time[0]);
							
							document.getElementById("d3Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

							var LineGraph = new Chart(z,{
								type: 'line',
								data: chartdata
							});
						},
							error : function(data) {}
						});
//4days ago
$.ajax({
				url: "../../server_side_php/days_four_chart.php",
				method: "GET",
				success: function(data4){
								
								data4 = json_parse(data4);

								var totalDrivers = [];
								var thirtyMinDemand = [];
								var time = [];

								for(var i in data4) {
													time.push(data4[i].date_and_time);
													totalDrivers.push(data4[i].total_drivers);
													thirtyMinDemand.push(parseInt(data4[i].thirty_min_drivers) + parseInt(data4[i].total_drivers));

												}

								var chartdata = {
									labels: time,
									datasets: [
										{
												data: totalDrivers,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#B53431",
												borderColor: "#B53431",
												pointHoverBackgroundColor: "#B53431",
												pointHoverBorderColor: "#B53431",
												label: "Total Drivers"
									},

									{
												data: thirtyMinDemand,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#D076DC",
												borderColor: "#D076DC",
												pointHoverBackgroundColor: "#D076DC",
												pointHoverBorderColor: "#D076DC",
												label: "30 Minute Prediction"
									}
								]

							};

							var x = $("#d4Chart");
							var chartDate = new Date(time[0]);
							
							document.getElementById("d4Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

							var LineGraph = new Chart(x,{
								type: 'line',
								data: chartdata
							});
						},
							error : function(data) {}
						});
//5days ago
$.ajax({
				url: "../../server_side_php/days_five_chart.php",
				method: "GET",
				success: function(data5){
								
								data5 = json_parse(data5);

								var totalDrivers = [];
								var thirtyMinDemand = [];
								var time = [];

								for(var i in data5) {
													time.push(data5[i].date_and_time);
													totalDrivers.push(data5[i].total_drivers);
													thirtyMinDemand.push(parseInt(data5[i].thirty_min_drivers) + parseInt(data5[i].total_drivers));

												}

								var chartdata = {
									labels: time,
									datasets: [
										{
												data: totalDrivers,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#23A232",
												borderColor: "#23A232",
												pointHoverBackgroundColor: "#23A232",
												pointHoverBorderColor: "#23A232",
												label: "Total Drivers"
									},

									{
												data: thirtyMinDemand,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#FCDE2C",
												borderColor: "#FCDE2C",
												pointHoverBackgroundColor: "#FCDE2C",
												pointHoverBorderColor: "#FCDE2C",
												label: "30 Minute Prediction"
									}
								]

							};

							var x = $("#d5Chart");
							var chartDate = new Date(time[0]);
							
							document.getElementById("d5Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

							var LineGraph = new Chart(x,{
								type: 'line',
								data: chartdata
							});
						},
							error : function(data) {}
						});
//6days ago
$.ajax({
				url: "../../server_side_php/days_six_chart.php",
				method: "GET",
				success: function(data6){
								
								data6 = json_parse(data6);

								var totalDrivers = [];
								var thirtyMinDemand = [];
								var time = [];

								for(var i in data6) {
													time.push(data6[i].date_and_time);
													totalDrivers.push(data6[i].total_drivers);
													thirtyMinDemand.push(parseInt(data6[i].thirty_min_drivers) + parseInt(data6[i].total_drivers));

												}

								var chartdata = {
									labels: time,
									datasets: [
										{
												data: totalDrivers,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#1B17EB",
												borderColor: "#1B17EB",
												pointHoverBackgroundColor: "#1B17EB",
												pointHoverBorderColor: "#1B17EB",
												label: "Total Drivers"
									},

									{
												data: thirtyMinDemand,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#63F5FE",
												borderColor: "#63F5FE",
												pointHoverBackgroundColor: "#63F5FE",
												pointHoverBorderColor: "#63F5FE",
												label: "30 Minute Prediction"
									}
								]

							};

							var x = $("#d6Chart");
							var chartDate = new Date(time[0]);
							
							document.getElementById("d6Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

							var LineGraph = new Chart(x,{
								type: 'line',
								data: chartdata
							});
						},
							error : function(data) {}
						});
//seven days ago
$.ajax({
				url: "../../server_side_php/days_seven_chart.php",
				method: "GET",
				success: function(data7){
								
								data7 = json_parse(data7);

								var totalDrivers = [];
								var thirtyMinDemand = [];
								var time = [];

								for(var i in data7) {
													time.push(data7[i].date_and_time);
													totalDrivers.push(data7[i].total_drivers);
													thirtyMinDemand.push(parseInt(data7[i].thirty_min_drivers) + parseInt(data7[i].total_drivers));

												}

								var chartdata = {
									labels: time,
									datasets: [
										{
												data: totalDrivers,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#51FEFB",
												borderColor: "#51FEFB",
												pointHoverBackgroundColor: "#51FEFB",
												pointHoverBorderColor: "#51FEFB",
												label: "Total Drivers"
									},

									{
												data: thirtyMinDemand,
												fill: false,
												lineTension: 0.1,
												backgroundColor: "#6A0073",
												borderColor: "#6A0073",
												pointHoverBackgroundColor: "#6A0073",
												pointHoverBorderColor: "#6A0073",
												label: "30 Minute Prediction"
									}
								]

							};

							var x = $("#d7Chart");
							var chartDate = new Date(time[0]);
							
							document.getElementById("d7Label").innerHTML = monthNames[chartDate.getMonth()] + ' ' + chartDate.getDate() + ', ' + chartDate.getFullYear();

							var LineGraph = new Chart(x,{
								type: 'line',
								data: chartdata
							});
						},
							error : function(data) {}
						});
					})
