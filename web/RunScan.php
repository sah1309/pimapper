<?php
/**
 * web -- RunScan.php
 * User: Simon Beattie
 * Date: 19/12/2013
 * Time: 20:04
 */

require_once(__DIR__ . '/includes/RunScanClass.php');
require_once(__DIR__ . '/includes/TwitterClass.php');
require_once(__DIR__ . '/includes/AutoScanClass.php');
require_once(__DIR__ . '/includes/twitteroauth/twitteroauth.php');
require_once(__DIR__ . '/includes/twitteroauth/config.php');

//Get main config
$config = require(__DIR__ . '/includes/config.php');

//Instantiate Scanning class
$scanning = new RunScanClass($pdo, $config);

//Create temp connection object, and instantiate twitter object
$tempcon = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET);
$twitter = new TwitterFuncs($pdo, $config, $tempcon);

//Create autoScan object
$autoScan = new AutoScanClass($pdo, $config);

if ($_SERVER['REQUEST_METHOD'] == 'GET')
{
    /*
     * Insert scanner healthcheck here
     */
}

// Check Twitter authentication, and authenticate if possible
$twitter->twitterAuthFromDB('default');
if (empty($_SESSION['access_token']) || empty($_SESSION['access_token']['oauth_token']) || empty($_SESSION['access_token']['oauth_token_secret']))
{
    $twitterAuth = true;
}
else
{
    $twitterAuth = false;
}

//Check whether scan is set to run
$checkStatus = $autoScan->checkStatus();
if($checkStatus['status'] == '1')
{
    // Run full scan against current network
    $scanning->startScan('--auto');
}
else
{
    echo "autoScan not active";
}

// Run Report Generator
$report = $scanning->getReport();

// If twitter is signed in, send DM
if ($twitterAuth)
{
    $twitter->sendDM('', 'A new device has connected to your network - Please check your StormMapper!');
}