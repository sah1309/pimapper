/**
 * User: simonbeattie
 * Date: 18/12/2013
 * Time: 08:14
 */

function ValidateIPaddress(inputText)
{
    var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

    return inputText.match(ipformat);
}

function processFormData()
{

    var name_element = document.getElementById('txt_name');

    if(ValidateIPaddress(name_element.value))
    {
        $.post("/includes/startScan.php",
            {
                opt:"-t " + name_element.value
            });
        timeout = setTimeout(isRunning, 2000);
    }
    else
    {
        alert("Invalid IP");
    }
}

function processFormDataSN()
{
    var name_element = document.getElementById('screen_name');

        $.post("/autoScan.php",
            {
                option:"setname",
                message: name_element.value
            });

}