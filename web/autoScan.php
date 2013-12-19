<?php
header('Content-Type:application/json');
session_start();

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


if ($_SERVER['REQUEST_METHOD'] == 'GET')
{
    if (empty($_SESSION['access_token']) || empty($_SESSION['access_token']['oauth_token']) || empty($_SESSION['access_token']['oauth_token_secret'])) {

        $isLoggedin['isLoggedin'] = false;
        echo json_encode($isLoggedin);
    }
    else
    {
        $isLoggedin['isLoggedin'] = true;

        echo json_encode($isLoggedin);
    }
}