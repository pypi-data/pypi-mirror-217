import sys
import os

def create_project(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir)

    app_dir = os.path.join(project_dir, "app")
    os.makedirs(app_dir)

    errors_dir = os.path.join(app_dir, "errors")
    os.makedirs(errors_dir)

    templates_dir = os.path.join(app_dir, "templates")
    os.makedirs(templates_dir)

    public_dir = os.path.join(app_dir, "public")
    os.makedirs(public_dir)

    with open(os.path.join(project_dir, "manage.py"), "w") as f:
        f.write(''' # Add your manage code here:
# Example usage

from app.app import app

@app.route("/", methods=['GET'], secure=True)
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

MEDIA_URL = '/media/'
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
        
    with open(os.path.join(errors_dir, "400.html"), "w") as f:
      f.write('''<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Your request was invalid.</p>
</body>
</html>

      ''')

      with open(os.path.join(errors_dir, "401.html"), "w") as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>401</title>
  <style>
    .error-card {
  margin: 50px 0 0 50px;
}

.error-card .error-card-icon {
  width: 100px;
  border-radius: 8px 0 0 8px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #eee;
}

.error-card .error-card-content {
  width: 400px;
  border-radius: 0 8px 8px 0;
  border: 1px solid #ddd;
  padding: 10px 20px;
}

  </style>
</head>
<body>
  <div class="error-card d-flex flex-row">
    <div class="error-card-icon">
      <h4 class="display-4"><i class="bi bi-x-octagon-fill text-danger"></i></h4>
    </div>
    <div class="error-card-content">
      <h2>Error 401</h2>
      <p>You are not authrorized to view this page</p>
    </div>
  </div>
</body>
</html>
        ''')

      with open(os.path.join(errors_dir, "404.html"), "w") as f:
        f.write(''' <html>
<head>
    <title>404 Not Found</title>
</head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Arvo">
<style>
    
/*======================
    404 page
=======================*/


.page_404{ padding:40px 0; background:#fff; font-family: 'Arvo', serif;
}

.page_404  img{ width:100%;}

.four_zero_four_bg{
 
 background-image: url(https://cdn.dribbble.com/users/285475/screenshots/2083086/dribbble_1.gif);
    height: 400px;
    background-position: center;
 }
 
 
 .four_zero_four_bg h1{
 font-size:80px;
 }
 
  .four_zero_four_bg h3{
			 font-size:80px;
			 }
			 
			 .link_404{			 
	color: #fff!important;
    padding: 10px 20px;
    background: #39ac31;
    margin: 20px 0;
    display: inline-block;}
	.contant_box_404{ margin-top:-50px;}
</style>
<body>
    <section class="page_404">
        <div class="container">
            <div class="row">	
            <div class="col-sm-12 ">
            <div class="col-sm-10 col-sm-offset-1  text-center">
            <div class="four_zero_four_bg">
                <h1 class="text-center ">404</h1>
            
            
            </div>
            
            <div class="contant_box_404">
            <h3 class="h2">
            Look like you're lost
            </h3>
            
            <p>the page you are looking for not avaible!</p>
            
        </div>
            </div>
            </div>
            </div>
        </div>
    </section>
</body>
</html>

      ''')

    with open(os.path.join(errors_dir, "403.html"), "w") as f:
      f.write(''' <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403</title>
</head>
<style>
    @import url("https://fonts.googleapis.com/css?family=Montserrat:400,400i,700");
/* sorry for the scrambled mess */
 body {
	 display: flex;
	 align-items: center;
	 justify-content: center;
	 height: 100vh;
	 width: 100vw;
	 background: #eceff1;
	 font-family: Montserrat, sans-serif;
}
 .container {
	 background: white;
	 height: auto;
	 width: 40vw;
	 padding: 1.5rem;
	 box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.2);
	 border-radius: 0.5rem;
	 text-align: center;
}
 .container h1 {
	 font-size: 1.25rem;
	 margin: 0;
	 margin-top: 1rem;
	 color: #263238;
	 opacity: 0;
	 transform: translateX(-0.1rem);
	 animation: fadeIn 1s forwards 1.5s;
}
 .container p {
	 margin: 0;
	 margin-top: 0.5rem;
	 color: #546e7a;
	 opacity: 0;
	 transform: translateX(-0.1rem);
	 animation: fadeIn 1s forwards 1.75s;
}
 @media screen and (max-width: 768px) {
	 .container {
		 width: 50vw;
	}
}
 @media screen and (max-width: 600px) {
	 .container {
		 width: 60vw;
	}
}
 @media screen and (max-width: 500px) {
	 .container {
		 width: 80vw;
	}
}
 @keyframes fadeIn {
	 from {
		 transform: translateY(1rem);
		 opacity: 0;
	}
	 to {
		 transform: translateY(0rem);
		 opacity: 1;
	}
}
 .forbidden-sign {
	 margin: auto;
	 width: 4.6666666667rem;
	 height: 4.6666666667rem;
	 border-radius: 50%;
	 display: flex;
	 align-items: center;
	 justify-content: center;
	 background-color: #ef5350;
	 animation: grow 1s forwards;
}
 @keyframes grow {
	 from {
		 transform: scale(1);
	}
	 to {
		 transform: scale(1);
	}
}
 .forbidden-sign::before {
	 position: absolute;
	 background-color: white;
	 border-radius: 50%;
	 content: "";
	 width: 4rem;
	 height: 4rem;
	 transform: scale(0);
	 animation: grow2 0.5s forwards 0.5s;
}
 @keyframes grow2 {
	 from {
		 transform: scale(0);
	}
	 to {
		 transform: scale(1);
	}
}
/* slash */
 .forbidden-sign::after {
	 content: "";
	 z-index: 2;
	 position: absolute;
	 width: 4rem;
	 height: 0.3333333333rem;
	 transform: scaley(0) rotateZ(0deg);
	 background: #ef5350;
	 animation: grow3 0.5s forwards 1s;
}
 @keyframes grow3 {
	 from {
		 transform: scaley(0) rotateZ(0deg);
	}
	 to {
		 transform: scaley(1) rotateZ(-45deg);
	}
}
 
</style>
<body>
    <div class="container">
        <div class="forbidden-sign"></div>
        <h1><b>403</b></h1>
        <h1>Access to this page is restricted.</h1>
        <p>Ensure you have sufficient permissions to access the same.</p>
    </div>
</body>
</html>''')
      
    with open(os.path.join(errors_dir, "405.html"), "w") as f:
      f.write(''' <html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<style>
    * {
	font-family: Verdana;
	text-align:center;
}

h1 {
	font-size:4em;
}

</style>
<body>
    <br><br><br><br>
<br><h1>Error 405</h1><h2>Method not allowed.</h2>
    <p>The requested method is not allowed for this URL.</p>
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

