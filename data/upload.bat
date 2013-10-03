:main
	FOR %%a IN (*.txt) DO CALL :exchange %%a
	
	GOTO :end

:exchange
	:: upload to server
	curl -F formdata=@%~1 127.0.0.1:8000/loader/raw/exchange/%~n1
	
	:: find all the prices and upload
	FOR %%b IN (%~n1_*.csv) DO CALL :price %~n1 %%b 
	
	:: move to archive.
	MOVE %1 archive\%1
	
	GOTO :eof

:price
	:: Upload to server (prices)
	curl -F formdata=@%2 127.0.0.1:8000/loader/raw/prices/%1
	
	:: archive
	MOVE %2 archive\%2
	
	GOTO :eof
	

:end 
	GOTO :eof