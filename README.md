# 🛡️ Image Moderation API

A secure, token-authenticated **Image Moderation API** built using **FastAPI** with **MongoDB** integration for tracking token usage. Includes a minimal frontend to test moderation and manage tokens. The system simulates content moderation and provides admin/user role separation.

---

## 📌 Project Description

This project implements an **Image Moderation API** that allows users to upload images and receive moderation feedback. Admins can generate and revoke tokens. The API uses **FastAPI** with **Bearer Token authentication** and stores all token data and usage logs in **MongoDB**. A lightweight frontend (HTML/CSS/JS) enables user-friendly interaction with the system.

---

### 🎯 Objectives Addressed

- **API Design & Security**  
  Developed a RESTful API with secure bearer token authentication, restricting access to admin/user roles appropriately.

- **Token Management & Tracking**  
  MongoDB is used to store tokens and log all moderation requests made by users.

- **Moderation Endpoint**  
  A `/moderate` endpoint accepts image uploads and returns a dummy moderation result.

- **Frontend Integration**  
  Simple and responsive frontend built with HTML/CSS/JS to support both user uploads and admin token actions.

- **Deployment**  
  The project has been deployed using Railway with both backend and frontend hosted live.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

## ENV
MONGO_URI=mongodb+srv://sumayahashim559:sumaya123@imagemoderation.fq4nd1s.mongodb.net/?retryWrites=true&w=majority&appName=imagemoderation
DATABASE_NAME=image_moderation
SECRET_KEY=supersecret

```bash
git clone https://github.com/your-username/image-moderation-api.git
cd image-moderation-api


