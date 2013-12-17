<?php

#Checks to see if stormmapper is running

if (file_exists("/var/run/stormmapper.pid"))
{
	$is_running['isrunning'] = true;
}
 else {

        $is_running['isrunning'] = false;

}

echo json_encode($is_running);
