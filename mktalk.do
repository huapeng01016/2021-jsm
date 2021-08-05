/* 
	Author: 	Hua Peng
	Date:		Aug 03, 2021
	Purpose:	Build reveal.js slides deck for 2021 JSM
*/

local path = ""
if "`c(os)'" == "MacOSX" {
	dynpandoc pystata.md, 	/// 
		sav(pystata.html)	/// 
		replace 	/// 
		to(revealjs) 	/// 
		path(/Users/hpeng01016/anaconda3/bin/pandoc)	///		
		pargs(-s --template=revealjs.html  	/// 
		--self-contained	/// 
		--section-divs	/// 
		--variable theme="stata"	/// 
		)
}
else {
	dynpandoc pystata.md, 	/// 
		sav(pystata.html)	/// 
		replace 	/// 
		to(revealjs) 	/// 
		pargs(-s --template=revealjs.html  	/// 
		--self-contained	/// 
		--section-divs	/// 
		--variable theme="stata"	/// 
		)
}

exit

