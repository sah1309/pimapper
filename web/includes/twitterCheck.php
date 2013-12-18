<?php
header('Content-Type:application/json');

session_start();
require_once(__DIR__ . 'bootstrap.php');

$checkLogin = $pdo->query("SELECT oauth_token, oauth_token_secret FROM twitter WHERE user = " . $user . ";");
$twitterCreds = $checkLogin->fetchAll(PDO::FETCH_ASSOC);

print_r($checkLogin);

if (empty($_SESSION['access_token']) || empty($_SESSION['access_token']['oauth_token']) || empty($_SESSION['access_token']['oauth_token_secret'])) {
    $isLoggedin['isLoggedin'] = false;
}
else
{
    $isLoggedin['isLoggedin'] = true;
}

echo json_encode($isLoggedin);


