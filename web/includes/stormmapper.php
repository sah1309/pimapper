<?php

#Checks to see if stormmapper is running

if (file_exists("/var/run/stormmapper.pd"))
{
    echo " It's running!";
} else {

    echo " It's not running";
}