function getDrivers(){
console.log("hello");
  var xmlhttp = new XMLHttpRequest();

  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.status);
        var myObj = JSON.parse(this.responseText);
        document.getElementById("driversAvailable").innerHTML = myObj[0];
        document.getElementById("totalDrivers").innerHTML = myObj[1];
        document.getElementById("5Min").innerHTML = myObj[2];
        document.getElementById("30Min").innerHTML = myObj[3];

    }
};
xmlhttp.open("GET", "../../server_side_php/driverQuery.php", true);
xmlhttp.send();
}

window.onload = getDrivers;
