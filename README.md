#### Django Rest Framework (DRF)

Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Python using the Django web framework. It provides a comprehensive set of tools and features that make it easier for developers to create robust and efficient RESTful APIs.

Some key features of Django Rest Framework include:

- **Serializers**: DRF provides serializers to convert complex data, such as Django models, querysets, or Python objects, into JSON or XML for API responses. They also handle deserialization, allowing data to be converted back to native Python data types for processing.

- **Viewsets and Views**: DRF offers powerful view classes, such as Viewsets and Views, which handle the logic for processing HTTP methods like GET, POST, PUT, PATCH, and DELETE for different API endpoints.

- **Authentication and Permissions**: DRF includes various authentication methods like Token Authentication, Basic Authentication, and JSON Web Tokens (JWT) to secure APIs. It also supports fine-grained permissions to control access to resources.

- **Pagination**: DRF allows easy configuration of pagination for API responses, enabling the handling of large datasets efficiently.

- **Filtering, Searching, and Ordering**: DRF provides filter backends to facilitate data filtering, searching, and ordering of API results, enhancing the API's usability.

Overall, Django Rest Framework is widely adopted in the Python and Django community due to its ease of use, extensive documentation, and versatility in building high-quality and scalable Web APIs. It provides a solid foundation for developers to create RESTful APIs with minimal boilerplate code, allowing them to focus on delivering functional and feature-rich applications.

#### System Requirements

To build web applications with DRF you will need to include the following requirements on your system:

- Python 3.10 or lattest version;
- Pip 22.0 or lattest version;
- Virtualenv 20.19 or lattest version;

#### Quick Install

This guide aims to jump start the project settings and bring a fast hands-on DRF Project. However, to enable and run the project, some commands are still required.

- **Step 1** - Create a virtual python environment to install all required dependencies:
~~~
    python3 -m venv venv
~~~
- **Step 2** - Activate the virtual python environment:
~~~
    . venv/bin/activate
~~~
- **Step 3** - Install all dependencies:
~~~
    pip install -r requirements.txt
~~~
  **Step 4** - Create file .env of root project and install dependencies! ;)
~~~
    # Exemplo de configurações para banco de dados
    DB_ENGINE=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=

    # Outras configurações  
    SECRET_KEY=
    DEBUG=True
~~~
- **Step 5** - Run internal server and fun! ;)
~~~
    python manage.py runserver
~~~
  **Step 6** - Create super user! ;)
~~~  
    python manage.py createsuperuser
~~~