
![Logo](https://png.pngtree.com/background/20210711/original/pngtree-music-and-landscape-poster-background-picture-image_1123969.jpg)


# Song REST API

Django REST API for reading, updating, deleting, and creating songs. This project allows user login through custom JWT authentication.


## Requirements

- Python 3.8
- PostgreSQL 14.5
- Postman

## Features

- User register
- User login (JWT Authentication)
- CRUD Operations on Songs model
- Connection to public API to retrieve a random number


## Authors

[@fandemisterling100](https://www.github.com/fandemisterling100)


## Installation

Create a postgreSQL DB

```bash
  sudo -u postgres psql postgres
```
```bash
  CREATE ROLE dbadmin WITH LOGIN ENCRYPTED PASSWORD 'password' CREATEDB CREATEROLE REPLICATION SUPERUSER;
```
```bash
  CREATE DATABASE demodb WITH OWNER dbadmin ENCODING 'UTF8';
```
```bash
  GRANT ALL PRIVILEGES ON DATABASE demodb TO dbadmin;
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_URL`

Following the example on the *Installation* section:

`DATABASE_URL=postgres://dbadmin:password@localhost/demodb`




## Run Locally

Clone the project

```bash
  git clone https://link-to-project .
```

Install dependencies

```bash
  pip install -r requirements/local.txt
```

Run migrations
```bash
  python manage.py migrate
```
Start the server

```bash
  python manage.py runserver
```
In case you need it
```bash
 yarn
 yarn run build
```

## API Reference

#### 1. User Register

```http
  POST /api/v1/register
```
Body parameters:
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. User email |
| `password` | `string` | **Required**. user password |


#### 2. User Login
This endpoint returns the access token you will need to send requests to the server. The lifetime of this token is 20 minutes.

```http
  POST /api/v1/public/token
```
Body parameters:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email` | `string` | **Required**. User email |
| `password` | `string` | **Required**. user password |


#### 3. Create Song

```http
  POST /api/v1/songs/create
```

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |

Body parameters:
| Parameter | Type     | Description                       | Example                       |
| :-------- | :------- | :-------------------------------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of the song | "Satellite" |
| `artist`      | `string` | **Required**. Artist of the song | "Khalid" |
| `album`      | `string` | **Required**. Album of the song | "Satellite" |
| `duration`      | `string` | **Required**. Duration in miliseconds | "00:03:07" |
| `favorite`      | `boolean` | **Required**. Indicates if it's a user's favorite song | false |
| `private`      | `boolean` | **Required**. Indicates if this song is private or public | true |

#### 4. Update Song

```http
  PUT /api/v1/songs/<pk>/update
```

*The pk in the URL means the Id of item to update.*

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |

Body parameters:
| Parameter | Type     | Description                       | Example                       |
| :-------- | :------- | :-------------------------------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of the song | "Satellite" |
| `artist`      | `string` | **Required**. Artist of the song | "Khalid" |
| `album`      | `string` | **Required**. Album of the song | "Satellite" |
| `duration`      | `string` | **Required**. Duration in miliseconds | "00:03:07" |
| `favorite`      | `boolean` | **Required**. Indicates if it's a user's favorite song | false |
| `private`      | `boolean` | **Required**. Indicates if this song is private or public | true |


#### 5. Delete Song

```http
  DEL /api/v1/songs/<pk>/delete
```

*The pk in the URL means the Id of item to delete.*

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |

#### 6. Get all songs

You will only be able to get songs created with the logged user.

```http
  GET /api/v1/songs?page=<n>
```

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |


If you want to control the paginator you can add the *query parameter* to the request:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `page`      | `int` | Page number |

#### 7. Get song by Id
You will only be able to get songs created with the logged user or public songs.

```http
  GET /api/v1/songs/<pk>
```
*The pk in the URL means the Id of item to update.*

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |

#### 8. Get song by Id
You will only be able to get songs created with the logged user or public songs.

```http
  GET /api/v1/songs/<pk>
```
*The pk in the URL means the Id of item to update.*

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |

#### 9. Get all public songs

```http
  GET /api/v1/songs/public?page=<n>
```
If you want to control the paginator you can add the *query parameter* to the request:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `page`      | `int` | Page number |

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |


#### 10. Generate random number

```http
  GET /api/v1/random-number
```

Add to the header of the request your access token:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization Bearer <ACCESS_TOKEN>`      | `string` | **Required**. API ACCESS_TOKEN |




## Running Tests

To run tests, run the following command

```bash
  coverage run -m pytest --ignore=node_modules
```

To display coverage:
```bash
  coverage report -m
```
Current coverage: 96%


## Usage/Examples

To facilitate the testing process I have created this workspace on Postman where you can use the same requests with which I have validated the project

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/18145912-1b4bf096-97b8-4580-965c-50f1c5cdb372?action=collection%2Ffork&collection-url=entityId%3D18145912-1b4bf096-97b8-4580-965c-50f1c5cdb372%26entityType%3Dcollection%26workspaceId%3Da1fda87e-219e-4982-90eb-8381580f7fc6)


## Support

For support, email mi.jaramillo@uniandes.edu.co

