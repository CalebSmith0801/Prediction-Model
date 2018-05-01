<?php
//carGo prediction model project, querries data from sql table and updates chart for 3 days ago from current date and sends to days_chart,js 
$server = "localhost";//---------------update naming structure for install
$username = "root";
$password = "password";
$db = "cargo";
$conn = new mysqli($server, $username, $password, $db);
if ($conn->connect_error){
	die("connection failed: ".$conn->connect_error);
}
//update naming structure for install 
  $d1Query = "SELECT date_and_time, thirty_min_drivers, total_drivers FROM prediction_output WHERE DATE(date_and_time) = DATE(NOW() - INTERVAL 3 DAY) and
	MINUTE(date_and_time) in ('00','15','30','45')";

    $result1 = $conn->query($d1Query);


    if ($result1 !== null){
        $data1 = array();

      if (is_null($result1)){
        $data1[] = "0";
      } else{
        foreach ($result1 as $row) {
          $data1[] = $row;
        }
        echo JSON_ENCODE($data1);
      }}else{
        echo "No Result!";
      }
?>
