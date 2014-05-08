:main
	:: load all exchanges.
	FOR %%a IN (exchange\*.txt) DO CALL :exchange %%a
	
	:: load symbols and prices 
	curl 127.0.0.1:8000/loader/
	echo %errorlevel%
	
	GOTO :end

:exchange
	:: upload to server
	curl -F formdata=@%~1 127.0.0.1:8000/loader/raw/exchange/%~n1
	echo %errorlevel%
		
	:: find all the prices and upload
	FOR %%b IN (%~n1_*.csv) DO CALL :price %~n1 %%b 
	
::	:: move to archive.
::	Move %1 archive\%1
	
	GOTO :eof

:price
	:: Upload to server (prices)
	curl -F formdata=@%2 127.0.0.1:8000/loader/raw/prices/%1
	if %errorlevel%==0 MOVE %2 loaded
	
	GOTO :eof
	
:end 
	GOTO :eof