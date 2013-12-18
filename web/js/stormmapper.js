/**
 * User: simonbeattie
 * Date: 18/12/2013
 * Time: 08:14
 */

function ValidateIPaddress(inputText)
{
    var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if(inputText.value.match(ipformat))
    {
        return true;
    }

    return true;

}

function processFormData()
{

    var name_element = document.getElementById('txt_name');

    var win = ValidateIPaddress(name_element.value);
    alert(win);

    if(ValidateIPaddress(name_element.value))
    {
        $.post("/includes/startScan.php",
            {
                opt:"-o" + name_element.value
            });
        isRunning();
    }
    else
    {
        alert("Invalid IP");
    }

}

