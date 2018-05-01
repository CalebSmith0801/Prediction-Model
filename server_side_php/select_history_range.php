<?php
$server = "localhost";  //---------------------don't forget to change sql server info to correct name/password
$username = "root";
$password = "password";
$db = "cargo";
$conn = new mysqli($server, $username, $password, $db);
if ($conn->connect_error){
	die("connection failed: ".$conn->connect_error);
}
if (isset($_GET['d'])) {
	$php_var = $_GET['d'];
	$dates = JSON_DECODE($php_var); //give you the two dates and time as array [date1, date2, hr, min]

	//----------------be sure to update column names during install
	$chartQuery = "SELECT date_and_time, thirty_min_drivers, total_drivers FROM prediction_output WHERE DATE(date_and_time) >= '$dates[0]' and DATE(date_and_time) <= '$dates[1]'
   and HOUR(date_and_time) = '$dates[2]' and MINUTE(date_and_time) = '$dates[3]'";
	$result = $conn->query($chartQuery);
	if ($result !== null){
			$data = array();
		if (is_null($result)){
			$data[] = "0";
		}
		else{
			foreach ($result as $row) {
				$data[] = $row;
			}
			echo JSON_ENCODE($data);
		}
	}
}
else
	echo "dates not set!";

?>
