<?php
/**
 * web -- startScan.php
 * User: Simon Beattie
 * Date: 17/12/2013
 * Time: 15:01
 */


$options = $_POST['opt'];

$command = '/usr/bin/stormmapper.py';

$line = $command . ' ' . $options . '&';

exec($line, $returnedOutput, $returnCode);


/**
var_dump($returnedOutput);

var_dump($returnCode);



$descriptors = array(
    0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
    1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
    2 => array("pipe", "w") // stderr is a file to write to
);

$cwd = '/tmp';

$process = proc_open($command, $descriptors, $pipes, $cwd);

ob_end_flush();

if (is_resource($process)) {
    // $pipes now looks like this:
    // 0 => writeable handle connected to child stdin
    // 1 => readable handle connected to child stdout
    // Any error output will be appended to /tmp/error-output.txt

    while(!feof($pipes[1]))
    {
        echo fread($pipes[1], 1024);
    }
}

 **/