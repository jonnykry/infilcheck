var hide =0;
document.getElementById("change").style.visibility = "hidden";

if (document.getElementById("en").innerHTML == "Pi is Enabled: True")
{
document.getElementById("Toggle Pi").style.background = '#4CAF50';
}
else
{
document.getElementById("Toggle Pi").style.background = '#f44336';
}



function showForm()
{
if (hide ==0)
    {
    document.getElementById("change").style.visibility = "visible";
    hide =1;
    }
else
    {
    document.getElementById("change").style.visibility = "hidden";
    hide =0;
    }


}
function fill_default()
{
document.getElementById("room_name").value = "Room";
document.getElementById("capture_framerate").value = 32;
document.getElementById("output_framerate").value = 10;
document.getElementById("threshold_frame_count").value = 5;
}
