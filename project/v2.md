# JB Fashion - Inventory Management App
## Video Demo
Presentation video can be find here:  https://youtu.be/9ETm6og0LxE and the link to the slides are here: https://docs.google.com/presentation/d/1SCXj_s2FipulNxH_9waVLNiDHoyGs7FRyJkhB5Gmj0E/edit?usp=sharing

## Description
This web app was created as an in-house app for a local fashion store. It will be used to keep track of customers and orders, as well as the status of the orders. The application will make it easier to register customers and their required details. This application can also record all orders placed by any customer.

The application is designed in such a way that login is required, so we created an admin account with a username and password. The account cannot be deleted, but the password can be changed. The admin can add additional users who can access the application and can also delete the user. Any user can add, delete, and modify customers and orders.

Here is default admin username and password:

```
username: admin
password: random-string
```

This is a multi-page application built with the Flask framework with Vanila javascript, CSS, and HTML. As previously said, you must login to access the application. The login page handles this. When a user enters a credential using the username and password, it is validated and the user is sent to the home page if successful, otherwise to the login page with an error message displayed. In summary, the programme has five pages or sections: login, home, customer, order, and settings.

Except for the login page, each page/section has a side navigation that users can utilise to navigate from one page/section to another. The home page contains connections to other pages/sections as well as a brief summary of what may be done on those pages/sections.

Customers, orders, and users are listed on the customer, order, and setting pages, respectively. Additionally, the user has the ability to add, delete, or alter any of the items. We use an accordion user interface (ui) to display a list of objects (such as customers, orders, and users). When you click on an item in the list, a panel appears that displays all of the item's associated details. Inside the panel, there are two visible buttons: delete and enable edit. To prevent accidental editing, all inputs, textareas, and select/dropdown elements are disabled once the panel is opened. As a result, the user cannot edit an item until the enable edit button is clicked, which allows the user to modify the item. When the enable edit button is clicked, it disappears and the save button is displayed to the user. This button will be used to save the item once the edit is complete.

To create a customer, you must provide the following information: first name, last name, address, and gender. The following information is optional: email, phone number, measurement (the customer's cloth measurement), and the last, comment, which is for any other information that needs to be captured.

As for the order, to create a new order, you must first specify the consumer to whom the offer applies. Also required is the following information: type (one of the following: shirt, t-shirt, trouser, belt, wallet, and others), delivery address, total cost, amount paid, and status (one of the following: started, in progress, completed, closed, and cancelled). The following details are optional and can be supplied: order date, delivery date, and comment—a space for any further information about the item—are all included.

### Technologies used:
Here are list of libraries, frameworks, languages, icons etc used in developing this web application:
- Flask Framework
- Sqlite3
- Google icons
- Logo.com generator (to generate the company logo)
- Languages
    - Python
    - CSS3
    - JavaScript
    - HTML5

### Design

The application can be divided into three layers, namely:

- view (frontend)
- (restful) api
- data

The interaction among all these layers is depicted in the diagram below:

![](./static/logos/readme/design-structure.png)

#### View Layer

This is the layer of the application that serve the static files and templates. Basically, this is the part responsible for the frontend ui. There are 4 routes in the view layer, and they are as follows:
1. login [path: `/login`] : renders login's page
2. index (or home) [path: `/`] : renders home's page
3. customer [path: `/customer`] : renders customer's page
4. order [path: `/order`] : renders order's page
5. settings [path: `/settings`] : renders setting's page

When these routes were requested, to retrieved the necessary data, a connection to the database will be established. The render_template method was used to transmit this data to the html page. These data were then handled appropriately.

The `templates` folder contains five flask templates, one for each view. The table below shows which templates are associated with which views:

| View     | Path        | Template       |
|----------|-------------|----------------|
| index    | `/`         | index.html     |
| login    | `/login`    | login.html     |
| customer | `/customer` | customer.html  |
| order    | `/order`    | order.html     |
| setting  | `/settings` | setting.html   |

The `static` folder contain the following subfolders:
- `css`: all files relating to styling are placed here.
- `scripts`: all javascript files are placed here
- `logos`: all images, logos etc used in this project are placed here

![](./static/logos/readme/static-files-structure.png)

Using the fetch API to communicate with the Restful API, and we also performed some DOM modifications using JavaScript.

#### Data Layer

The data layer is in charge of maintaining, storing, and modifying the data that the application uses. Three tables are present in the system, which are customers, orders, and users. The `schema.sql` file contains the definitions for the SQL schema for each of these tables. When the application launches, this schema will be loaded, and if the tables don't already exist, they will be created inside the database (named `jbfashion.db`). The table representation (including its columns) and their relationships are depicted in the diagram below.

![](./static/logos/readme/datamodel.png)

The customer id is used as a foreign key in the order table, as seen in the diagram above. This ensures that each other must be associated with a customer.

#### Restful API

This is the layer that utilises and accesses data via HTTP requests. It is built on REST, which is an architectural style and approach to communication that is commonly used in web services development. We represent each of our tables using a data transfer object (dto), therefore we generated user dto, customer dto, and order dto. This object's serialisation was also defined alongside its class definition. This allows us to simply convert the database response to json, which will be included in the restful api response. We regard each table as a resource, therefore we use the GET, PUT, POST, and DELETE methods on each one. [See below for the documentation of the restful api](#Restful-API-Documentation).

### How To run the application

#### Prerequisites
- Python v3.11
- sqlite3
- modern browser
- terminal

#### Run
To start the application, do the following:

- clone (or download) the application from this repository:
- open a terminal and cd in to the root of the application
- and lastly execute the command below

```
flask run
```
- if all the prerequisites are met, you should see the running address of the application. Type this address in your browser and you should be able to reach the application.
- for the first time, don't forget to use the provided username and password.
```
username: admin
password: random-string
```

## TODO
- [ ] address at which Add the capability to search, filter, sort and paginate on each of the tables
- [ ] Turn the application into single page app
- [ ] Show more intuitive error message
- [ ] Finish the documentation of the Restful API

------------------------------------

# Restful API Documentation

## 1. Customers API:

These are list of api used to interact with the Customers table:

### A. Get list of all customers
| METHOD | ENTRYPOINT         | Authorisation                        |
|--------|--------------------|--------------------------------------|
| Get    | `/api/customers`   | `Authorization: Basic <credentials>` |


| Status | Response                                      |
|--------|-----------------------------------------------|
| 200    | ![](./static/logos/readme/customers-json.png) |
| 400    | Bad User Request                              |
| 401    | Unauthorised User                             |
| 500    | Internal Server Error                         |

### B. Create a customer
| METHOD | ENTRYPOINT          | Authorisation                        | Body |
|--------|---------------------|--------------------------------------|------|
| Post    | `/api/customers`   | `Authorization: Basic <credentials>` | ![](./static/logos/readme/customer-create-request.png) |


| Status | Response                                                |
|--------|---------------------------------------------------------|
| 201    | ![](./static/logos/readme/customer-create-response.png) |
| 400    | Bad User Request                                        |
| 401    | Unauthorised User                                       |
| 500    | Internal Server Error                                   |


### C. Get details of a specific customer
| METHOD | ENTRYPOINT              | Authorisation                        | Parameter         |
|--------|-------------------------|--------------------------------------|-------------------|
| Get    | `/api/customers/<id>`   | `Authorization: Basic <credentials>` | _id_ is an integer|

| Status | Response                                                |
|--------|---------------------------------------------------------|
| 200    | ![](./static/logos/readme/customer-create-response.png) |
| 400    | Bad User Request                                        |
| 401    | Unauthorised User                                       |
| 500    | Internal Server Error                                   |

### D. Update a specific customer
| METHOD | ENTRYPOINT              | Authorisation                        | Parameter         | Body |
|--------|-------------------------|--------------------------------------|-------------------|------|
| Put    | `/api/customers/<id>`   | `Authorization: Basic <credentials>` | _id_ is an integer| ![](./static/logos/readme/customer-create-request.png) |


| Status | Response                                                |
|--------|---------------------------------------------------------|
| 200    | ![](./static/logos/readme/customer-create-response.png) |
| 400    | Bad User Request                                        |
| 401    | Unauthorised User                                       |
| 500    | Internal Server Error                                   |

### C. Delete a specific customer
| METHOD | ENTRYPOINT              | Authorisation                        | Parameter         |
|--------|-------------------------|--------------------------------------|-------------------|
| Delete | `/api/customers/<id>`   | `Authorization: Basic <credentials>` | _id_ is an integer|


| Status | Response               |
|--------|------------------------|
| 204    | no-content             |
| 400    | Bad User Request       |
| 401    | Unauthorised User      |
| 500    | Internal Server Error  |

## 2. Orders API

These are list of api used to interact with the Orders table:

### A. Get list of all orders
| METHOD | ENTRYPOINT      | Authorisation                        |
|--------|-----------------|--------------------------------------|
| Get    | `/api/orders`   | `Authorization: Basic <credentials>` |


| Status | Response                                   |
|--------|--------------------------------------------|
| 200    | ![](./static/logos/readme/orders-json.png) |
| 400    | Bad User Request                           |
| 401    | Unauthorised User                          |
| 500    | Internal Server Error                      |

### B. Create an order
| METHOD | ENTRYPOINT    | Authorisation                        | Body |
|--------|---------------|--------------------------------------|------|
| Post   | `/api/orders` | `Authorization: Basic <credentials>` | ![](./static/logos/readme/order-create-request.png) |


| Status | Response                                             |
|--------|------------------------------------------------------|
| 201    | ![](./static/logos/readme/order-create-response.png) |
| 400    | Bad User Request                                     |
| 401    | Unauthorised User                                    |
| 500    | Internal Server Error                                |


### C. Get details of a specific order
| METHOD | ENTRYPOINT          | Authorisation                        | Parameter         |
|--------|---------------------|--------------------------------------|-------------------|
| Get    | `/api/order/<id>`   | `Authorization: Basic <credentials>` | _id_ is an integer|


| Status | Response                                             |
|--------|------------------------------------------------------|
| 200    | ![](./static/logos/readme/order-create-response.png) |
| 400    | Bad User Request                                     |
| 401    | Unauthorised User                                    |
| 500    | Internal Server Error                                |

### D. Update a specific order
| METHOD | ENTRYPOINT          | Authorisation                        | Parameter         | Body |
|--------|---------------------|--------------------------------------|-------------------|------|
| Put    | `/api/order/<id>`   | `Authorization: Basic <credentials>` | _id_ is an integer| ![](./static/logos/readme/order-create-request.png) |


| Status | Response                                             |
|--------|------------------------------------------------------|
| 200    | ![](./static/logos/readme/order-create-response.png) |
| 400    | Bad User Request                                     |
| 401    | Unauthorised User                                    |
| 500    | Internal Server Error                                |

### C. Delete a specific order
| METHOD | ENTRYPOINT          | Authorisation                        | Parameter         |
|--------|---------------------|--------------------------------------|-------------------|
| Delete | `/api/order/<id>`   | `Authorization: Basic <credentials>` | _id_ is an integer|


| Status | Response               |
|--------|------------------------|
| 204    | no-content             |
| 400    | Bad User Request       |
| 401    | Unauthorised User      |
| 500    | Internal Server Error  |
```

## 3. Users API

```
TODO
```
