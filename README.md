# 🔐 Secure Cloud Video Storage

Mô phỏng hệ thống lưu trữ video đám mây an toàn sử dụng các kỹ thuật An toàn & Bảo mật Thông tin.

## ✨ Tính năng

* 📤 Upload video an toàn
* 📥 Download video an toàn
* 🔒 Mã hóa AES-GCM
* 🔑 Trao đổi khóa RSA
* ✍️ Chữ ký số (Digital Signature)
* 🛡️ Kiểm tra toàn vẹn dữ liệu (SHA-256)
* 🚫 Chống Replay Attack
* 📝 Security Logging
* 🌐 Mô phỏng lỗi mạng (Packet Loss)
* 🖥️ Giao diện Client & Server bằng Tkinter

---

## 🏗️ Kiến trúc hệ thống

Client
↓
RSA Key Exchange
↓
AES Session Key
↓
Encrypted Video
↓
Cloud Server

---

## 🔐 Cơ chế bảo mật

| Cơ chế            | Mô tả                    |
| ----------------- | ------------------------ |
| AES-GCM           | Mã hóa video             |
| RSA               | Trao đổi khóa phiên      |
| Digital Signature | Xác thực metadata        |
| SHA-256           | Kiểm tra toàn vẹn        |
| Anti-Replay       | Chống gửi lại gói tin    |
| Security Log      | Ghi nhận sự kiện bảo mật |

---

## 🌐 Chế độ mạng

### NORMAL

Upload/Download hoạt động bình thường.

```text
ACK
```

### PACKET LOSS

Mô phỏng mất gói tin.

```text
NACK
```

---

## 📂 Cấu trúc thư mục

```text
client/
server/
crypto/
logs/
keys/
cloud_storage/
test_files/
```

---

## 🚀 Cách chạy

### 1. Clone dự án

```bash
git clone https://github.com/lsdai1411/secure-cloud-video-storage.git
cd secure-cloud-video-storage
```

### 2. Cài thư viện

```bash
pip install -r requirements.txt
```

### 3. Khởi động Server

```bash
python server/server_gui.py
```

### 4. Khởi động Client

```bash
python client/client_gui.py
```

---

## 🧪 Demo

### Upload thành công

```text
SERVER: ACK
```

### Mô phỏng lỗi mạng

```text
SERVER: NACK
```

---

## 📸 Giao diện

### Server GUI

(Thêm ảnh sau)

### Client GUI

(Thêm ảnh sau)

---

## 👨‍💻 Công nghệ sử dụng

* Python
* Socket Programming
* Tkinter
* AES-GCM
* RSA
* SHA-256

---

## 📚 Học phần

**Nhập môn An toàn và Bảo mật Thông tin**
Năm học 2025 - 2026

---

⭐ Dự án được xây dựng nhằm mô phỏng quy trình lưu trữ video đám mây an toàn với các cơ chế bảo mật cơ bản và nâng cao.
