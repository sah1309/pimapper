<?php
header('Content-Type:application/json');

session_start();
require_once(__DIR__ . '/bootstrap.php');


$statement = $pdo->prepare("SELECT oauth_token, oauth_token_secret FROM twitter WHERE user= :user");
$statement->execute(array(':user' => "default"));

$twitterCreds = $statement->fetch();


if (!$twitterCreds){

    if (empty($_SESSION['access_token']) || empty($_SESSION['access_token']['oauth_token']) || empty($_SESSION['access_token']['oauth_token_secret'])) {

        $isLoggedin['isLoggedin'] = false;
    }
    else
    {
        $isLoggedin['isLoggedin'] = true;
    }

}
else
{
    //Get details from DB
    $isLoggedin['isLoggedin'] = true;
}

echo json_encode($isLoggedin);