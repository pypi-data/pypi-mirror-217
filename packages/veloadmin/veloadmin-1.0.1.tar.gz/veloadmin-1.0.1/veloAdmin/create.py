import sys
import os

def create_project(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir)

    app_dir = os.path.join(project_dir, "app")
    os.makedirs(app_dir)

    templates_dir = os.path.join(app_dir, "templates")
    os.makedirs(templates_dir)

    public_dir = os.path.join(app_dir, "public")
    os.makedirs(public_dir)

    with open(os.path.join(project_dir, "manage.py"), "w") as f:
        f.write(''' # Add your manage code here:
# Example usage

from app.app import app

@app.route("/", methods=['GET'], secure = True)
async def home(request):
    return make_response("welcome to VeloWeb") ''')

    with open(os.path.join(app_dir, "wsgi.py"), "w") as f:
        f.write('''from app import app


if __name__ == "__main__":
    app.runserver() ''')

    with open(os.path.join(app_dir, "app.py"), "w") as f:
        f.write('''from veloweb import velo
app = velo()

@app.route("/", methods=["GET", "POST"], secure=True)
async def home(request):
    return app.render_template("index.html")
''')

    with open(os.path.join(app_dir, "settings.py"), "w") as f:
        f.write(''' # settings.py config

HOST = "127.0.0.1"  # default host by veloWEB on localhost
PORT = 8000 # default port by veloWEB on 8000
DEBUG = True # default debug value True for development

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0'] # You can add more hosts as per your requirements

# VeloWeb provides a inbuild database engine @nexus, NexusDB developed by @PyDev using Json/Application.
# @nexus is a fully manage and structured database and also compatible for production usage with,
# app.config['SET_APP_MODE'] = "Production"
# db.set_app(app.config['SET_APP_MODE'])

# Default configuration for @nexus 

DATABASES = {
        'default': {
            'ENGINE': 'velo.db.backends.nexus', # default database engine Nexus
            'NAME': 'YOUR_DB_NAME',
            'USER': 'USERNAME',
            'PASSWORD': 'PASSWORD_FOR_DB',
            'HOST': 'localhost'
        }
    }

MEDIA_URL= '/media/'
STATIC_URL = '/public/'
TEMPLATE_ENGINE = '/templates'
        ''')

    with open(os.path.join(app_dir, "__init__.py"), "w") as f:
        pass

    with open(os.path.join(app_dir, ".env"), "w") as f:
        f.write(''' SECRET_KEY = "your_secret_key" ''')

    with open(os.path.join(app_dir, "velo.json"), "w") as f:
        f.write(f'''{{
    "name": "{project_name}",
    "version": "1.0.0",
    "description": "Description of your project",
    "author": "Your Name",
    "email": "your@email.com",
    "app": {{
        "name": "Your App Name",
        "description": "Description of your app",
        "routes": [
        {{
            "url": "/",
            "methods": ["GET", "POST"],
            "secure": true,
            "handler": "app.home"
        }}
        ]
    }}
    }}''')


    with open(os.path.join(templates_dir, "index.html"), "w") as f:
        f.write(''' <!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to VeloWeb Server</title>

  <!-- Tailwind CSS -->
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

  <!-- Animation.js -->
  <script src="https://cdn.jsdelivr.net/npm/animation.js@2.4.2/dist/animation.min.js"></script>

  <style>
    /* Custom styling */
    .container {
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    .welcome-message {
      font-size: 3rem;
    }
  </style>
</head>

<body>
  <div class="container">
    <h1 class="welcome-message animate__animated animate__fadeInDown">
      Welcome to VeloWeb Server
    </h1>
    <p class="text-gray-500 mt-4">
      A lightweight and feature-rich web framework
    </p>
  </div>

  <script>
    // Animation.js usage
    const welcomeMessage = document.querySelector('.welcome-message');
    Animation.animate(welcomeMessage, 'animate__infinite', 'animate__heartBeat');
  </script>
</body>

</html>
 ''')

    js_dir = os.path.join(public_dir, "js")
    os.makedirs(js_dir)

    css_dir = os.path.join(public_dir, "css")
    os.makedirs(css_dir)

def main():
    if len(sys.argv) < 2 or sys.argv[1] != "startproject":
        print("Invalid command")
        return

    project_name = sys.argv[2]
    create_project(project_name)
    print(f"Project '{project_name}' created successfully!")

if __name__ == "__main__":
    main()

