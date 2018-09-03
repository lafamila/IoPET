<?php
    function query($q, $one, $json){
        $conn = mysqli_connect("localhost", "root", "123456789", "iopet");
        $result = mysqli_query($conn, $q);
        if(mysqli_num_rows($result) == 0){
            return false;
        }
        else{
            if($one){
                $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                if($json){
                    return json_encode($row);            
                }
                else{
                    return $row;
                }
            }
            else{
                $data = array();
                while($row = mysqli_fetch_array($result, MYSQLI_ASSOC)){
                    $data[] = $row;
                }
                if($json){
                    return json_encode($data);            
                }
                else{
                    return $data;
                }
            }
        }
    }
?>