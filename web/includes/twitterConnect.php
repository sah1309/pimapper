<?php
/**
 * web -- TwitterConnect.php
 * User: Simon Beattie
 * Date: 18/12/2013
 * Time: 13:28
 */

/* Start session and load library. */
session_start();
require_once(__DIR__ . '/twitteroauth/twitteroauth.php');

$config = require(__DIR__ . '/config.php');

/* Build TwitterOAuth object with client credentials. */
$connection = new TwitterOAuth($config['twitter']['consumer_key'], $config['twitter']['consumer_secret']);

/* Get temporary credentials. */
$request_token = $connection->getRequestToken($config['twitter']['oauth_callback']);

/* Save temporary credentials to session. */
$_SESSION['oauth_token'] = $token = $request_token['oauth_token'];
$_SESSION['oauth_token_secret'] = $request_token['oauth_token_secret'];

/* If last connection failed don't display authorization link. */
switch ($connection->http_code) {
    case 200:
        /* Build authorize URL and redirect user to Twitter. */
        $url = $connection->getAuthorizeURL($token);
        header('Location: ' . $url);
        break;
    default:
        /* Show notification if something went wrong. */
        echo 'Could not connect to Twitter. Refresh the page or try again later.';
}