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
require_once(__DIR__ . '/TwitterClass.php');

$config = require(__DIR__ . '/config.php');

try {
    $pdo = new PDO(
        'mysql:host=' . $config['db']['hostname'] . ';dbname=' . $config['db']['database'],
        $config['db']['username'],
        $config['db']['password']
    );
} catch (PDOException $pdoError)
{
    die('Error constructing database, error was: ' . $pdoError->getMessage());
}

/* Create TwitteroAuth object with app key/secret and token key/secret from default phase */
$connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $_SESSION['oauth_token'], $_SESSION['oauth_token_secret']);

/* Request access tokens from twitter */
$access_token = $connection->getAccessToken($_REQUEST['oauth_verifier']);

/* Save the access tokens. Normally these would be saved in a database for future use. */
$_SESSION['access_token'] = $access_token;

$twitterCallback = new TwitterFuncs($pdo, $config, $connection);

$status = $this->getOauth()->get('account/verify_credentials');
print_r($status);
die();

//$twitterCallback->saveAuth($access_token);

/* Remove no longer needed request tokens */
unset($_SESSION['oauth_token']);
unset($_SESSION['oauth_token_secret']);

header('Location: ../index.html');