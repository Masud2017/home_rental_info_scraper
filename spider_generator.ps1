$map = @{
    'antares' = 'https://wonen.thuisbijantares.nl/aanbod/nu-te-huur/te-huur/details/'
    'dewoningzoeker' = 'https://www.dewoningzoeker.nl/aanbod/te-huur/details/'
    'frieslandhuurt' = 'https://www.frieslandhuurt.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'hollandrijnland' = 'https://www.hureninhollandrijnland.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'hwwonen' = 'https://www.thuisbijhwwonen.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'klikvoorwonen' = 'https://www.klikvoorwonen.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'mercatus-aanbod' = 'https://woningaanbod.mercatus.nl/aanbod/te-huur/details/'
    'mosaic-plaza' = 'https://plaza.newnewnew.space/aanbod/huurwoningen/details/'
    'noordveluwe' = 'https://www.hurennoordveluwe.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'oostwestwonen' = 'https://woningzoeken.oostwestwonen.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'studentenenschede' = 'https://www.roomspot.nl/aanbod/te-huur/details/'
    'svnk' = 'https://www.svnk.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'thuisindeachterhoek' = 'https://www.thuisindeachterhoek.nl/aanbod/te-huur/details/'
    'thuisinlimburg' = 'https://www.thuisinlimburg.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'thuiskompas' = 'https://www.thuiskompas.nl/aanbod/nu-te-huur/te-huur/details/'
    'thuispoort' = 'https://www.thuispoort.nl/aanbod/te-huur/details/'
    'thuispoortstudenten' = 'https://www.thuispoortstudentenwoningen.nl/aanbod/details/'
    'woninghuren' = 'https://www.woninghuren.nl/aanbod/te-huur/details/'
    'woninginzicht' = 'https://www.woninginzicht.nl/aanbod/te-huur/details/'
    'wooniezie' = 'https://www.wooniezie.nl/aanbod/nu-te-huur/te-huur/details/'
    'woonkeusstedendriehoek' = 'https://www.woonkeus-stedendriehoek.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'woonnethaaglanden' = 'https://www.woonnet-haaglanden.nl/aanbod/nu-te-huur/te-huur/details/'
    'woontij' = 'https://www.wonenindekop.nl/aanbod/nu-te-huur/huurwoningen/details/'
    'zuidwestwonen' = 'https://www.zuidwestwonen.nl/aanbod/nu-te-huur/huurwoningen/details/'
}

foreach ($key in $map.Keys) {
    $url = $map[$key]
    Write-Output "Generating spider for $key with URL $url"
    python -m scrapy genspider $key $url
}
