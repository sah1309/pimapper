<?php

session_start();

if (empty($_SESSION['access_token']) || empty($_SESSION['access_token']['oauth_token']) || empty($_SESSION['access_token']['oauth_token_secret'])) {
$isLoggedin['isLoggedin'] = false;
}
else
{
$isLoggedin['isLoggedin'] = true;
}

echo json_encode($isLoggedin);


