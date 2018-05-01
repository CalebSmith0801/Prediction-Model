<?php //PHP file ate handles query to get result for Driver predicitons and Current Drivers updates home_chart.js
			//Using JSON_ENCODE to transmit data to javascript file


$server = "localhost";//----------update naming structure during install
$username = "root";
$password = "password";
$db = "cargo";
$conn = new mysqli($server, $username, $password, $db);
if ($conn->connect_error){
	die("connection failed: ".$conn->connect_error);
}
//-----------update naming structure during install
$chartQuery = "SELECT date_and_time, total_drivers, thirty_min_drivers FROM prediction_output where DATE(date_and_time) = DATE(NOW()) and MINUTE(date_and_time) in ('00','15','30','45') ";
$result = $conn->query($chartQuery);
if ($result !== null){
		$data = array();
	if (is_null($result)){
		$data[] = "0";
	} else{
		foreach ($result as $row) {
			$data[] = $row;
		}
		echo JSON_ENCODE($data);
	}}else{
		echo "No Result!";
	}
?>
