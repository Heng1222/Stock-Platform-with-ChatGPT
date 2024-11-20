<?php
$command = escapeshellcmd('python ./scraper.py'); 
shell_exec($command); 
echo "更新完成";
?>