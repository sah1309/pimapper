<?php
header('Content-Type:application/json');

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

function sendTweet()
{
    $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $oauth_token, $oauth_token_secret);
    $connection->post('statuses/update', array('status' => $tweet));
}

function sendDM($oauth_token, $oauth_token_secret, $user, $msg)
{
    $connection = new TwitterOAuth('3EBL9R4f4H6pHOorcz96Q', '2lXeTHNPGsqXbx3QYj4NGZqFPt6AUmG9dLlQY02Tl6s', $oauth_token, $oauth_token_secret);
    $connection->post('direct_messages/new', array('user_id' => $user->id, 'text' => $msg));
}