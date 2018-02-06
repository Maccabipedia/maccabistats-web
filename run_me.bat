pushd %~dp0

set FLASK_DEBUG=1
set FLASK_APP=maccabistats_web\__init__.py
flask run --host=0.0.0.0

popd