<?php

$config = require(__DIR__ . '/config.php');

$examp = $_GET["q"]; //query number

$id = $_GET['id'];

// connect to the database
$db = mysql_connect($config['db']['hostname'], $config['db']['username'], $config['db']['password'])
or die("Connection Error: " . mysql_error());

mysql_select_db($config['db']['database']) or die("Error conecting to db.");
$SQL = "SELECT portID, scanTime FROM services WHERE hostID=" . $id . " and scantime = (select max(scantime) from services where hostID=" . $id . ")";
$SQL = "SELECT services.portID, ports.service, ports.description, services.scanTime FROM services RIGHT JOIN ports ON ports.port=services.portID AND protocol='tcp' WHERE services.hostID=" . $id . " AND services.scantime = (select max(scantime) from services where hostID=" . $id . ") GROUP BY portID;";

$result = mysql_query($SQL) or die("Couldnt execute query." . mysql_error());

$response = new stdClass();
$i = 0;
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
    $response->rows[$i]['cell'] = array($row['portID'], $row['service'], $row['description'], date('H:i:s Y-m-d', $row['scanTime']));
    $i++;
}
echo json_encode($response);
