// perlgenie.js
  // ***************************************************************************
  // ///////////////////////////////////////////////////////////////////////////
  // ***************************************************************************
  //
  //  SOFTWARE: PerlGenie.Com
  //   VERSION: 1.0
  // 
  // ***************************************************************************
  // ///////////////////////////////////////////////////////////////////////////
  // ***************************************************************************
  // Functions added by AVS
  // Copyright (c) 2016 by AV Sivaprasad and WebGenie Software Pty Ltd.
var items_in_cart = 0;
var cookiename    = "WebGenie_SDM";
var cookieVal = "";
var tot_price = 0;
var item_tax = 0;
var item_totpayable = 0;
var pquery;
var url;
var sc_action;
var number_of_products = 0;
var divs = [];
//-- Clear Defaults in form inputs

/*
 * Clear Default Text: functions for clearing and replacing default text in
 * <input> elements.
 *
 * by Ross Shannon, http://www.yourhtmlsource.com/
 */
	addEvent(window, 'load', init, false);
	
	function init() 
	{
	    var formInputs = document.getElementsByTagName('input');
	    for (var i = 0; i < formInputs.length; i++) 
	    {
		var theInput = formInputs[i];
		
		if (theInput.type == 'text' && theInput.className.match(/\bcleardefault\b/)) 
		{  
		    /* Add event handlers */          
		    addEvent(theInput, 'focus', clearDefaultText, false);
		    addEvent(theInput, 'blur', replaceDefaultText, false);
		    
		    /* Save the current value */
		    if (theInput.value != '') 
		    {
			theInput.defaultText = theInput.value;
		    }
		}
	    }
	    var formInputs = document.getElementsByTagName('textarea');
	    for (var i = 0; i < formInputs.length; i++) 
	    {
		var theInput = formInputs[i];
		
		if (theInput.className.match(/\bcleardefault\b/)) 
		{  
		    /* Add event handlers */          
		    addEvent(theInput, 'focus', clearDefaultText, false);
		    addEvent(theInput, 'blur', replaceDefaultText, false);
		    
		    /* Save the current value */
		    if (theInput.value != '') 
		    {
			theInput.defaultText = theInput.value;
		    }
		}
	    }
	}
	
	function clearDefaultText(e) {
	    var target = window.event ? window.event.srcElement : e ? e.target : null;
	    if (!target) return;
	    
	    if (target.value == target.defaultText) {
		target.value = '';
	    }
	}
	
	function replaceDefaultText(e) {
	    var target = window.event ? window.event.srcElement : e ? e.target : null;
	    if (!target) return;
	    
	    if (target.value == '' && target.defaultText) {
		target.value = target.defaultText;
	    }
	}
	
	jQuery(document).ready(function($) 
	{

		if (window.history && window.history.pushState) 
		{

		window.history.pushState('forward', null, '');

			$(window).on('popstate', function() 
		{
//				showTheseDivs('avs_0', 'avs_5', 'avs_6', 'avs_10','avs_11');
		}
		);

		}
	});

//-- Clear Defaults in form inputs
// Close a CSS box
/*
window.onload = function(){
    document.getElementById('close').onclick = function(){
        this.parentNode.parentNode.parentNode
        .removeChild(this.parentNode.parentNode);
        return false;
    };
};
*/
// Close a CSS box


function get_browser(){
    var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []; 
    if(/trident/i.test(M[1])){
        tem=/\brv[ :]+(\d+)/g.exec(ua) || []; 
        return {name:'IE',version:(tem[1]||'')};
        }   
    if(M[1]==='Chrome'){
        tem=ua.match(/\bOPR\/(\d+)/)
        if(tem!=null)   {return {name:'Opera', version:tem[1]};}
        }   
    M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
    return {
      name: M[0],
      version: M[1]
    };
 }

 function checkAndShow()
 {
	var doc = document.location.href;
alert(doc);	
 }
 function setSectionHeight(height)
 {
	var id = document.getElementById('avs_main_section'); 
 	if(!height)
 	{
		height = 830; // default
		var doc = document.location.href;
		var i = doc.indexOf('markup.html');
		if (i >= 0) height = 830;
		var i = doc.indexOf('pricing.html');
		if (i >= 0) height = 610;
		var i = doc.indexOf('subscribe.html');
		if (i >= 0) height = 670;
 	}
	id.style.height = height +"px";
 }
 function getMaxHeight()
 {
	var n = divs.length;
	var j;
	for (j=0; j < n; j++)
	{
		var id = document.getElementById(divs[j]); 
		var idh = id.style.height;
//		alert(j + ". " + divs[j] + " Height: " + idh);
	}
 	 
 }
 function DetectBrowser()
 {
 	 var bv = get_browser();
//alert("Browser: " + bv.name + "; Version: " + bv.version);
	if((bv.name == "IE" && bv.version <= 8) || (bv.name == "MSIE"))
	{
		showHide('old_re_captcha','div','block');	
		showHide('new_re_captcha','div','none');	
	}
	else
	{
		showHide('new_re_captcha','div','block');	
		showHide('old_re_captcha','div','none');	
	}
 }
 	function ParseTheQueryString()
	{
		var idx = document.URL.indexOf('?');
		var params = {}; // simple js object
		if (idx != -1) 
		{
			var pairs = document.URL.substring(idx + 1, document.URL.length).split('&');
			for (var i = 0; i < pairs.length; i++) 
			{
			    nameVal = pairs[i].split('=');
			    params[nameVal[0]] = nameVal[1];
			}
		}
		var sc_action = unescape(params["q"]);
		var id = unescape(params["id"]);
//alert(sc_action);		
		if (sc_action == 'access_denied')
		{
			showTheseDivs('avs_main_section','avs_access_denied');
			return;
		}
		if (sc_action == 'login_failed')
		{
			showTheseDivs('avs_main_section','avs_login_failed');
			return;
		}
//alert("OK");

//alert(id);
		pquery = 
		"&id=" + id +
		"&";
		ajaxFunction(4,sc_action,id);
	}

	function BingMarkUp(iframe1,iframe2)
	{
var content = document.getElementById(iframe2).contentWindow.document.body.outerHTML;
//alert(content);
var myIFrame = document.getElementById(iframe1);
myIFrame.contentWindow.document.body.innerHTML = content;
//document.getElementById(iframe1).contentWindow.document.body.innerHTML = content;
	}

function xinspect(o,i){
    if(typeof i=='undefined')i='';
    if(i.length>50)return '[MAX ITERATIONS]';
    var r=[];
    for(var p in o){
        var t=typeof o[p];
        r.push(i+'"'+p+'" ('+t+') => '+(t=='object' ? 'object:'+xinspect(o[p],i+'  ') : o[p]+''));
    }
    return r.join(i+'\n');
}

function GetAny()
{
var content = document.getElementById("iframe_1").contentWindow.document.body.outerHTML;
//var content = document.getElementById("bing_raw").contentWindow.document.body.outerHTML;
alert(content);
return;

	var url = "http://www.google.com";
	var object = $.getJSON(url);
var output = '';
for (var property in object) {
  output += property + ': ' + object[property]+'; ';
}
document.write(output);
//document.write(inspect(object));
//console.log(object);
//alert(JSON.stringify(content));
// example of use:
//alert(xinspect(content));
return;
	
//	$.getJSON('http://whateverorigin.org/get?url=' + encodeURIComponent('http://www.google.com/search?q=webgenie+shopping+cart') + '&callback=?', function(data){
	$.getJSON('http://whateverorigin.org/get?url=' + encodeURIComponent('http://www.google.com/') + 'search?q=webgenie+shopping+cart' + '&callback=?', function(data){
		alert(data.contents);
	});
}
	function GetAndInsertST(form,item)
	{
		var search_term = item.value;
		var end = search_term.indexOf('|');
		var pos = search_term.substring(0,end);
		var search_string = search_term.substring(end+1,search_term.length);
		var page = parseInt(pos/10);
//alert(document.main_form);
//		form.serp_rank.value = page;
		form.search_term_other.value = search_string;
//alert(page);		
	}
	function CSWriteCookie() 
	{
//		cookieVal += "; path=/";
		var this_cookie = cookiename + "=" + cookieVal;
//		this_cookie += ";";
//alert("this_cookie = " + this_cookie);		
		document.cookie = this_cookie;
		var cookies = document.cookie;
//alert("cookies set now: " + cookies);		
	}
	function Logout(id) 
	{
		document.cookie = cookiename + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
		document.location = '/';
	}
	function CSReadCookie(id) 
	{
		var cookies = document.cookie;
		cookies = unescape(cookies);
		return cookies;
	}
	function ParseCookies(cookies,id)
	{
//alert(cookies);				
		var cookies_array = cookies.split(";");
		nc = cookies_array.length;
		for (var j=0; j < nc; j++)
		{
			var i = cookies_array[j].indexOf(id, 0);
			if (i >= 0) 
			{
				var i = cookies_array[j].indexOf('=', 0);
//alert(i);				
				var user_id = cookies_array[j].substring(i+1,cookies_array[j].length);
				return user_id;
//alert(user_id);				
			}
		}
		return 0;
	}
	function Monify(value)
	{
	//alert (value);
	  if (!value || value == undefined) return "0.00";
	  var str = "" + Math.round(value*100);
	  var len = str.length;
	
	  return (str=="0")?"":(str.substring(0,len-2)+"."+str.substring(len-2,len));
	}
  	function ConfirmOrder()
  	{
		showTheseDivs('avs_checkout','avs_personal_details','avs_billing_details','avs_confirm_button');
		showTheseDivs('avs_confirm');
  	}
	function Send_password(form,action)
	{
		var User_email = form.User_email.value;
		pquery = 
		"&User_email=" + User_email +
		"&";
		ajaxFunction(6);
	}
	function Login(form,action)
	{
		var User_email = form.User_email.value;
		var Password = form.Password.value;
		pquery = 
		"&User_email=" + User_email +
		"&Password=" + Password +
		"&";
		ajaxFunction(5);
	}
	function google(form,action)
	{
		if (form.search_term) var search_term = form.search_term.value;
		var search_term_other = form.search_term_other.value;
		var domain = form.domain.value;
//		var serp_rank = form.serp_rank.value;
//		var gl = form.gl.value;
		var gl = 'gl';
//		if(document.getElementById("gl2").checked) gl = 'country';
//		if(form.gl[1].checked) gl = 'country';
//alert(gl);		
		var se = 'bing';
		if(form.se[1].checked) se = 'google';
//alert(se);		
		if (!search_term && !search_term_other) 
		{
			alert("No Search Term Specified. Exiting.");
			return;
		}
/*
		var verified = form.verified.checked
		if(!verified)
		{
			alert("You must manually test this search term and check the button, 'I have tested this manually', to proceed.");
			return;
		}
*/
		if(action == 'M')
		{
			var title = form.title.value;
			var price = form.price.value;
			var image_url = form.image_url.value;
			var desc = form.desc.value;
			var rating_or_review = form.rating_or_review.value;
			var rating_value = form.rating_value.value;
			var rating_count = form.rating_count.value;
			var review_count = form.review_count.value;
			var review_rating = form.review_rating.value;
			pquery = 
			"&search_term=" + search_term +
			"&search_term_other=" + search_term_other +
			"&domain=" + domain +
			"&markup=" + action +
			"&title=" + title +
			"&price=" + price +
			"&image_url=" + image_url +
			"&desc=" + desc +
			"&rating_or_review=" + rating_or_review +
			"&rating_value=" + rating_value +
			"&rating_count=" + rating_count +
			"&review_count=" + review_count +
			"&review_rating=" + review_rating +
			"&gl=" + gl +
			"&se=" + se +
			"&";
		}
		else
		{
			pquery = 
			"&search_term=" + search_term +
			"&search_term_other=" + search_term_other +
			"&domain=" + domain +
			"&markup=" + action +
			"&gl=" + gl +
			"&se=" + se +
			"&";
		}
  		ajaxFunction(3);
	}
	function markup(form,action)
	{
		var url = form.url.value;
//		var country_code = form.country_code.value;
//		var gl = form.gl.value;
		var se = 'bing';
		if(form.se[1].checked) se = 'google';
		pquery = 
		"&url=" + url +
		"&se=" + se +
		"&";
  		ajaxFunction(2);
	}
  
	function CloseAllDivs()
	{
		var e=document.getElementsByTagName('div');
		var n = e.length;
		var i;
		for (i=0; i < n; i++)
		{
			div_id = e[i].id;
			var m = div_id.indexOf("avs_");
			if (m >= 0) 
			{
				showHide(div_id, 'div', 'none');
			}
		}
	}
	function showTheseDivs(div1,div2,div3,div4,div5,div6)
	{
		divs = []; // empty the array first
		CloseAllDivs();
		if (div1) { showHide(div1, 'div', 'block'); divs.push(div1);}
		if (div2) { showHide(div2, 'div', 'block'); divs.push(div2);}
		if (div3) { showHide(div3, 'div', 'block'); divs.push(div3);}
		if (div4) { showHide(div4, 'div', 'block'); divs.push(div4);}
		if (div5) { showHide(div5, 'div', 'block'); divs.push(div5);}
		if (div6) { showHide(div6, 'div', 'block'); divs.push(div6);}
		var maxheight = getMaxHeight();
//	var n = divs.length;
//alert(n);	
	}
	function CheckIfDivExists(id,type)
	{
		var e=document.getElementsByTagName(type);
		var n = e.length;
		var i;
		for (i=0; i < n; i++)
		{
			if(e[i].id == id) return 1;
		}
		return 0;
	}
	function showHide(id,type,state)
	{
//alert("id = " + id + " type = " + type + " state = " + state);
//		CloseAllDivs();
		if (state == undefined) state = 'block';
		var exists = CheckIfDivExists(id,type);
		if(id && exists)
		{
			var style = document.getElementById(id).style.display;
			document.getElementById(id).style.display=""+state;
		}
	}
	function showHideToggle(id,type)
	{
		var exists = CheckIfDivExists(id,type);
		if(id && exists)
		{
			var style = document.getElementById(id).style.display;
			if(style == 'none') showHide(id,type,'block');
			else showHide(id,type,'none');
		}
	}
	function ajaxFunction(n,sc_action,id)
	{
		var ran_number= Math.random()*5000;
		var xmlHttp;
		var url;
		try
		{  // Firefox, Opera 8.0+, Safari  
		  xmlHttp=new XMLHttpRequest();  
		}
		catch (e)
		{  // Internet Explorer  
			try
			{    
				xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");    
			}
			catch (e)
			{    
				try
				{      
					xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");      
				}
				catch (e)
			{	      
					alert("Your browser does not support AJAX!");      
					return false;      
				}    
			}
		}
		xmlHttp.onreadystatechange=function()
		{
			if(xmlHttp.readyState==4)
			{
				response = xmlHttp.responseText;
//alert(response);
				if (n == 1)
				{
//return;					
//alert(response);
					if(response == 'Not OK')
					{
//						alert('Login Failed! Please try again or register');
						var doc = document.location.href;
						var i = doc.indexOf('markup.html');
						if (i >= 0) document.location = 'index.html';
						else
						{
							showHide('loggedin_info','div','block');
						}
					}
					else
					{
						var First_name = response;
						var doc = document.location.href;
						var i = doc.indexOf('markup.html');
						if (i < 0) document.location = 'markup.html';
						else
						{
							var innerHTML = "Welcome " + First_name + "!" + "<a href=\"#\" onmousedown=\"Logout()\"/>Logout</a>";
							document.getElementById('loggedin_info').innerHTML = innerHTML;
							showHide('loggedin_info','div','block');
						}
					}
					
				}
				if (n == 2)
				{
//alert("2." + response);
					showTheseDivs('avs_keywords_display','avs_keyword_spy','avs_search_terms');
					document.getElementById('avs_keyword_spy').innerHTML = response;
				}
				if (n == 3)
				{
//alert("3." + response);
					document.getElementById('avs_google_serp').innerHTML = response;
					showTheseDivs('avs_google_serp_container','avs_google_serp');
				}
				if (n == 4)
				{
//					document.getElementById('avs_google_serp').innerHTML = response;
					if(response == "Confirmed")
					{
						showTheseDivs('avs_reg_ack_main','avs_reg_ack_success');	
					}
					else if(response == "Already Confirmed")
					{
						showTheseDivs('avs_reg_ack_main', 'avs_reg_ack_fail');
					}
					else
					{
						showTheseDivs('avs_reg_ack_main', 'avs_reg_ack_fail');
					}
				}
				if (n == 5)
				{
//alert("5. " + response);
					if(response == 'Not OK')
					{
//						alert('Login Failed! Please try again or register');
						var doc = document.location.href;
						var i = doc.indexOf('markup.html');
						if (i >= 0) document.location = 'index.html';
						else
						{
							document.location = 'error.html?q=login_failed';
							showHide('loggedin_info','div','block');
						}
					}
					else
					{
						var doc = document.location.href;
						var i = doc.indexOf('markup.html');
						if (i < 0) document.location = 'markup.html';
						else
						{
							showHide('loggedin_info','div','block');
						}
					}
				}
				if (n == 6)
				{
//alert(response);
					if(response == 'OK') showTheseDivs('avs_main_section','avs_password_sent');
					else showTheseDivs('avs_main_section','avs_wrong_email');
				}				
			}
		}
		if (n == 1) 
		{
			var cookies = CSReadCookie(cookiename);
			var user_id = ParseCookies(cookies,cookiename);
			pquery = 
			"&id=" + user_id +
			"&";
			url = "/cgi-bin/sdm.cgi?re_login+" + ran_number + "+" + pquery;
		}
		if (n == 2) 
		{
			pquery = escape(pquery);
			pquery = pquery.replace("+","%2B");
			url = "/cgi-bin/sdm.cgi?markup+" + ran_number + "+" + pquery;
		}
		if (n == 3) 
		{
			pquery = escape(pquery);
			pquery = pquery.replace("+","%2B");
			url = "/cgi-bin/sdm.cgi?google+" + ran_number + "+" + pquery;
		}
		if (n == 4) 
		{
			pquery = escape(pquery);
			pquery = pquery.replace("+","%2B");
			url = "/cgi-bin/sdm.cgi?" + sc_action + "+" + ran_number + "+" + pquery;
		}
		if (n == 5) 
		{
			url = "/cgi-bin/sdm.cgi?login+" + ran_number + "+" + pquery;
		}
		if (n == 6) 
		{
			url = "/cgi-bin/sdm.cgi?send_password+" + ran_number + "+" + pquery;
		}
//return;
		if (url)
		{
//alert("url = " + url);	
			xmlHttp.open("POST",url,true);
			xmlHttp.send(null); 
		}
		else
		{
			return;
		}
	}
	
/* ------------------  */
/* ------------------  */
/* ------------------  */



