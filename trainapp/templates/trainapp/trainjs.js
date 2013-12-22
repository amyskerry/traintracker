
function validate(myform){
    if (!checkRadioArray(myform.response)) {alert('Please enter your rating!');return false;}
    return true;
}
function checkRadioArray(radioButtons){
    for (var i=0; i< radioButtons.length; i++) {
        if (radioButtons[i].checked) return true;
    }
    return false;
}

<script type="text/javascript">
function getnextstep(myform){
    var chosen=document.getElementById("choice").value
    document.getElementById(newurltail).value=chosen
}
<script>

<script>
function savetempuser(userid) {
        {% user=request.POST['green']            
        datevar=datetime.datetime.now()
        date=datevar.strftime("%Y-%m-%d %H:%M")
        p=TempVals(USERID=user, DATE=date)
        p.save() %}
    }
</script>