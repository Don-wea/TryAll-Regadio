# regadio-backend


## 📦 Detalles de Instalacion y Ejecucion
* Entorno virtual
  
  1. Crear entorno virtual  
      ```bash
      python -m venv .venv
      ```
  2. Activar entorno virtual  
      **linux/macOS**  

      ```bash
      source .venv/bin/activate
      ```

      **Windows**  

      ```bash
      source .venv/Scripts/activate
      .venv\Scripts\activate
      ```

      **Windows (PowerShell)**  

      ```bash
      .venv\Scripts\Activate.ps1
      ```
    
  1. Instalar dependencias
      ```bash
      pip install -r requirements.txt
      ```
      Para el login , si no funciona pip install django djangorestframework mongoengine bcrypt djangorestframework-simplejwt drf-yasg,pip install PyJWT

    <img src="../docs/export/backend/images/venv.png"/>


* Base de datos
      1. Asegurarse de que el servicio de mongoDB esté funcionando correctamente
      2. agregar datos dummy `python database/agregar_datos_dummy.py` esto crea una base de datos local y agregar archivos dummy
   
* Servidor
      1. `cd regadio_backend`
      2. `python manage.py makemigrations`
      3. `python manage.py migrate`
      4. `python manage.py runserver`


