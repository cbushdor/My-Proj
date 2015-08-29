#!/usr/bin/perl

$|=1;
use CGI;
use strict;
use warnings;
use POSIX qw(strftime);
use io::MyNav;
use DateTime;
use DateTime::Format::Strptime;


my $now_string = time(); # strftime "%m %d %H:%M:%S UTC %Y", gmtime;

my $doc = new CGI;
my $url=();
my $ip=io::MyNav::gets_ip_address;
my $ipAddr=io::MyNav::gets_ip_address;
my $logfile="album/hist/log-$ipAddr-$$";
my $mparam=();# my parameter passed

print "Content-type: text/html\n\n";
my $leng=scalar $doc->param;
#print "---|$leng|------". (defined($doc->param('maop_lon'))) ? "longitude defined" : "longitude not defined"  ;
print "---$leng------". $doc->param('maop_lon') ."<br>";

#my $la=$doc->param("maop_lat");
#my $lo=$doc->param("maop_lon");

foreach my $p ($doc->param){ # begin foreach my $p ($doc->param)
	print ">>>>>>>$p --->".$doc->param($p)."<br>";
	if($p=~m/^maop\_/){ # begin if($p=~m/^maop\_/)
		if($p!~m/^maop_lon$/&&
		   $p!~m/^maop_lat$/&&
		   $p!~m/^maop_prog$/&&
		   $p!~m/^maop_date$/&&
		   $p!~m/^maop_log$/){ # begin if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
			$mparam.="&$p=".$doc->param($p);
		}  # end if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
		elsif ($p!~m/^maop_lat$/){ # begin elsif ($p!~m/^maop_lat$/)
#&myrec("Case logfile format maop ","../error.html","****** $la" );
		} # end elsif ($p!~m/^maop_lat$/)
		elsif($p!~m/^maop_lon$/){ # begin elsif($p!~m/^maop_lon$/)
#&myrec("Case logfile format maop ","../error.html","****** $lo" );
		} # end elsif($p!~m/^maop_lon$/)
	} # end if($p=~m/^maop\_/)
} # end foreach my $p ($doc->param)
#&myrec("Case logfile format maop ","../error.html","logfile: $logfile *****(lo,la)=($lo,$la)" );
#print "oooooooo>$mparam<br>";

my $prog=(length($doc->param("maop_prog"))==0) ? "album.cgi" : $doc->param("maop_prog");


print "<h1>>>>>ooooooooooooooooooooo>$prog<<<<<<<<<<<<</h1><br>";

if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!){ # begin if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!)
	$url="http://localhost/~sdo/cgi-bin/$prog";
} # end if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!)
else{ # begin  else
	$url="http://derased.heliohost.org/cgi-bin/$prog";
} # end else

if( -f "$logfile"){ # begin if( -f "$logfile")
	unlink("$logfile");
	&myrec("Case logfile format maop ","../error.html","-f $logfile");
} # end if( -f "$logfile")
open(FD,">$logfile") or die("$logfile error $!");
print FD " ";
close(FD) or die("$logfile error $!");

$logfile=~s/\//\_/g;
#$logfile=~s/\_/\//g;

my $myform=<<FORM;
<!DOCTYPE html>
<html>
<body>
<p id="wait"></p>

<script>
var x=document.getElementById("wait");
x.innerHTML="Attendre svp pendant le chargement...<br><i>Please wait while loading...</i>";// + "$url?maop_lon="+lon+"&maop_lat="+lat+"$mparam&maop_date=$now_string&maop_log=$logfile";
getLocation();

function getLocation() { // begin function getLocation()
    if (navigator.geolocation) { // begin if (navigator.geolocation)
    	var options = { maximumAge: 600000, timeout: 1000000 }; 
        navigator.geolocation.watchPosition(showPosition,showError);
    } // end if (navigator.geolocation)
    else { // begin else
        x.innerHTML = "Geolocation is not supported by this browser.";
    } // end else
} // end function getLocation()

function showError(error){ // begin function showError(error)
    switch(error.code) { // begin switch(error.code)
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    } // end switch(error.code)
} // end function showError(error)

function showPosition(position) { // begin function showPosition(position)
    var lon=position.coords.longitude;
    var lat=position.coords.latitude;
    window.location="$url?maop_lon="+lon+"&maop_lat="+lat+"$mparam&maop_date=$now_string&maop_log=$logfile";
} // end function showPosition(position)
</script>
</body>
</html>
FORM

&myrec("Case 1 ","../error.html","logfile: $logfile");

sub myrec{
	my ($c,$f,$m)=@_;# $c:case name ; $f: logifile where to store stuff; $m:that's the message
	my $dt = DateTime->from_epoch( epoch => time() );# Current date format DateTime
	my $mainp=(split(/[\\\/]/,"$0"))[scalar(split(/[\\\/]/,"$0"))-1]; # gets program name

	open(W,">>$f")||die("error $!");
	print W "<pre>\n";
	print W "--------------------\n$mainp\n------------$dt---------------------\n";
	print W "$c:\n$m\n\n";
	print W "</pre><br><br>\n";
	close(W)||die("error close$!");
}

print "Content-type: text/html\n\n";
print $myform;
