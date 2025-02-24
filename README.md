# GivEnergy Data Downloader

🚀 A high-performance, multi-threaded Python script to fetch and store CSV data from the GivEnergy cloud platform. This script efficiently downloads inverter data across multiple dates and saves them in a structured `data/` directory.

## Features
✅ Fetches **GivEnergy inverter data** via API  
✅ Supports **single & multiple date ranges**  
✅ **Multi-threaded** for fast concurrent downloads  
✅ Saves **CSV files** in a structured `data/` directory  
✅ **Automatic retries** for failed downloads  
✅ Uses a **separate `config.json`** for secure credentials  

---

## 📦 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://gitlab.com/your-username/givenergy-data-downloader.git
cd givenergy-data-downloader
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```
> ⚠️ The script only requires Python's standard `requests` library. If needed, manually install it:  
> ```sh
> pip install requests
> ```

---

## ⚙ **Configuration**

Before running the script, **edit `config.json`** with your GivEnergy API credentials:

1️⃣ **Open `config.json`**
```json
{
    "base_url": "https://givenergy.cloud/inverter/CH2335G142/data/download",
    "headers": {
        "X-XSRF-TOKEN": "your_full_xsrf_token_here",
        "User-Agent": "your_user_agent_here"
    },
    "cookies": {
        "XSRF-TOKEN": "your_full_xsrf_token_here",
        "laravel_session": "your_laravel_session_here",
        "laravel_token": "your_laravel_token_here"
    }
}
```
2️⃣ **Replace placeholder values** with actual credentials.

---

## 🚀 **Usage**

### **Download Data for a Single Date**
```sh
python fetch_givenergy_data.py 2024-03-01
```

### **Download Data for a Date Range**
```sh
python fetch_givenergy_data.py 2024-03-01 2024-03-05
```

### **Where Are the Files Saved?**
- CSV files are automatically **saved in the `data/` directory**.
- Example structure:
  ```
  data/
    ├── system_data_2024-03-01.csv
    ├── system_data_2024-03-02.csv
    ├── system_data_2024-03-03.csv
  ```

---

## 🛠 **Troubleshooting**
### 1️⃣ **`config.json` Not Found**
- Ensure `config.json` exists in the same directory as the script.

### 2️⃣ **Request Errors or Authentication Failures**
- Double-check your **tokens & session values** in `config.json`.

### 3️⃣ **Connection Timeouts**
- Reduce `MAX_WORKERS` in the script (e.g., from `5` to `3`).

---

## 📜 **Contributing**
1. Fork the repository 🍴  
2. Create a new branch (`feature-name`) 🌱  
3. Commit your changes (`git commit -m "Added new feature"`) 🔥  
4. Push to the branch (`git push origin feature-name`) 🚀  
5. Open a **Merge Request** on GitLab 🎉  

---

## ⚖️ **License**
This project is **open-source** under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

### 👨‍💻 **Maintainers**
- **Your Name** ([Your GitLab Profile](https://gitlab.com/your-username))
