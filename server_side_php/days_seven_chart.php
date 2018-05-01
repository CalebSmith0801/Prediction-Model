<?php
//carGo prediction model project, queries data from 1 week ago from current date and sends data to 
$server = "localhost";//----------update naming structure during install 
$username = "root";
$password = "password";
$db = "cargo";
$conn = new mysqli($server, $username, $password, $db);
if ($conn->connect_error){
	die("connection failed: ".$conn->connect_error);
}
//-----------update naming structure during install 
  $d1Query = "SELECT date_and_time, thirty_min_drivers, total_drivers FROM prediction_output WHERE DATE(date_and_time) = DATE(NOW() - INTERVAL 7 DAY) and
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
