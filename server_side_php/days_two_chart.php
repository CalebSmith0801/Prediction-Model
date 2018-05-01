<?php
//carGo prediction model project, queries and sends data to days_chart.js for 2 days prior to present day

$server = "localhost";//--------- update naming structure during install
$username = "root";
$password = "password";
$db = "cargo";
$conn = new mysqli($server, $username, $password, $db);
if ($conn->connect_error){
	die("connection failed: ".$conn->connect_error);
}

//--------- update naming structure during install
  $d2Query = "SELECT date_and_time, thirty_min_drivers, total_drivers FROM prediction_output WHERE DATE(date_and_time) = DATE(NOW() - INTERVAL 2 DAY) and
	MINUTE(date_and_time) in ('00','15','30','45')";

    $result2 = $conn->query($d2Query);


    if ($result2 !== null){
        $data2 = array();

      if (is_null($result2)){
        $data2[] = "0";
      } else{
        foreach ($result2 as $row) {
          $data2[] = $row;
        }
        echo JSON_ENCODE($data2);
      }}else{
        echo "No Result!";
      }
?>
