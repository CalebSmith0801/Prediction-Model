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
	$dates = JSON_DECODE($php_var); //give you the two dates as array [date1, date2]
	//--------------be sure to update naming structure during install to correct column names 
	$chartQuery = "SELECT date_and_time, thirty_min_drivers, total_drivers FROM prediction_output WHERE DATE(date_and_time) >= '$dates[0]' and DATE(date_and_time) <= '$dates[1]' and MINUTE(date_and_time) in ('00','15','30','45')";
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
