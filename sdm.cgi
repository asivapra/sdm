#!/usr/local/bin/perl
#-----------------------------
# Created on 02 April 2016
# Copyright 2016 AV Sivaprasad - 4
#-----------------------------
use URI::Escape;
use DBI;
#use Cpanel::JSON::XS qw(encode_json decode_json);
use IP::Country::Fast;
use LWP::Simple;
use LWP::UserAgent;
my $browser = LWP::UserAgent->new;
$browser->agent("MyApp/0.1 ");
$browser->timeout( 15 );
use feature 'say';
use Geo::IP;
sub numerically { $a <=> $b }
sub Monify
{
   $in = $_[0];
   $in = sprintf "%.2f", $in;
   return $in;
}
sub LWP_CAPTCHA
{
	my $Url = $_[0];
	$private_key = "6LdDkfwSAAAAAHKfEf9tnFGKmW52H3CiUXKrXDFd"; # working with 'webgenie.com'
#	$private_key = "6LeTkfwSAAAAAPIzVEwXjDAOcCsWO5Yk6Mnsw7qv"; 
	
#&debug("remoteip = $remoteHostID; privatekey = $private_key");	
	my $response = $browser->post(
	  $Url,
	  [
		'privatekey'  => "$private_key",
		'remoteip'  => $remoteHostID,
		'challenge'  => $recaptcha_challenge_field,
		'response' => $recaptcha_response_field,
	  ],
	);
	my $message = $response->message;
	my $result = $response->content;
	return $result;
}
sub LWPMethod
{
	my $Url = $_[0];
	my $response = $browser->get(
	  $Url,
	  [
	  ],
	);
	my $message = $response->message;
	my $result = $response->content;
	return $result;
}
sub debug
{
  $line = $_[0];
  $exit = $_[1];
  if (!$headerAdded) { print "Content-type: text/html\n\n"; $headerAdded = 1; }
  print "$line<br>\n";
  if ($exit) { exit; }
}
sub debugEnv
{
   print "Content-type:text/html\n\n";
   print "<Pre>\n";
   foreach $item (%ENV)
   {
      print "$item\n";
   }
   exit;
}
sub reformat
{
  local($tmp) = $_[0] ;
  $tmp =~ s/\+/ /g ;
  while ($tmp =~ /%([0-9A-Fa-f][0-9A-Fa-f])/)
  {
   $num = $1;
   $dec = hex($num);
   $chr = pack("c",$dec);
   $chr =~ s/&/^/g;  # Replace if it is the & char.
   $tmp =~ s/%$num/$chr/g;
  }
  return($tmp);
}
sub ConnectToDBase
{
	$driver = "mysql";
	$hostname = "localhost";
	$database = "sdm"; 
	$dbuser="avs";
	$dbpassword="2Kenooch";
	$dsn = "DBI:$driver:database=$database;host=$hostname";
	$dbh = DBI->connect($dsn, $dbuser, $dbpassword);
	$drh = DBI->install_driver("mysql");
}
sub execute_query
{
	$sth=$dbh->prepare($query);
	$rv = $sth->execute or die "can't execute the query:" . $sth->errstr;
}

sub Fetchrow_array
{
   $tablerows = $_[0];
   my @results = ();
   while(@entries = $sth->fetchrow_array)
   {
	   for ($jj=0; $jj < $tablerows; $jj++)
	   {
		   push (@results, $entries[$jj]);
	   }
   }
   my $numreturned = scalar(@results)/$tablerows;
   return @results;
}
sub Get_fields
{
#&debug("OK = @_");		
#	while ($var = shift)
	foreach $var(@_)
	{
	   my @fields = split (/=/, $var);
	   $var = $fields[0];
	   if ($pquery =~ /$var\d*=([^&]*)&/i)
	   {
		$$var = $1;
		if ($var eq "g-recaptcha-response") { $g_recaptcha_response = $1; }
	   }
	}
}
sub Print_fields
{
	while ($var = shift)
	{
	   my @fields = split (/=/, $var);
	   $var = $fields[0];
	   if ($pquery =~ /$var\d*=([^&]*)&/i)
	   {
		$$var = $1;
		if ($var eq "g-recaptcha-response") 
		{ 
			$g_recaptcha_response = $1; 
		}
		if ($var =~ /g-recaptcha-response/) { next; }
		if ($var =~ /sc_action/) { next; }
		if ($var =~ /Subject/) { next; }
		$content .= "<tr><td>$var</td><td>" . $$var . "</td></tr>\n";		
	   }
	}
}
sub SendConfirmationEmail
{
	my $result;
	my $sc_action = $_[0];
	if ($sc_action eq "register")
	{
		my $Full_name = uri_escape($Full_name);
		my $random_number = &GetRandomNosChars(6);
		my $Subject = "Confirmation of Registration";
		my $url = "http://www.webgenie.com/cgi-bin/SDM/sdm_mailer.cgi?conf_email+$random_number+User_email=$User_email&Full_name=$Full_name&Subject=$Subject&Confirmation_code=$Confirmation_code&";	
		$result = &LWPMethod($url);
	}
	if ($sc_action eq "send_password")
	{
		my $random_number = &GetRandomNosChars(6);
		my $Subject = "Password Request";
		$url = "http://www.webgenie.com/cgi-bin/SDM/sdm_mailer.cgi?send_password+$random_number+User_email=$User_email&Full_name=$Full_name&Password=$Password&Subject=$Subject&";	
#&debug($url);		
		$result = &LWPMethod($url);
	}
	return $result;
}
sub SendMailToOwner
{
	if (!$User_email || $User_email !~ /^.*@.*\./)
	{
		$mailerror = 1;
		return;
	}
	$filecontent = $content;
	$Owner_name = "WebGenie Software";
	$tfilecontent =  "From:$User_name <$User_email>\n";
	$tfilecontent .=  "To:$Owner_name <$Owner_email>\n";
	$tfilecontent .=  "MIME-Version: 1.0\n";                                 # Inactivate this line to send text-only msg

	$tfilecontent .= "Subject:$Subject\n";
	$tfilecontent .= "Content-Type: text/html; charset=ISO-8859-1; format=flowed\n";
	$tfilecontent .= "Content-Transfer-Encoding: 7bit\n\n";
	$tfilecontent .= $filecontent;

	my $filename = "/tmp/perlgenie$$.tmp";
	open (OUT, ">$filename");
	print OUT $tfilecontent;
	close (OUT);
	`$mailprogram -t < $filename`;
	$mailerror = $?;
#&debug("mailerror=$mailerror	`$mailprogram -t < $filename`;");
	if(!$mailerror)
	{
		unlink($filename);
	}
}
sub GetCountry
{
	my $ip = $_[0];
	my $gi = Geo::IP->new(GEOIP_MEMORY_CACHE);
	my $country = $gi->country_code_by_addr($ip);
	return $country;
}
sub CreateMailContent
{
}
sub Register
{
	my $country = &GetCountry($remoteHostID);	
	my @allowed_countries = qw(AU US GB UK NZ CA DE FR);
	if($country ~~ @allowed_countries) 
	{
#&debug("g_recaptcha_response = $g_recaptcha_response");
		$g_recaptcha_response = 1; # Debug
		if (!$g_recaptcha_response)
		{
			my $Url = "http://www.google.com/recaptcha/api/verify"; # http://www.google.com/recaptcha/api/verify
			$ok = &LWP_CAPTCHA($Url); 
			if ($ok !~ /^true/)
			{
				print "location: http://www.webgenie.com/nocaptcha.html\n\n";
				exit;
			}
		}
	}
	else
	{
		print "location: http://www.webgenie.com/nocaptcha.html\n\n";
		exit;
	}
	$Confirmation_code = &GetRandomNosChars(10);
	&ConnectToDBase;
	$query = "select id from `users` where User_email='$User_email';";
	&execute_query($query);
	my @results = &Fetchrow_array(1);
	my $id=$results[0];
	if(!$id)
	{
		$query = "insert into `users` (Full_name,User_email,password,confirm_code) values ('$Full_name','$User_email','$password','$Confirmation_code');";
		&execute_query($query);
#&debug($query);
	}
	else
	{
		print "location: http://www.webgenie.com/already_registered.html\n\n";
		$dbh->disconnect;
		exit;
	}
	
	$dbh->disconnect;
	$result = &SendConfirmationEmail($sc_action);
	if($result eq "OK")
	{
		print "location: http://www.webgenie.com/thanks.html\n\n";
	}
	else
	{
&debug($result);		
		print "location: http://www.webgenie.com/sorry.html\n\n";
	}
}
sub StoreMarkupDetails
{
}
sub GetKeyWordSpy
{
	$url =~ s/http.*:\/\///gi;
	my @fields = split(/\//, $url);
	$domain = $fields[0];
	$domain =~ s/www\.//gi;
	my $filename = $domain;
#my $filename = "test.txt";
#	$filename = "./Cache/$se/$filename";
	$filename = "$homedir/Cache/$se/$filename";
#&debug("File:$filename");
	if (-f $filename)
	{
#&debug("Existing file found:$filename");
		open(INP, "<$filename");
		@filecontent = <INP>;
		close(INP);
		&debug("<tr><td colspan=4><hr></td></tr>\n"); # <hr> Denotes reading from cache
	}
	else
	{
		my $keywordspy_url = "curl -sA \"Chrome\" -L 'http://www.keywordspy.com/research/search.aspx?q=$domain'";
#&debug("New search: $keywordspy_url");
		$keywordspy_result = `$keywordspy_url`;
		@filecontent = split(/\n/, $keywordspy_result);
		open(OUT, ">$filename");
		print OUT $keywordspy_result;
		close(OUT);
		if (!-f $filename)
		{
			$error = $!;		
#&debug("2. $filename: Not Writing: $error");
		}
#&debug("3. $filename");
	}
	my $len = $#filecontent;
	for ($j=0; $j <= $len; $j++)
	{
		if ($filecontent[$j] =~ /Organic Overview/) { last; }
	}
	for ($j++; $j <= $len; $j++)
	{
		if ($filecontent[$j] =~ /<\/table>/) { last; }
#    <td class="overview-details-left"><a href="/overview/keyword.aspx?q=what is froogle">what is froogle</a></td>
#    <td class="overview-details-right" align="right">9</td>		
		if ($filecontent[$j] =~ /overview-details-left/) 
		{ 
			my @fields = split(/>/, $filecontent[$j]);
			@fields = split(/</, $fields[2]);
			my $search_term = $fields[0]; 
			my @fields = split(/>/, $filecontent[$j+1]);
			@fields = split(/</, $fields[1]);
			my $search_rank = $fields[0];
			if ($search_rank ne '&nbsp;' || $search_term ne '&nbsp;')
			{
				$search_rank_and_term = "$search_rank\|$search_term";
				push(@search_terms, $search_rank_and_term);
			}
		}
	}
	my $len = $#search_terms;
	if ($len >= 0) 
	{ 
		@search_terms = sort numerically (@search_terms);
		$search_terms_to_display = "<table style=\"font-size:10px; width:70%; text-align:left\">
		<input type=hidden name=sc_action value=google>
		<input type=hidden name=domain value=\"$domain\">\n";
		$search_terms_to_display .= "<tr><td align=center>Position</td><td>Search Term</td><td align=center>Position</td><td>Search Term</td></tr>\n";
		my $len = $#search_terms;
		my $locationStr = "";
		if($country_code && $gl eq "gl") 	{ $locationStr = "&gl=$country_code"; }
		if($country_code && $gl eq "country") 	{ $locationStr = "&cr=country$country_code"; }
		for(my $j=0; $j <= $len; $j++)
		{
			$search_terms_to_display .= "<tr>";
			my $item = $search_terms[$j++];
			my @fields = split (/\|/, $item);
			my $google_page = int($fields[0]/10)*10;
			$google_search_term = $fields[1];
			$google_search_term =~ s/ /\+/gi;
#			$search_terms_to_display .= "<td align=center>$fields[0]</td><td><input type=radio name=search_term value=\"$fields[0]|$fields[1]\" onmousedown=\"GetAndInsertST(this.form,this)\"><a href=\"$google_url$google_search_term$locationStr&start=$google_page\" target=\"_blank\"> $fields[1]</a></td>\n";
			$search_terms_to_display .= "<td align=center>$fields[0]</td><td><input type=radio name=search_term value=\"$fields[0]|$fields[1]\" onmousedown=\"GetAndInsertST(this.form,this)\"><a href=\"$searchURL=$google_search_term\" target=\"_blank\"> $fields[1]</a></td>\n";
			my $item = $search_terms[$j];
			my @fields = split (/\|/, $item);
			my $google_page = int($fields[0]/10)*10;
			$google_search_term = $fields[1];
			$google_search_term =~ s/ /\+/gi;
#			$search_terms_to_display .= "<td align=center>$fields[0]</td><td><input type=radio name=search_term value=\"$fields[0]|$fields[1]\" onmousedown=\"GetAndInsertST(this.form,this)\"><a href=\"$google_url$google_search_term$locationStr&start=$google_page\" target=\"_blank\"> $fields[1]</a></td>\n";
			$search_terms_to_display .= "<td align=center>$fields[0]</td><td><input type=radio name=search_term value=\"$fields[0]|$fields[1]\" onmousedown=\"GetAndInsertST(this.form,this)\"><a href=\"$searchURL=$google_search_term\" target=\"_blank\"> $fields[1]</a></td>\n";
			$search_terms_to_display .= "</tr>";
		}
		#$search_terms_to_display .= "<tr><td align=left colspan=2><input type=text name=search_term_other value=\"Froogle Feeder\"> Other</td></tr>\n";
		#$search_terms_to_display .= "<tr><td align=left colspan=2><input type=button value=Display onmousedown=\"google(this.form)\"> Other</td></tr>\n";
		$search_terms_to_display .= "</table>\n";
	}
	else
	{
		$search_terms_to_display = "
		<input type=hidden name=sc_action value=google>
		<input type=hidden name=domain value=\"$domain\">\n";
		$search_terms_to_display .= "<span style=\"text-align:justify; color:red; font-size:12px\">Sorry! Your domain has no history in our database. 
		Please do a manual <a href=\"http://www.google.com/\" target=\"_blank\">Google Search</a> to find the search terms that bring up your pages and, then, insert one in the box below. Alternatively,
		please write to us to scan your domain to find some relevant search terms.</span>";
	}
	&debug($search_terms_to_display);
}
sub MarkupDomainResultsBing
{
	my $len = $#search_results;	
	for(my $j=0; $j <= $len; $j++)
	{
		if($search_results[$j] =~ /href=.*$domain.*>?/i)
		{
			$rating_value = &Monify($rating_value);
			$review_rating = &Monify($review_rating);
			
			if($rating_value > 5) { $rating_value = 5; }
			my $starcount = int($rating_value);
			my $table_top = "<table cellpadding=\"0\" cellspacing=\"0\" style=\"width: 100%\"><tr><td valign=\"top\"><img src=\"$image_url\" style=\"width:70px; height:70px\">&nbsp;</td><td>&nbsp;&nbsp;</td><td valign=\"top\">";
			my $table_bottom = "</td></tr></table>";
			my $stars = "<br><span style=\"color:red\"><strong>$rating_value/5</strong></span> <span style=\"color:gray; font-size:13px\"><img src=\"http://www.webgenie.com/Software/SDM/$starcount-star.png\"> $rating_count votes - $price</span>";
			if($rating_or_review eq "review")
			{
				$starcount = int($review_rating);
				$stars = "<div style=\"color:gray; font-size:13px\"><img src=\"http://www.webgenie.com/Software/SDM/$starcount-star.png\"> Rating: $review_rating - $review_count reviews</div>";
			}
#			$search_results[$j] =~ s/<\/h2>/<\/h2>$table_top/gi;
#			$search_results[$j] =~ s/<\/li>/<\/li>$table_bottom/gi;
			$search_results[$j] =~ s/<\/cite>/<\/cite>$stars/gi;
			$search_results[$j] = "<ol id=\"b_results\">" . $search_results[$j] . "\n";
		}
		else
		{
			if ($search_results[$j]) { $search_results[$j] = "<ol id=\"b_results\">" . $search_results[$j] . "\n"; }
		}
	}
	$search_results = join("",@search_results);
}
sub MarkupDomainResults
{
	my $len = $#search_results;	
	my $k="";	
	$rating_value = &Monify($rating_value);
	$review_rating = &Monify($review_rating);
	
	if($rating_value > 5) { $rating_value = 5; }
	my $starcount = int($rating_value);
	my $table_top = "<table cellpadding=\"0\" cellspacing=\"0\" style=\"width: 100%\"><tr><td valign=\"top\"><img src=\"$image_url\" style=\"width:70px; height:70px\">&nbsp;</td><td>&nbsp;&nbsp;</td><td valign=\"top\">";
	my $table_bottom = "</td></tr></table></div>";
	my $stars = "<div style=\"color:gray; font-size:13px\"><img src=\"http://www.webgenie.com/Software/SDM/$starcount-star.png\"> Rating: $rating_value - $rating_count votes - $price</div>";
	if($rating_or_review eq "review")
	{
		$starcount = int($review_rating);
		$stars = "<div style=\"color:gray; font-size:13px\"><img src=\"http://www.webgenie.com/Software/SDM/$starcount-star.png\"> Rating: $review_rating - $review_count reviews</div>";
	}
	for(my $j=0; $j <= $len; $j++)
	{
		if(!$search_results[$j] || $search_results[$j] =~ /^<\/div>$/) 
		{
			$search_results[$j] = "";
			next;
		}
		if($search_results[$j] !~ /<div class="_sPg">/) 
		{
			$k++;
		}
		if($k <= 10)
		{
			if(&RecordIsFromDomain($search_results[$j]))
			{
				$search_results[$j] =~ s/<\/h3>/<\/h3>$table_top/gi;
				$search_results[$j] =~ s/<br><\/div><\/div>/<br><\/div>$table_bottom<\/div>/gi;
				$search_results[$j] =~ s/Cached<\/a><\/li><\/ul><\/div><\/div>/Cached<\/a><\/li><\/ul><\/div><\/div>$stars/gi;
				$search_results[$j] =~ s/Similar<\/a><\/li><\/ul><\/div><\/div>/Similar<\/a><\/li><\/ul><\/div><\/div>$stars/gi;
				$search_results[$j] = "<div class=\"g\"  style=\"background-color:#CCFFCC\">" . $search_results[$j] . "\n";
			}
			else
			{
				if ($search_results[$j]) { $search_results[$j] = "<div class=\"g\">" . $search_results[$j] . "\n"; }
			}
		}
		else
		{
			if(&RecordIsFromDomain($search_results[$j]))
			{
				if ($search_results[$j]) { $search_results[$j-1] = "<div class=\"g\">" . "Skipped  $skipped records" . "</div>\n"; }
				$search_results[$j] =~ s/<\/h3>/<\/h3>$table_top/gi;
				$search_results[$j] =~ s/<br><\/div><\/div>/<br><\/div>$table_bottom<\/div>/gi;
				$search_results[$j] =~ s/Cached<\/a><\/li><\/ul><\/div><\/div>/Cached<\/a><\/li><\/ul><\/div><\/div>$stars/gi;
				$search_results[$j] =~ s/Similar<\/a><\/li><\/ul><\/div><\/div>/Similar<\/a><\/li><\/ul><\/div><\/div>$stars/gi;
				$search_results[$j] = "<div class=\"g\"  style=\"background-color:#CCFFCC\">" . $search_results[$j] . "\n";
				$skipped = 0;
			}
			else
			{
				if ($search_results[$j]) { $search_results[$j] = ""; }
				$skipped++;
			}
		}
	}
	$search_results = join("",@search_results);
}
sub MarkupDomainResults_0
{
	my $len = $#search_results;	
	for(my $j=0; $j <= $len; $j++)
	{
#		if($search_results[$j] =~ /(href="\/url\?q=.*$domain.*>)/i)
		if(&RecordIsFromDomain($search_results[$j]))
		{
			$rating_value = &Monify($rating_value);
			$review_rating = &Monify($review_rating);
			
			if($rating_value > 5) { $rating_value = 5; }
			my $starcount = int($rating_value);
			my $table_top = "<table cellpadding=\"0\" cellspacing=\"0\" style=\"width: 100%\"><tr><td valign=\"top\"><img src=\"$image_url\" style=\"width:70px; height:70px\">&nbsp;</td><td>&nbsp;&nbsp;</td><td valign=\"top\">";
			my $table_bottom = "</td></tr></table></div>";
			my $stars = "<div style=\"color:gray; font-size:13px\"><img src=\"http://www.webgenie.com/Software/SDM/$starcount-star.png\"> Rating: $rating_value - $rating_count votes - $price</div>";
			if($rating_or_review eq "review")
			{
				$starcount = int($review_rating);
				$stars = "<div style=\"color:gray; font-size:13px\"><img src=\"http://www.webgenie.com/Software/SDM/$starcount-star.png\"> Rating: $review_rating - $review_count reviews</div>";
			}
			$search_results[$j] =~ s/<\/h3>/<\/h3>$table_top/gi;
			$search_results[$j] =~ s/<br><\/div><\/div>/<br><\/div>$table_bottom<\/div>/gi;
			$search_results[$j] =~ s/Cached<\/a><\/li><\/ul><\/div><\/div>/Cached<\/a><\/li><\/ul><\/div><\/div>$stars/gi;
			$search_results[$j] =~ s/Similar<\/a><\/li><\/ul><\/div><\/div>/Similar<\/a><\/li><\/ul><\/div><\/div>$stars/gi;
			$search_results[$j] = "<div class=\"g\">" . $search_results[$j] . "\n";
		}
		else
		{
			if ($search_results[$j]) { $search_results[$j] = "<div class=\"g\">" . $search_results[$j] . "\n"; }
		}
	}
	$search_results = join("",@search_results);
}
sub HighLightDomainResultsBing
{
	my $len = $#search_results;	
	for(my $j=0; $j <= $len; $j++)
	{
		if($search_results[$j] =~ /$domain/i)
		{
			$search_results[$j] = "<li class=\"b_algo\" style=\"background-color:#CCFFCC\">" . $search_results[$j] . "\n";
		}
		else
		{
			if ($search_results[$j]) { $search_results[$j] = "<li class=\"b_algo\"" . $search_results[$j] . "\n"; }
		}
	}
	$search_results = join("",@search_results);
}
sub RecordIsFromDomain
{
	my $search_result = $_[0];
	if($search_result =~ /href=.*http(.*$domain\/)/i)
	{
		my @fields = split(/\//, $1);
		my $this_domain = $fields[2];
		$this_domain =~ s/www\.//gi;
		if ($this_domain =~ /^$domain$/)
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	return 0;
}
sub HighLightDomainResults
{
	my $len = $#search_results;
	my $k="";	
	# Find the entries for the domain
	for(my $j=0; $j <= $len; $j++)
	{
		if(&RecordIsFromDomain($search_results[$j]))
		{
			push(@positions, $j);
		}
	}		
	# Show the first 10 results, then skip and show only those with domain
	for(my $j=0; $j <= $len; $j++)
	{
		if(!$search_results[$j] || $search_results[$j] =~ /^<\/div>$/) 
		{
			$search_results[$j] = "";
			next;
		}
		if($search_results[$j] !~ /<div class="_sPg">/) 
		{
			$k++;
		}
		if($k <= 10 && $positions[0] <= 10)
		{
			if(&RecordIsFromDomain($search_results[$j]))
			{
				$search_results[$j] = "<div class=\"g\" style=\"background-color:#CCFFCC\">" . $search_results[$j] . "\n";
			}
			else
			{
				if ($search_results[$j]) { $search_results[$j] = "<div class=\"g\">" . $search_results[$j] . "\n"; }
			}
		}
		else
		{
			if(&RecordIsFromDomain($search_results[$j]))
			{
				if ($search_results[$j]) { $search_results[$j-1] = "<div class=\"g\">" . "Skipped  $skipped records" . "</div>\n"; }
				$search_results[$j] = "<div class=\"g\" style=\"background-color:#CCFFCC\">" . $search_results[$j] . "\n";
				$skipped = 0;
			}
			else
			{
				if ($search_results[$j]) { $search_results[$j] = ""; }
				$skipped++;
			}
		}
	}
	$search_results = join("",@search_results);
}
sub ParseBing_serp
{
	my @fields = split(/<ol id="b_results">/, $google_serp);
	$serp_top = $fields[0];	
	@fields = split(/<\/ol>/, $fields[1]);
	$search_results = $fields[0];	
	$serp_bottom = $fields[1];	
	@search_results = split(/<li class="b_algo">/,$fields[0]);
	if($markup) { &MarkupDomainResultsBing; }
	else { &HighLightDomainResultsBing; }
	$google_serp = $serp_top . "<ol id=\"b_results\">" . $search_results . "</ol>" . $serp_bottom;
}
sub ParseGoogle_serp
{
	my @fields = split(/<ol>/, $google_serp);
	my $len = $#fields;	
	$j0 = $len - 1 ;
	$j1 = $len;
	$google_serp_top = $fields[0];	
	my @fields = split(/<\/ol>/, $fields[$j1]);
	$search_results = $fields[0];	
	$google_serp_bottom = $fields[1];	
	@search_results = split(/<div class="g">/,$search_results);
	if($markup) { &MarkupDomainResults; }
	else { &HighLightDomainResults; }
	$google_serp = $google_serp_top . "<ol>" . $search_results . "</ol>" . $google_serp_bottom;
}
sub GetGoogleSerp
{
	$domain =~ s/www\.//gi;
	$search_term =~ s/ *$//gi; # Remove trailing spaces
	$search_term =~ s/ /\+/gi;
	my $filename = $search_term;
	$filename =~ s/\+/_/gi;
	$filename = "$homedir/Cache/$se/$filename";
	if (-f $filename && $use_cache)
	{
		open(INP, "<$filename");
		@google_serp = <INP>;
		close(INP);
		$google_serp = join("\n", @google_serp);
		&debug("<hr>"); # <hr> Denotes reading from cache
	}
	else
	{
		my $locationStr = "";
		if($country_code && $gl eq "gl") 	{ $locationStr = "&gl=$country_code"; }
		if($country_code && $gl eq "country") 	{ $locationStr = "&cr=country$country_code"; }

		my $start_page = $serp_rank * 10;
		my $google_url = "curl -sA \"Chrome\" -L '$searchURL=$search_term'";
		$google_serp = `$google_url`;
		open(OUT, ">$filename");
		print OUT $google_serp;
		close(OUT);
	}
	my $outfile = "$homedir/httpdocs/test1.htm";
	open(OUT, ">$outfile");
	print OUT $google_serp;
	close(OUT);
	$error = $!;		
	if($searchURL =~ /google/ && $google_serp =~ /href=.*(http.*$domain\/)/i)
	{
		&ParseGoogle_serp;
	}
	elsif($google_serp =~ /href=.*$domain/ && $searchURL =~ /bing/)
	{
		&ParseBing_serp;
	}
	else
	{
		$google_serp = "<div style=\"text-align:center\">Your domain is not on the first 10 pages. Please try a different search or switch the search engines.
		<span style=\"cursor:pointer; text-decoration:underline\" onmousedown=\"showTheseDivs('avs_keywords_display','avs_keyword_spy','avs_search_terms')\">Try Again!</span></div>";
	}
	$google_serp =~ s/<div class="g"/\n<div class="g"/gi;	
	$google_serp =~ s/<div id=gbar/<div id=gbar style="display:none"/gi;	
	$google_serp =~ s/<div id=guser/<div id=guser style="display:none"/gi;	
	$google_serp =~ s/<div class="tn"/<div class="tn" style="display:none"/gi;	
	$google_serp =~ s/<div><h2 class="hd">Search Options<\/h2>/<div style="display:none"><h2 class="hd">Search Options<\/h2>/gi;
	if($se eq "google") { $google_serp =~ s/<head>/<head><base href=\"http:\/\/www.google.com\">/gi; }
	if($se eq "bing") { $google_serp =~ s/<head>/<head><base href=\"http:\/\/www.bing.com\">/gi; }
	@filecontent = split(/\n/, $google_serp);
	my $len = $#filecontent;
	my $outfile = "$homedir/httpdocs/test.htm";
	open(OUT, ">$outfile");
	print OUT $google_serp;
	close(OUT);
	&debug($google_serp);
}
sub Markup
{
#	&StoreMarkupDetails;
	&GetKeyWordSpy;
}
sub Google
{
	&GetGoogleSerp;
}
sub GetRandomNosChars
{
	$n = $_[0];
	$alphanumeric = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
	@alphanumeric = split (//, $alphanumeric);
	$randomString = "";
	for (my $j=0; $j <= $n; $j++)
	{
		srand;  # Seed the random number
		$i = int (rand (62));  # Get a random start position
		$randomString .= $alphanumeric[$i];
	}
	return $randomString;
}
sub Confirm
{
#&debug($id);
	&ConnectToDBase;
	$query = "select id,confirmed from `users` where confirm_code='$id';";
	&execute_query($query);
	my @results = &Fetchrow_array(2);
	my $id=$results[0];
	my $confirmed=$results[1];
	if($id && !$confirmed)
	{
		$query = "update `users` set confirmed=1, status=1, modified_date=now() where id='$id';";
		&execute_query($query);
		$dbh->disconnect;
		print "Content-type:text/html\n\n";
		print("Confirmed");
		exit;
	}
	elsif($id && $confirmed)
	{
#		print "location: http://www.webgenie.com/not_registered.html\n\n";
		print "Content-type:text/html\n\n";
		print("Already Confirmed");
		$dbh->disconnect;
		exit;
	}
	else
	{
		print "Content-type:text/html\n\n";
		print("Not Found");
		$dbh->disconnect;
		exit;
	}
}
sub SetLoginCookieAjax
{
	# NOTE: This method adds the HTTPD header after setting the cookie. Hence, it is not possible to do a 'print location' after that.
	# It may be the reason why this method was not used in previous instances.
	# It should be OK to use it for JavaScript calls but not for Form submit
	# That is why it is called "...Ajax" !
	my $ndays = $_[0];
	use CGI;
	$cookiequery = new CGI;
	$cookie = $cookiequery->cookie(-name=>'WebGenie_SDM',
	-value=>$login_cookie,
	-expires=>'+3M',
	-path=>'/');
	$cookie =~ s/%7C/\|/gi;
	$cookie =~ s/%40/\@/gi;
	print $cookiequery->header(-cookie=>$cookie);
	$headerAdded = 1; # The CGI.pm is adding the header after lodiging cookie
}
sub Login
{
	&ConnectToDBase;
	$query = "select Full_name from `users` where id = '$id' and status=1;";
	&execute_query($query);
	my @results = &Fetchrow_array(1);
	$Full_name = $results[0];
	$dbh->disconnect;
	print "Content-type:text/html\n\n";
#&debug($query);	
	my @fields = split (/\s/, $Full_name);
	my $First_name = $fields[0];
	if ($First_name) { print $First_name; }
	else { print "Not OK"; }
}
sub do_main
{
#&debugEnv;
  $cl = $ENV{'CONTENT_LENGTH'};
  if ($cl > 0)
  {
	read(STDIN, $_, $cl);
	$_ .= "&"; # Append an & char so that the last item is not ignored
	$pquery = &reformat($_);
	@pquery = split(/\&/, $pquery);
	$lenpquery = $#pquery;
	&Get_fields (@pquery);
	if ($sc_action eq "register")
	{
#		print "Content-type:text/html\n\n";
		&Register;
		exit;
	}
	if ($sc_action eq "contactus")
	{
		&Contactus;
		exit;
	}
	&debug("sc_action ($sc_action) was not found",1);
  }
  else
  {
  	$query_string = $ENV{'QUERY_STRING'};
  	$query_string = uri_unescape($query_string);
  	@fields = split(/\+/, $query_string);
  	$sc_action = $fields[0];
	$pquery = $fields[2];
	@pquery = split(/\&/, $pquery);
	&Get_fields (@pquery);
	if($se eq "bing") { $searchURL = $bing_url; }
	if($se eq "google") { $searchURL = $google_url; }
	if($search_term_other) { $search_term = $search_term_other; }
	if ($sc_action eq "markup")
	{
		&Markup;
		exit;
	}
	if ($sc_action eq "google")
	{
		&Google;
		exit;
	}
	if ($sc_action eq "confirm")
	{
		&Confirm;
		exit;
	}
	if ($sc_action eq "re_login")
	{
		&Login;
		exit;
	}
	if ($sc_action eq "login")
	{
		&ConnectToDBase;
		$query = "select id from `users` where User_email = '$User_email' and Password = '$Password' and status=1;";
#&debug($query);	
		&execute_query($query);
		my @results = &Fetchrow_array(1);
		$dbh->disconnect;
		$id = $results[0];
		if ($id) 
		{ 
			$query = "update `users` set last_login=now() where id='$id';";
			&execute_query($query);
			$login_cookie = $id;
			&SetLoginCookieAjax;
			print "OK";
		}
		else
		{ 
			print "Content-type:text/html\n\n";
			print "Not OK";
		}
		exit;
	}
	if ($sc_action eq "send_password")
	{
		&ConnectToDBase;
		$query = "select id,Full_name,password from `users` where User_email = '$User_email' and status=1;";
#&debug($query);		
		&execute_query($query);
		my @results = &Fetchrow_array(3);
		$dbh->disconnect;
		$id = $results[0];
		$Full_name = $results[1];
		$Password = $results[2];
		if(!$id)
		{
			print "Content-type:text/html\n\n";
			print "Incorrect Email address";
			exit;
		}
		$result = &SendConfirmationEmail($sc_action);
#&debug($result);
		print $result;
		exit;
	}
	&debug("sc_action ($sc_action) was not found",1);
  }
}
$thisCGI = "/cgi-bin/perlgenie.cgi";
$Owner_email = 'perlsupport@webgenie.com';
$mailprogram = "/usr/sbin/sendmail";
$remoteHostID = $ENV{'REMOTE_HOST'};
if (!$remoteHostID) { $remoteHostID = $ENV{'REMOTE_ADDR'}; }
$ProcessTime = `/bin/date`;
$ProcessTime =~ s/\n//gi;
$tmpDir = "/tmp";
$google_url = "http://www.google.com/search?num=100&hl=en&gl=US&q";
$bing_url = "http://www.bing.com/search?setmkt=en-US&count=50&q";
$use_cache = 1;
$homedir = "/var/www/sdm.webgenie.com";
$|=1;
&do_main;
#CREATE TABLE `users` (  `id` bigint(11) NOT NULL AUTO_INCREMENT,  `Full_name` varchar(100) DEFAULT '',  `User_email` varchar(100) NOT NULL DEFAULT '',  `password` varchar(20) DEFAULT '',  `confirm_code` varchar(100) DEFAULT '',  `confirmed` int(1) DEFAULT '0',  `status` int(1) DEFAULT '0',  `last_login` datetime DEFAULT NULL,  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,  `modified_date` datetime DEFAULT NULL,  PRIMARY KEY (`User_email`),  KEY `id` (`id`)) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


