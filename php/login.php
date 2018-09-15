<?php
    include_once('config.php');
    $user_id = $_POST['username'];
    $user_pw = $_POST['password'];
    $query = "SELECT * FROM `hospital` WHERE `HOSPITAL_USER_ID` = '$user_id' AND `HOSPITAL_USER_PW` = '$user_pw'";
    $data = query($query, true, false);
    if($data != false){
        session_start();
        $_SESSION['hospital_id'] = $data["HOSPITAL_ID"];
        print "true";
    }
    else{
        print "false";
    }
?>