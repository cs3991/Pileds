
<!DOCTYPE html>
<html lang="fr" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Rapberry dashboard</title>
  </head>
  <body><p>
    <?php
    $command = escapeshellcmd('/usr/bin/python3 /home/pi/Scripts/python/DataProcessing.py');
    $output = shell_exec($command);

    if($output == null) {
      echo "erreur";
    }
    ?>


    <img src="last24h.svg"></p>
<p>   <?php echo $output;?> </p>
  </body>
</html>

