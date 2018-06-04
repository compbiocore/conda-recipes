:: Needed so we can find stdint.h from msinttypes.
set LIB=%LIBRARY_LIB%;%LIB%
set LIBPATH=%LIBRARY_LIB%;%LIBPATH%
set INCLUDE=%LIBRARY_INC%;%INCLUDE%

:: VS2008 doesn't have stdbool.h so copy in our own
:: to 'lib' where the other headers are so it gets picked up.
if "%VS_MAJOR%" == "9" (
    copy %RECIPE_DIR%\stdbool.h lib\
)

cmake -G "NMake Makefiles" ^
      -D CMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX% ^
      -D CMAKE_BUILD_TYPE=Release ^
      .
if errorlevel 1 exit 1

nmake install
if errorlevel 1 exit 1
