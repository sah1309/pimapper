<?php

/*
 * POST:
 *      setname -> Sets twitter screenname to send alert DMs to
 *      getname -> Returns currently set screen name (JSON)
 *      setstatus -> Sets autoscan status (1 = on, 0 = off)
 *      cleandata -> Clear all data except last scan
 */


header('Content-Type:application/json');
session_start();

require_once(__DIR__ . '/includes/AutoScanClass.php');

$config = require(__DIR__ . '/includes/config.php');

try {
    $pdo = new PDO(
        'mysql:host=' . $config['db']['hostname'] . ';dbname=' . $config['db']['database'],
        $config['db']['username'],
        $config['db']['password']
    );
} catch (PDOException $pdoError) {
    die('Error constructing database, error was: ' . $pdoError->getMessage());

}

$autoScan = new AutoScanClass($pdo, $config);

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $checkStatus = $autoScan->checkStatus();
    if (array_key_exists('status', $checkStatus)) {
        if ($checkStatus['status'] == '1') {
            $response['autoScan'] = true;
            echo json_encode($response);
        } else {
            $response['autoScan'] = false;
            echo json_encode($response);
        }
    } else {
        $response['autoScan'] = false;
        echo json_encode($response);
    }
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (array_key_exists("option", $_POST)) {
        $option = $_POST['option'];
    } else {
        die("You must POST an option");
    }

    if (array_key_exists("message", $_POST)) {
        $message = $_POST['message'];
    } else {
        die("You must POST a message");
    }

    if ($option == 'setstatus') {
        if ($_POST['message'] == 0 | $_POST['message'] == 1) {
            $setStatus = $autoScan->setStatus($_POST['message']);
            echo $setStatus;
        } else {
            die("Invalid message");
        }

    }
    if ($option == 'setname') {
        $setStatus = $autoScan->setScreenName($_POST['message']);
        echo $setStatus;
    }
    if ($option == 'getname') {
        $response = $autoScan->getScreenName();
        echo json_encode($response);
    }

    if ($option == 'cleandata') {
        /*
         * insert function to clean out old data
         */
    }
}
