function getChart(){$(document).ready(function(){
	$.ajax({
          url: "../../server_side_php/home_chart.php",
          method: "GET",
          success: function(data){
                  console.log(data);
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

                var x = $("#todaysChart");

                var LineGraph = new Chart(x,{
                  type: 'line',
                  data: chartdata
                });
              },
                error : function(data) {}
              });
            })
}
