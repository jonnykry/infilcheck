var hide =0;
$("#change").hide();
function showForm()
{
if (hide ==0)
    {
    $("#change").show();
    hide =1;
    }
else
    {
    $("#change").hide();
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
