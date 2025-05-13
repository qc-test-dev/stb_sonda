

CORRER EN AMBIENTE VIRTUAL SOLAMENTE(llamarlo venv, por convención del proyecto)
dentro del ambiente virtual instalar librerias pip
pip install -r requirements.txt

** necesario migrar BBDD 

python manage.py migrate
python manage.py loaddata datos.json
python manage.py runserver 8080 (o puede ser en 8081)


2- ws-scrcpy  ejecutar servidor con npm start (npm install -g ws-scrcpy, para instalar)
** antes de iniciar la apk web de Django para poder ver los streams de los dispos es necesarioejecutar ws-scrcpy


****************

pendientes
1- refactorizar el codigo
2- requiremtnst.txt----- HECHO
LUIS 3- agregar control rcu  CUANDO SE ABRA VENTANA DE STREAM QUE SEA MAS grande Y TENGA rcu a lado
3- el stream de rtmp, en vez de ws-scrcpy  ( aún no iniciar)
LUIS 4- el stream mas grande


LUIS
Panel de dispostivos cambiar en el titulo, en vez de que diga STB que diga dispositivos.
dispositivos conectados....e nla pantalla media, quitar STB

Alberto/Luis
1-ftp de versiones. crear apk ftp para guardar versiones
2-API para subir versiones a FTP o Script SSH..
3- REFACTOR codigo Y QUITAR TEMPLATE ANTIGUOS


Luis
2- luis crear nueva apk web en este proyecto para manuales de instalacion FW, APK, para todas las marcas de STB y TV
