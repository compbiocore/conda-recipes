if "%ARCH%"=="32" (
    set PLATFORM=Win32
) else (
    set PLATFORM=x64
)

mkdir dll\%PLATFORM%\Release || goto :error
mkdir lib\%PLATFORM%\Release || goto :error

set mpc_root=%cd%
cd .. || goto :error

for %%d in (mpir, mpfr) do (
    mkdir %%d\dll\%PLATFORM%\Release || goto :error
    mkdir %%d\lib\%PLATFORM%\Release || goto :error

    REM copy libraries
    copy %LIBRARY_BIN%\%%d.dll %%d\dll\%PLATFORM%\Release\%%d.dll || goto :error
    copy %LIBRARY_LIB%\%%d.lib %%d\dll\%PLATFORM%\Release\%%d.lib || goto :error
    copy %LIBRARY_LIB%\%%d_static.lib %%d\lib\%PLATFORM%\Release\%%d.l || goto :errorib
)

REM copy headers
xcopy %LIBRARY_INC%\*.h mpir\lib\%PLATFORM%\Release\ /E || goto :error
xcopy %LIBRARY_INC%\*.h mpir\dll\%PLATFORM%\Release\ /E || goto :error
copy %LIBRARY_INC%\gmp-config.h mpir\lib\%PLATFORM%\Release\config.h || goto :error
copy %LIBRARY_INC%\gmp-config.h mpir\dll\%PLATFORM%\Release\config.h || goto :error
copy %LIBRARY_INC%\gmp-longlong.h mpir\lib\%PLATFORM%\Release\longlong.h || goto :error
copy %LIBRARY_INC%\gmp-longlong.h mpir\dll\%PLATFORM%\Release\longlong.h || goto :error

cd %mpc_root%\build.vc14 || goto :error

msbuild.exe /p:Platform=%PLATFORM% /p:Configuration=Release /p:PostBuildEvent="" mpc_lib\mpc_lib.vcxproj || goto :error
msbuild.exe /p:Platform=%PLATFORM% /p:Configuration=Release /p:PostBuildEvent="" mpc_dll\mpc_dll.vcxproj || goto :error

copy dll\%PLATFORM%\Release\mpc.lib %LIBRARY_LIB%\mpc.lib || goto :error
copy dll\%PLATFORM%\Release\mpc.dll %LIBRARY_BIN%\mpc.dll || goto :error
copy dll\%PLATFORM%\Release\mpc.pdb %LIBRARY_BIN%\mpc.pdb || goto :error

copy lib\%PLATFORM%\Release\mpc.lib %LIBRARY_LIB%\mpc_static.lib || goto :error

cd %mpc_root% || goto :error
copy src\mpc.h %LIBRARY_INC%\mpc.h || goto :error


REM testing
cd build.vc14 || goto :error
xcopy dll\%PLATFORM%\Release\mpc.* ..\dll\%PLATFORM%\Release\ /E || goto :error
mkdir dll_tests\%PLATFORM%\Release || goto :error

msbuild.exe /property:SolutionDir=..\..\ /property:OutDir=..\..\%PLATFORM%\Release\ /p:Platform=%PLATFORM% /p:Configuration=Release dll_tests\add_test_lib\add_test_lib.vcxproj || goto :error
copy %PLATFORM%\Release\test_lib.lib dll_tests\%PLATFORM%\Release\test_lib.lib || goto :error

for /d %%d in (dll_tests\*) do (
    for %%f in (%%d\*.vcxproj) do (
        msbuild.exe /property:SolutionDir=..\..\ /property:OutDir=..\..\%PLATFORM%\Release\ /p:Platform=%PLATFORM% /p:Configuration=Release %%f || goto :error
    )
)

REM for /r "%PLATFORM%\Release\" %%a in (*.exe) do ( %%~fa )
xcopy ..\tests\* %PLATFORM%\Release\ /E || goto :error
cd %PLATFORM%\Release || goto :error
treal.exe || goto :error
goto :EOF

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
