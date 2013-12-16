<?php
//database setting
$dbhost = 'localhost';
$dbuser = 'root';
$dbpassword = 'pa55word';
$database = 'pimapper';
$page = $_GET['page'];
// get the requested page
$limit = $_GET['rows'];
// get how many rows we want to have into the grid
$sidx = $_GET['sidx'];
// get index row - i.e. user click to sort
$sord = $_GET['sord']; // get the direction if(!$sidx)
$sidx = 1;
// connect to the database
$db = mysql_connect($dbhost, $dbuser, $dbpassword) or die("Connection Error: " . mysql_error());
mysql_select_db($database) or die("Error conecting to db.");
$result = mysql_query("SELECT COUNT(*) AS count FROM host_current");
$row = mysql_fetch_array($result, MYSQL_ASSOC);
$count = $row['count'];
if ($count > 0) {
    $total_pages = ceil($count / $limit);
} else {
    $total_pages = 0;
}
if ($page > $total_pages) $page = $total_pages;
$start = $limit * $page - $limit; // do not put $limit*($page - 1)
$SQL = "SELECT * FROM host_current ORDER BY $sidx $sord LIMIT $start , $limit";
$result = mysql_query($SQL) or die("Couldn t execute query." . mysql_error());

$response = new stdClass();
$response->page = $page;
$response->total = $total_pages;
$response->records = $count;
$i = 0;
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {

    $SQL2 = "SELECT os, confidence FROM os_match WHERE hostID=" . $row['id'] . " AND scantime = (SELECT max(scantime) FROM os_match WHERE hostID=" . $row['id'] . ")";;
    $result2 = mysql_query($SQL2) or die('Couldn\'t execute query. ' . mysql_error());
    while ($row2 = mysql_fetch_array($result2, MYSQL_ASSOC)) {
        $response->rows[$i]['id'] = $row['id'];
        $response->rows[$i]['cell'] = array($row['id'], $row['hostname'], $row['hostIP'], $row2['os'], $row2['confidence'], date('H:i:s Y-m-d', $row['scanTime']));
    }
    $i++;
}
echo json_encode($response);
?>
