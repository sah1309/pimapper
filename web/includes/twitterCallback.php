<?php
/**
 * @file
 * Take the user when they return from Twitter. Get access tokens.
 * Verify credentials and redirect to based on response from Twitter.
 */

/* Start session and load lib */
session_start();
require_once(__DIR__ . '/twitteroauth/twitteroauth.php');
require_once(__DIR__ . '/twitteroauth/config.php');
require_once(__DIR__ . '/StatusAbstract.php');

var_dump($_SESSION);


/* If the oauth_token is old redirect to the connect page. */
if (isset($_REQUEST['oauth_token']) && $_SESSION['oauth_token'] !== $_REQUEST['oauth_token']) {
    $_SESSION['oauth_status'] = 'oldtoken';
    header('Location: ./twitterConnect.php');
}


/* Request access tokens from twitter */
$access_token = $connection->getAccessToken($_REQUEST['oauth_verifier']);

/* Save the access tokens. Normally these would be saved in a database for future use. */
$_SESSION['access_token'] = $access_token;

$tokenInsert = $pdo->prepare('INSERT INTO twitter (user, oauth_token, oauth_token_secret) VALUES(?, ?, ?)');
$insertedOk = $tokenInsert->execute(array($user, $access_token['oauth_token'], $access_token['oauth_token_secret']));

if(!$insertedOk)
{
    die('Sorry, we couldn\'t add the Twitter credentials ' . $tokenInsert->errorInfo()[2]);
}


/* Remove no longer needed request tokens */
unset($_SESSION['oauth_token']);
unset($_SESSION['oauth_token_secret']);
