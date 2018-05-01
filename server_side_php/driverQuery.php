<?php //PHP file ate handles query to get result for Driver predicitons and Current Drivers
			//Using JSON_ENCODE to transmit data to
$server = "localhost";//------------update naming structure during install
$username = "root";
$password = "password";
$db = "cargo";
$conn = new mysqli($server, $username, $password, $db);
if ($conn->connect_error){
	die("connection failed: ".$conn->connect_error);
}



//-----------update nmaing structure during install
	$inactiveDrivers = "SELECT inactive_drivers FROM prediction_output WHERE DATE(date_and_time) = DATE(NOW())
							and HOUR(date_and_time) in (HOUR(current_time()))  and MINUTE(date_and_time) in (MINUTE(current_time()))
							and Second(date_and_time) in ('00') LIMIT 1";
  $totalDrivers = "SELECT total_drivers FROM prediction_output WHERE DATE(date_and_time) = DATE(NOW())
							and HOUR(date_and_time) in (HOUR(current_time()))  and MINUTE(date_and_time) in (MINUTE(current_time()) + 1)
							and Second(date_and_time) in ('00') LIMIT 1";
	$fiveMin = "SELECT five_min_drivers FROM prediction_output WHERE DATE(date_and_time) = DATE(NOW())
							and HOUR(date_and_time) in (HOUR(current_time()))  and MINUTE(date_and_time) in (MINUTE(current_time()) + 1)
							and Second(date_and_time) in ('00') LIMIT 1";
	$thirtyMin = "SELECT thirty_min_drivers FROM prediction_output WHEREDATE(date_and_time) = DATE(NOW())
							and HOUR(date_and_time) in (HOUR(current_time()))  and MINUTE(date_and_time) in (MINUTE(current_time()) + 1)
							and Second(date_and_time) in ('00') LIMIT 1";
	$result = $conn->query($inactiveDrivers);
  $result2 = $conn->query($totalDrivers);
	$result3 = $conn->query($fiveMin);
	$result4 = $conn->query($thirtyMin);


if ($result !== null && $result2!== null && $result3!== null && $result4!== null) {
	$driverArray = array($result, $result2, $result3, $result4);
	if (is_null($result)){
		$driverArray[0] = "0";
	} else {
		while($row1 = $result->fetch_assoc()){
		$driverArray[0] = ($row1['inactive_drivers']);
		}
	}
	if (is_null($result2)){
		$driverArray[1] = "0";
	} else {
		while($row2 = $result2->fetch_assoc()){
		$driverArray[1] = ($row2['total_drivers']);
		}
	}
	if (is_null($result3)){
		$driverArray[2] = "0";
	} else {
		while($row3 = $result3->fetch_assoc()){
		$driverArray[2] = ($row3['five_min_drivers']);
		}
	}
	if (is_null($result4)){
		$driverArray[3] = "0";
	} else {
		while($row4 = $result4->fetch_assoc()){
		$driverArray[3] = ($row4['thirty_min_drivers']);
		}
	}
	$data = json_encode($driverArray);
	echo $data;
} else {
	echo "No Result!";
}
?>
