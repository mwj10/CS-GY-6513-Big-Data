var checkForm = function(form) { 
/* Submit button was clicked */
//
// check form input values
//
    form.submit.disabled = true;
    form.submit.value = "Please wait...";
    return true;
};



function loading(){
    document.getElementById("loading").style.display = "block"
    document.getElementById("main_content").style.display = "none"
    // $("#loading").show();
    // $("#content").hide();       
}
