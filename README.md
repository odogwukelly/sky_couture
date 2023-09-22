# SkyCouture

SkyCouture is a comprehensive e-commerce platform designed to provide a seamless shopping experience for high-end fashion enthusiasts. Our project aims to connect users with a curated selection of premium fashion products, offering a user-friendly interface, secure payment processing, and personalized recommendations.

## Key Features

### User Registration

- Users can create accounts by providing the following information:
  - Username
  - Email
  - Password
  - Date of Birth
  - Gender

- Validation ensures that usernames and emails are unique.

- Passwords are securely hashed before storage to protect user data.

### User Login

- Registered users can securely log in using their email and password.

- Authentication is handled securely, and users are remembered if they choose to do so.

### Password Reset

- Users who forget their passwords can request a password reset via email.

- A time-limited token is generated for password reset links.

- Security measures are implemented to prevent misuse of reset tokens.

### View Product Details

- Users can view detailed information about products before making a purchase.

- This feature allows users to choose their preferred product options, such as color and quantity, before adding items to their cart.

### Add to Cart / Delete from Cart

- Users can easily add products to their shopping cart for convenient shopping.

- If users change their minds, they can also delete products from the cart with ease.

### Clear Cart

- Users have the option to clear their entire shopping cart at once, providing a fresh start for their shopping experience.

These features collectively form the foundation of our e-commerce platform, demonstrating our team's dedication to web development and delivering value to users. We aim to provide a seamless and secure shopping experience for our customers.


## File Descriptions

### Flask Routes
- Flask routes are a fundamental concept in building web applications with Flask. They provide a way to define the structure and behavior of your web application, making it possible to handle different URLs and HTTP methods effectively.

### Data Models
- In a web application, data models represent the structure of your data and how it's stored in a database. These models are typically defined as Python classes. For example, in a simple e-commerce application, you might have a User model to represent user data, and a Product model to represent product data.

### Templates
-  templates are files that contain dynamic content and are used to generate HTML responses to be sent to clients (typically web browsers). Flask uses a templating engine to render these templates, allowing you to inject dynamic data into the HTML to create dynamic web pages. Templates are a crucial part of separating the presentation layer from the application logic, following the principles of the Model-View-Controller (MVC) or Model-View-Template (MVT) architecture

