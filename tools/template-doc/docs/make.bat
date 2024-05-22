@ECHO OFF

pushd %~dp0

REM ###############################################################################
REM - Command file for Sphinx documentation
REM - Essentially an abstracted form of `sphinx-build -b html source_dir build_dir`
REM - Originally generated via `sphinx-quickstart`
REM - Requires make: `choco install make -y`
REM - Double clicking the .bat == `make html`
REM - On success: ENTER to quit, or "b" to launch build index.html
REM ###############################################################################

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build

REM If no argument is provided, default to 'html'
if "%1" == "" (
	set TARGET=html
) else (
	set TARGET=%1
)

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://sphinx-doc.org/
	echo.
	pause
	exit /b 1
)

%SPHINXBUILD% -M %TARGET% %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
if errorlevel 1 (
	echo.
	echo.Build failed. Please check the output above for details.
	echo.
	pause
	goto end
) else (
	echo.
	echo.Build succeeded. The documentation has been generated at:
	echo.%~dp0%BUILDDIR%\index.html
	echo.
	set /p userInput="Press 'B' to launch 'build/html/index.html', or ENTER to quit: "
	if /i "%userInput%"=="b" (
		start %~dp0%BUILDDIR%\html\index.html
	)
)

:end
popd
