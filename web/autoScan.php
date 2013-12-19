<?php
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

if ($_SERVER['REQUEST_METHOD'] == 'GET')
{

    $checkStatus = $autoScan->checkStatus();
    if($checkStatus[''])
    var_dump($checkStatus);

}