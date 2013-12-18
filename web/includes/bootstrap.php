<?php
/**
 * web -- bootstrap.php
 * User: Simon Beattie
 * Date: 18/12/2013
 * Time: 16:51
 */

require_once(__DIR__ . '/../conf/stormmapper.conf.php');

try
{
    $pdo = new PDO('mysql:hostname=' . $dbhost . ';dbname=' . $database, $dbuser , $dbpassword);
} catch(PDOException $error)
{
    die('Error constructing database, error was: ' . $error->getMessage());
}