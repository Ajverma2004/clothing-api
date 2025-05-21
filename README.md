# 🧠 SnapClothes Backend – Flask + MongoDB

This is the backend API service powering the **SnapClothes** AR fashion app. It handles product data management, category-based queries, search functionality, and banner image delivery. Built with **Flask** and **MongoDB**, this lightweight backend is hosted on [Fly.io](https://fly.io) and connects seamlessly with the mobile frontend.

---

## 🚀 Features

- 📦 **Product Management**
  - Fetch all products
  - Retrieve product by ID
  - Add new products
- 🧭 **Category-Based Filtering**
  - Get list of categories
  - Fetch products by category
- 🔍 **Search API**
  - Search products by name, description, or category
- 🖼️ **Banner Management**
  - Get banners per category
  - Add new banner images

---

## 🛠️ Tech Stack

- **Backend Framework:** Flask (Python)
- **Database:** MongoDB (with `pymongo`)
- **Hosting:** Fly.io
- **Security:** ObjectID conversion, basic validations
- **API Format:** RESTful JSON APIs

---

## 📂 API Endpoints

| Method | Endpoint                  | Description                            |
|--------|---------------------------|----------------------------------------|
| GET    | `/products`               | Get all products                       |
| GET    | `/product/<product_id>`   | Get a specific product by ID           |
| GET    | `/categories`             | Get list of all categories             |
| GET    | `/category/<name>`        | Get products by category               |
| GET    | `/search?query=<term>`    | Search products                        |
| POST   | `/add`                    | Add a new product                      |
| GET    | `/banners`                | Get all category banners               |
| POST   | `/banners`                | Add a new category banner              |

---

## 🌐 Deployment

Hosted on **Fly.io** using Docker containerization and exposed at a public endpoint to serve the SnapClothes Android app.

---

## 🔗 Linked Frontend

View the full SnapClothes project here:  
👉 [SnapClothes Mobile App Repo](https://github.com/Ajverma2004/SnapClothes)

---

## 📄 License

MIT License – Feel free to reuse and extend with attribution.
