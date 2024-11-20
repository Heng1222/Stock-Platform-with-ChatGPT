<?php
$command = escapeshellcmd('python ./main.py'); 
shell_exec($command); 
echo "分析完成";
?>