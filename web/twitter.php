<?php
header('Content-Type:application/json');
session_start();

require_once(__DIR__ . '/includes/TwitterClass.php');
require_once(__DIR__ . '/includes/twitteroauth/twitteroauth.php');


$config = require(__DIR__ . '/includes/config.php');

try {
    $pdo = new PDO(
        'mysql:host=' . $config['db']['hostname'] . ';dbname=' . $config['db']['database'],
        $config['db']['username'],
        $config['db']['password']
    );
} catch (PDOException $pdoError) {
    die('Error constructing database, error was: ' . $error->getMessage());

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

if ($_SERVER['REQUEST_METHOD'] == 'POST')
{

    $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET);

    $twitterOptions = new TwitterFuncs($pdo, $config, $connection);

    // Check if a post has been sent
    if (array_key_exists("option", $_POST))
    {
        $option = $_POST['option'];
    }
    else
    {
        die("You must POST an option");
    }

    if ($option == 'info')
    {
        $status = $twitterOptions->getStatus();
        var_dump($status);
    }
    elseif ($option == 'tweet')
    {
        $status = $twitterPosts->sendTweet($connection, $_POST['message']);
        var_dump($status);
    }
    elseif ($option == 'dm')
    {
        $status = $twitterPosts->sendDM($connection, $_POST['user'], $_POST['message']);
        var_dump($status);
    }
    elseif ($option == 'logout')
    {
        session_start();
        session_destroy();
        echo "Logged out";
    }

}
