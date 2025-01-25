# **Lexora**

![Lexora Logo](Hilti_Hackathon/Lexora/lexora-ui/public/lexora.png)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/Byte-Crfat-AI/Hilti_Hackathon/actions)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## **Table of Contents**
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

---

## **1. Overview**
Introducing Lexora, an AI-driven database management system. Ever thought of searching a file based on the content inside rather than the metadata? Lexora does that. It helps you to search, sort, and filter files based on the keywords present inside the file.

---

## **2. Features**
Lexora is capable of handling:
- Text data
- Images
- Audio 
- CSV

---

## **3. Installation**
Step-by-step instructions to install and set up the project.

### **Prerequisites**
- Python 3.10.11 (For RASA)

### **Installation Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/Byte-Crfat-AI/Hilti_Hackathon.git
   ```

2. To run the RASA server (For Windows) (Make sure the below venv is created with Python 3.10.11):
   ```bash
   python -m venv .venv
   .venv/scripts/activate
   pip install -r requirements.txt
   cd Lexora/Retrival/RASA
   rasa run --enable-api -m models\20250122-121655-isometric-cantaloupe.tar.gz
   ```

3. To start using Lexora:
   ```bash
   python -m venv venv
   venv/scripts/activate
   pip install -r requirements.txt
   cd Lexora/lexora-ui
   npm run dev
   ```

Your local server will be running, and you will be able to use Lexora.

[Download Target Data](https://drive.google.com/file/d/1buLZLJAmGTpsXzANf45K6VBmIOwh8jlj/view?usp=sharing)