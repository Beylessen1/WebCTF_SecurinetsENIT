<?php

$cmd = $_GET['cmd'] ?? "";

/*
    ❌ Block direct usage of "cat"
    ✅ But allow concatenated bypass: 'c'+'a'+'t'
*/
if (preg_match('/\bcat\b/i', $cmd)) {
    die("<h3>Command contains forbidden keyword!</h3>");
}

echo "<h2>Cloning Repository...</h2>";
echo "<pre>";

system("git clone " . $cmd);

echo "</pre>";

?>

