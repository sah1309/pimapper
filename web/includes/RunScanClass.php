<?php
/**
 * web -- RunScanClass.php
 * User: Simon Beattie
 * Date: 19/12/2013
 * Time: 20:04
 */

require_once(__DIR__ . '/ScanAbstract.php');

class RunScanClass extends ScanAbstract {

    function startScan($options)
    {
        exec( "sudo /usr/bin/stormmapper/stormmapper.py " . $options . " > /var/log/stormmapper_scan.log &");
    }

    function scanActive()
    {

    }

    function getReport()
    {
        /*
         * Add report functionality
         * Report on any new MAC addresses added since last scan
         */
        return true;
    }
}