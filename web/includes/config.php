<?php
/**
 * web -- config.php
 * User: Simon Beattie
 * Date: 18/12/2013
 * Time: 21:48
 */

return array(
    'db'      =>
    array(
        'hostname' => 'localhost',
        'username' => 'root',
        'database' => 'pimapper',
        'password' => 'pa55word',
    ),
    'user'    =>
    array(
        'user' => 'default',
    ),
    'twitter' =>
    array(
        'consumer_key'    => 'PkCCwJcKHXvDgY8W3gjAcQ',
        'consumer_secret' => 'cS9NkbLQfnhylG6PSeLT7gfjSI8u5LsANBNPeK8dkk',
        'oauth_callback'  => '/includes/TwitterCallback.php',
    )
);

?>