# PetCare Chile 🐾

**Marketplace de servicios para mascotas desarrollado con Django.**

PetCare Chile es una plataforma web que permite explorar servicios para mascotas, consultar sus detalles y organizar solicitudes mediante un carrito. También incorpora registro de usuarios, perfiles y herramientas de administración para gestionar los servicios publicados.

## 📌 Funcionalidades principales

### Catálogo de servicios
- Visualización de servicios disponibles.
- Búsqueda por nombre, descripción y código.
- Filtrado por categoría.
- Ordenamiento por nombre y precio.
- Paginación de resultados.
- Vista individual con información detallada de cada servicio.

### Usuarios
- Registro de nuevos usuarios.
- Inicio y cierre de sesión.
- Edición del perfil.
- Información de RUT y teléfono.
- Roles de cliente y proveedor.

### Carrito de solicitudes
- Agregar servicios al carrito.
- Actualizar cantidades.
- Eliminar servicios.
- Vaciar el carrito.
- Almacenamiento mediante sesiones de Django.

### Administración
- Gestión protegida de servicios.
- Creación de servicios.
- Edición de servicios existentes.
- Eliminación de servicios.
- Administración de categorías y servicios mediante Django Admin.

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.13 | Lenguaje de programación |
| Django 5.2 | Framework backend |
| SQLite | Base de datos |
| HTML5 | Estructura de páginas |
| Bootstrap 5 | Diseño de interfaces |
| Pillow | Manejo de imágenes |
| python-dotenv | Variables de entorno |
| Git y GitHub | Control de versiones y colaboración |

## 📂 Estructura del proyecto

```text
PetCare-Chile/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── servicios/
│   ├── management/
│   │   └── commands/
│   │       └── poblar_datos.py
│   ├── migrations/
│   ├── templates/
│   │   └── servicios/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── usuarios/
│   ├── migrations/
│   ├── templates/
│   │   └── usuarios/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## ⚙️ Instalación y configuración

### 1. Requisitos previos

- Python 3.13 o compatible.
- Git.
- Un editor de código, como Visual Studio Code.

### 2. Clonar el repositorio

```bash
git clone https://github.com/bull-cpu/PetCare-Chile.git
cd PetCare-Chile
```

### 3. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

### 5. Configurar las variables de entorno

Crear un archivo `.env` en la carpeta principal, tomando como referencia `.env.example`.

Contenido:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True
```

Reemplazar `tu_clave_secreta` por una clave secreta propia.

**Importante:** No subir el archivo `.env` a GitHub. Este archivo contiene información privada. El repositorio incluye `.env.example` como plantilla.

### 6. Aplicar las migraciones

```powershell
python manage.py migrate
```

### 7. Cargar los datos iniciales

```powershell
python manage.py poblar_datos
```

Este comando carga las categorías y los servicios de ejemplo del proyecto.

### 8. Crear un superusuario

```powershell
python manage.py createsuperuser
```

Seguir las instrucciones para configurar las credenciales del administrador.

### 9. Ejecutar el servidor

```powershell
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

## 🔐 Administración de Django

Para acceder al panel administrativo:

http://127.0.0.1:8000/admin/

Ingresar con las credenciales del superusuario creado anteriormente.

## 🧪 Pruebas automatizadas

El proyecto incorpora pruebas automatizadas para verificar el funcionamiento de sus aplicaciones.

Ejecutar:

```powershell
python manage.py test
```

La versión actual del proyecto cuenta con **20 pruebas automatizadas aprobadas**.

## 🗺️ Rutas principales

| Ruta | Funcionalidad |
|---|---|
| `/` | Catálogo de servicios |
| `/servicio/<codigo>/` | Detalle de un servicio |
| `/carrito/` | Carrito de solicitudes |
| `/usuarios/registro/` | Registro |
| `/usuarios/login/` | Inicio de sesión |
| `/usuarios/logout/` | Cierre de sesión |
| `/usuarios/perfil/editar/` | Edición del perfil |
| `/administracion/servicios/` | Administración de servicios |
| `/admin/` | Panel administrativo de Django |

## 👥 Equipo de desarrollo

Proyecto desarrollado colaborativamente por:

- **Joaquín Toro**
- **Alexandra Pedrero**

Se utiliza Git y GitHub para organizar el trabajo mediante ramas, commits y Pull Requests.

## 📄 Licencia

Proyecto desarrollado con fines académicos.
