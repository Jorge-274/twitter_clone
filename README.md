# twitter_clone
Proyecto Django - Instalación y Configuración
Requisitos
Python 3.10+ (o compatible)

Conda instalado (recomendado Miniconda o Anaconda)

1. Clonar el repositorio (opcional)
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

2. Crear el entorno virtual con Conda

    conda create -n env-x python=3.12

    conda activate env-x
3. Instalar las dependencias

    pip install -r requirements.txt
4. Configurar el proyecto Django

    python manage.py makemigrations

    python manage.py migrate
5. Crear un superusuario:

   python manage.py createsuperuser
   
   -(Te va a pedir email, username y contraseña.)
6. Correr el servidor de desarrollo

    python manage.py runserver
- Abrí tu navegador y andá a:
http://127.0.0.1:8000/
