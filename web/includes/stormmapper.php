<?php
header('Content-Type:application/json');
#Checks to see if stormmapper is running

if (file_exists("/var/run/stormmapper.pid"))
{
	$is_running['isRunning'] = true;
}
 else {
    $is_running['isRunning'] = true;
}
echo json_encode($is_running);
