<?php
$command = escapeshellcmd('python ./removeData.py'); 
shell_exec($command); 
header("Location:index.php")
?>