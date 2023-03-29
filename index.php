
<?php               $parametre = file_get_contents("parametres.txt");
                    $parametreaffichage = $parametre[0];
                    $parametretheme = $parametre[1];
                    $parametretaille = $parametre[2];
                    $titregreve = 0;
                    if ($parametretheme==1)
                    {
                        echo '<html class=sombre>';

                    }
                    elseif ($parametretheme==2)
                    {
                        echo '<html class=bc>';
                    }
                    elseif ($parametretheme==3)
                    {
                        echo '<html class=vw2>';
                    }
                    else
                    {
                        echo "Échec du chargement du thème!".$parametretheme."<html>";
                    }


?>

<head>
	<title> Profs absents </title>
	<meta charset = "utf-8"/>
	<link rel="stylesheet" href="style.css?<?php echo time(); ?>" />
</head>
    <body>
        
        <section class=first>
        <?php

        echo "<h1> Liste des professeurs absents aujourd'hui et à venir: </h1>";

        ?>
            <ul>
                <?php
               header("refresh: 10"); 

                date_default_timezone_set('Europe/Paris');
			    $ajd = date('d-m-Y H:i');

                    $lines = count(file("profabsents.txt"));
                    $contentsdebut=file_get_contents("datedebut.txt");
                    $linesdebut=explode("\n",$contentsdebut);

                    $contentsfin=file_get_contents("datefin.txt");
                    $linesfin=explode("\n",$contentsfin);

                    $contentsprof=file_get_contents("profabsents.txt");
                    $linesprof=explode("\n",$contentsprof);

                    $listedatesdebut = array();
                    $listedatesfin = array();
                    $listeprofspasvert = array();
                    $incr=0;
                    for($i=0; $i < $lines; $i++)
                    {
                        $incr = $i;
                        if ($parametretaille == 3){if ($incr==26){break;}}
                        $datedebut= new DateTime($linesdebut[$i]);
                        $datedebutformat = $datedebut->format('d-m-Y H:i');
                        $datefin= new DateTime($linesfin[$i]);
                        $datefinformat = $datefin->format('d-m-Y H:i');
                        if (strtotime($ajd)>strtotime($datefinformat)){
                            $fp=fopen('retirerauto.txt','a');
                            fwrite($fp,$linesprof[$i]);
                            fwrite($fp,"\n");
                            fclose($fp);
                        }
                        

                        if ( strtotime($datedebutformat) <= strtotime($ajd) and strtotime($ajd) <= strtotime($datefinformat))
                        {

                            $datedebutformat = $datedebut->format('d-m \d\e H:i');
                            $datefinformat = $datefin->format('d-m \à H:i');                                                        
                            echo '<li class="actif taille'.$parametretaille.'"><strong>'.$linesprof[$i].' du '.$datedebutformat.' au '.$datefinformat.'</strong></li>';
                        } 

                        elseif ((strtotime($datedebutformat) > strtotime($ajd)) or ( strtotime($datedebutformat) < strtotime($ajd) and strtotime($ajd) > strtotime($datefinformat)))
                        {
                            array_push($listedatesdebut, $datedebutformat);
                            array_push($listedatesfin, $datefinformat);
                            array_push($listeprofspasvert, $linesprof[$i]);
                            $datedebutformat = $datedebut->format('d-m \d\e H:i');
                            $datefinformat = $datefin->format('d-m \à H:i'); 
                        }
                        else{
                            echo "<li>Echec de l'affichage des profs absents !</li>";
                        }
                    }
                    if ($incr<26){echo "</ul></section><section class=second><ul>";}
                    
                    for($i=0; $i < sizeof($listeprofspasvert); $i++)
                    {
                    if ($parametretaille==3){if ($incr>=26){
                        break;
                        }}
                        if (strtotime($listedatesdebut[$i]) > strtotime($ajd))
                        {
                            $datedebutformat =date('d-m \d\e H:i', strtotime( $listedatesdebut[$i]));
                            $datefinformat = date('d-m \à H:i', strtotime( $listedatesfin[$i]));

                            echo '<li class="taille'.$parametretaille.'"><strong>'.$listeprofspasvert[$i].' du '.$datedebutformat.' au '.$datefinformat.'</strong></li>';
                        }
                    }

                    if ($parametretaille == 3) {
                        echo'</ul></section><aside><h1>Beaucoup de profs absents aujourd\'hui!</h1>';
                        for($i=0; $i < $lines; $i++)
                        {
                            $datedebut= new DateTime($linesdebut[$i]);
                            $datedebutformat = $datedebut->format('d-m-Y H:i');
                            $datefin= new DateTime($linesfin[$i]);
                            $datefinformat = $datefin->format('d-m-Y H:i');
    
    
                            if ( strtotime($datedebutformat) < strtotime($ajd) and strtotime($ajd) < strtotime($datefinformat))
                            {
    
                                $datedebutformat = $datedebut->format('d-m \d\e H:i');
                                $datefinformat = $datefin->format('d-m \à H:i');   
                                if ($i<$incr){
                                    continue;
                                    }                                                     
                                echo '<li class="actif taille'.$parametretaille.'"><strong>'.$linesprof[$i].' du '.$datedebutformat.' au '.$datefinformat.'</strong></li>';
                            } 
    
                            elseif ((strtotime($datedebutformat) > strtotime($ajd)) or ( strtotime($datedebutformat) < strtotime($ajd) and strtotime($ajd) > strtotime($datefinformat)))
                            {
                                array_push($listedatesdebut, $datedebutformat);
                                array_push($listedatesfin, $datefinformat);
                                array_push($listeprofspasvert, $linesprof[$i]);
                                $datedebutformat = $datedebut->format('d-m \d\e H:i');
                                $datefinformat = $datefin->format('d-m \à H:i'); 
                                if ($i<$incr){
                                    continue;
                                    }        
                            }
                        }
                        echo '<p><br><p>';
                        for($i=0; $i < sizeof($listeprofspasvert); $i++)
                        {
                            if (strtotime($listedatesdebut[$i]) > strtotime($ajd))
                            {
                                $datedebutformat =date('d-m \d\e H:i', strtotime( $listedatesdebut[$i]));
                                $datefinformat = date('d-m \à H:i', strtotime( $listedatesfin[$i]));
                                echo '<li class="taille'.$parametretaille.'"><strong>'.$listeprofspasvert[$i].' du '.$datedebutformat.' au '.$datefinformat.'</strong></li>';
                            }
                        }
                }else {
                        echo'</ul></section><aside><h1> Actualité au lycée: </h1>';
                        if ($parametreaffichage==1 or $parametreaffichage==2)
                        {
                            echo'<img src=image/image.png alt="actu">';
                        }
                        elseif ($parametreaffichage==3)
                        {
                            $fn = fopen("image/texte.txt","r");
                            echo '<p class=texte>';
                            while(! feof($fn))  {
                              $result = fgets($fn);
                              echo $result."<br>";
                            }
                          
                            fclose($fn);
                            echo '</p>';
                        }
                    }

                ?>
    </aside><img class=imagelycee src=Logo.png alt=logo>
    <p class=textebasdroite><span>Suivez le compte du CVL sur Instagram! <strong class=customcolor1> @cvl_lamer </strong> | Des suggestions pour améliorer le tableau? Envoyez-les à <strong class=customcolor1>@hatenadu33 </strong> sur Instagram! </span></p>                                             
    </body>
</html>
<!-- Site et logiciels créés par Noémie, 1GEN5 -> TGEN5

Merci à Agathe pour m'avoir aidé avec le PHP

Merci à Manon pour avoir testé le site

Merci à Emelyne, Anthony et Clara pour m'aider continuellement à améliorer le site par le biais de mises à jour

Mentions-->