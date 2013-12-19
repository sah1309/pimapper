<?php
/**
 * web -- AutoScanClass.php
 * User: Simon Beattie
 * Date: 19/12/2013
 * Time: 09:12
 */

require_once(__DIR__ . '/ScanAbstract.php');

class AutoScanClass extends ScanAbstract{

    function checkStatus()
    {
        $statement = $this->getPdo()->prepare("SELECT status FROM auto_scan WHERE name = :name");
        $response = $statement->execute(array(':name' => "default"));

        if(!$response)
        {
            die('Sorry, we couldn\'t insert the token details: ' . $response->errorInfo()[2]);
        }

        return $response;

    }

}