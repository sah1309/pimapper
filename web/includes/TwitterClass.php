<?php
/**
 * web -- Class_Twitter.php
 * User: Simon Beattie
 * Date: 18/12/2013
 * Time: 21:38
 */

require_once(__DIR__ . '/StatusAbstract.php');

class TwitterFuncs extends StatusAbstract{

    function checkTwitterAuth()
    {

            $statement = $this->getPdo()->prepare("SELECT id FROM twitter WHERE user = :user");
            $statement->execute(array(':user' => "default"));
            $response = $statement->fetch();

            return $response;
    }

    function TwitterAuthFromDB($id)
    {
        $statement = $this->getPdo()->prepare("SELECT oauth_token, oauth_token_secret, user_id, screen_name FROM twitter WHERE id = :id");
        $statement->execute(array(':id' => $id));
        $response = $statement->fetch();

        return $response;
    }

    function DeleteTwitterAuth($id)
    {
        $statement = $this->getPdo()->prepare("DELETE FROM twitter WHERE id = :id");
        $statement->execute(array(':id' => $id));
        $response = $statement->fetch();

        return $response;
    }

    function saveAuth($accessToken)
    {

        $statement = $this->getPdo()->prepare("INSERT INTO twitter (user, oauth_token, oauth_token_secret, user_id, screen_name) VALUES ( ?, ?, ?, ?, ? )");
        $insertedOk = $statement->execute(array('default', $accessToken['oauth_token'], $accessToken['oauth_token_secret'], $accessToken['user_id'], $accessToken['screen_name']));

        if(!$insertedOk)
        {
            die('Sorry, we couldn\'t insert the token details: ' . $statement->errorInfo()[2]);
        }
    }

    function getStatus()
    {
        // get and return twitter status
        $status = $this->getOauth()->get('account/verify_credentials');
        return $status;
    }

    function sendTweet($tweet)
    {
        $tweetSend = $this->getOauth()->post('statuses/update', array('status' => $tweet));
        return $tweetSend;
    }

    function sendDM($user, $message)
    {
        $dm = $this->getOauth()->post('direct_messages/new', array('screen_name' => $user, 'text' => $message));
        return $dm;
    }
}
