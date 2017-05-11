#!/bin/bash
clear
echo "PURGANDO ARCHIVOS"
rm -r __pycache__/
rm -r db/__pycache__/
rm examenes.db
echo "SUBIENDO"
git add . && git commit -m "Correcciones generales" && git push && git push heroku master
echo "LISTO :-)"
