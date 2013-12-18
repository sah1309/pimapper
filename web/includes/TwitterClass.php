<?php
/**
 * web -- Class_Twitter.php
 * User: Simon Beattie
 * Date: 18/12/2013
 * Time: 21:38
 */

require_once(__DIR__ . '/StatusAbstract.php');

class TwitterFuncs extends StatusAbstract{

    function checkStatus(){
        $statement = $this->getPdo()->prepare("SELECT oauth_token, oauth_token_secret FROM twitter WHERE user= :user");
        $statement->execute(array(':user' => "default"));

        $twitterCreds = $statement->fetch();

        if (!$twitterCreds){

            if (empty($_SESSION['access_token']) || empty($_SESSION['access_token']['oauth_token']) || empty($_SESSION['access_token']['oauth_token_secret'])) {

                $isLoggedin['isLoggedin'] = false;
		return $isLoggedin;
            }
            else
            {
                $isLoggedin['isLoggedin'] = true;
                $isLoggedin['method'] = 'cookie';
		return $isLoggedin;
            }


        }
        else
        {
            // create twitter connection
            $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $twitterCreds['oauth_token'], $twitterCreds['oauth_token_secret']);
	    $isLoggedin['isLoggedin'] = true;
            $isLoggedin['method'] = 'db';
            $isLoggedin['connectionObj'] = $connection;
	    return $isLoggedin;
        }

    }

    function connect($type)
    {
        if ($type == 'db')
        {
            $statement = $this->getPdo()->prepare("SELECT oauth_token, oauth_token_secret FROM twitter WHERE user= :user");
            $twitterCreds = $statement->execute(array(':user' => "default"));
            $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $twitterCreds['oauth_token'], $twitterCreds['oauth_token_secret']);
            return $connection;
        }
        elseif ($type == 'cookie')
        {
            /* Create TwitteroAuth object with app key/secret and token key/secret from default phase */
            $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $_SESSION['oauth_token'], $_SESSION['oauth_token_secret']);
            return $connection;
        }
        else
        {
            return false;
        }

    }

    function checkConnection($connection)
    {
        $status = $connection->get('account/verify_credentials');
        if (array_key_exists('screen_name', $status))
        {
            $isLoggedin['isLoggedin'] = true;
            return $isLoggedin;
        }
        else
        {
            $isLoggedin['isLoggedin'] = false;
            return $isLoggedin;
        }
    }

    function getStatus($connection)
    {
        // get and return twitter status
        $status = $connection->get('account/verify_credentials');
        return $status;
    }

    function sendTweet($connection, $tweet)
    {
        $connection->post('statuses/update', array('status' => $tweet));
        return true;
    }

    function sendDM($connection, $user, $message)
    {
        $dm = $connection->post('direct_messages/new', array('user_id' => $user, 'text' => $message));
        return $dm;
    }
}
