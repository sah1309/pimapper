<?php
header('Content-Type:application/json');


session_start();
require_once(__DIR__ . '/twitteroauth/config.php');
require_once(__DIR__ . '/twitteroauth/twitteroauth.php');


if (array_key_exists("option", $_POST))
{
    $option = $_POST['option'];
}
else
{
    die("You must POST an option");
}

if (array_key_exists("message", $_POST))
{
    $message = $_POST['message'];
}
else
{
    die("You must POST a message");
}




if ($option == 'tweet')
{
    echo "Tweeeeeeeeeeting";
    sendTweet($message);
}

if ($option == 'logout')
{
    echo "Logging out";
    logout();
}

if ($option == 'info')
{
    getTwitter();
}

function getTwitter()
{
    $access_token = $_SESSION['access_token'];
    $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $access_token['oauth_token'], $access_token['oauth_token_secret']);
    $content = $connection->get('account/verify_credentials');

    print_r($content);
}

function sendTweet($message)
{

    $access_token = $_SESSION['access_token'];
    $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $access_token['oauth_token'], $access_token['oauth_token_secret']);

    $connection->post('statuses/update', array('status' => $message));

}

function sendDM($oauth_token, $oauth_token_secret, $user, $msg)
{
    $connection = new TwitterOAuth('3EBL9R4f4H6pHOorcz96Q', '2lXeTHNPGsqXbx3QYj4NGZqFPt6AUmG9dLlQY02Tl6s', $oauth_token, $oauth_token_secret);
    $connection->post('direct_messages/new', array('user_id' => $user->id, 'text' => $msg));
}

function logout()
{

session_start();
session_destroy();

}