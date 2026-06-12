# 🔐 Secure Cloud Video Storage

## Bài tập lớn môn học "Nhập môn An toàn và Bảo mật Thông tin"

**Giảng viên hướng dẫn:** TS. Trần Quý Nam<br>
**Nhóm thực hiện:** Nhóm 7<br>
**Trường:** Đại học Đại Nam

---

## 📖 Giới thiệu

Hệ thống mô phỏng quá trình lưu trữ video đám mây an toàn, áp dụng các cơ chế bảo mật như mã hóa dữ liệu, trao đổi khóa, xác thực người gửi và kiểm tra tính toàn vẹn của dữ liệu.

---

## ✨ Chức năng chính

* 📤 Upload video an toàn
* 📥 Download video an toàn
* 🔒 Mã hóa video bằng AES-GCM
* 🔑 Trao đổi khóa bằng RSA
* ✍️ Xác thực bằng chữ ký số (Digital Signature)
* 🛡️ Kiểm tra tính toàn vẹn bằng SHA-256
* 🚫 Chống Replay Attack
* 📝 Ghi nhật ký bảo mật (Security Logging)
* 🔄 Tự động gửi lại khi mạng lỗi (Retry Mechanism)
* 🌐 Mô phỏng mất gói tin (Packet Loss)
* 🖥️ Giao diện Client và Server bằng Tkinter

---

## 🏗️ Mô hình hệ thống

```text
Client
   │
   │ RSA Public Key
   ▼
Tạo khóa phiên AES
   │
   │ Mã hóa video
   ▼
Video đã mã hóa
   │
   │ SHA-256 Hash
   │ Digital Signature
   ▼
Cloud Server
   │
   ├── Xác thực chữ ký số
   ├── Kiểm tra toàn vẹn dữ liệu
   ├── Giải mã video
   └── Lưu trữ video
```

---

## 🔐 Các cơ chế bảo mật được sử dụng

| Cơ chế            | Mục đích                 |
| ----------------- | ------------------------ |
| AES-GCM           | Mã hóa video             |
| RSA               | Trao đổi khóa phiên      |
| Digital Signature | Xác thực người gửi       |
| SHA-256           | Kiểm tra tính toàn vẹn   |
| Anti-Replay       | Chống gửi lại gói tin    |
| Security Logging  | Ghi nhận sự kiện bảo mật |

---

## 📂 Cấu trúc thư mục

```text
secure-cloud-video-storage/
│
├── client/
├── server/
├── crypto/
├── logs/
├── keys/
├── cloud_storage/
├── downloads/
├── test_files/
│
├── generate_keys.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Yêu cầu môi trường

* Python 3.10 trở lên
* Windows 10 hoặc Windows 11
* Kết nối localhost

Kiểm tra phiên bản Python:

```bash
python --version
```

---

## 🚀 Hướng dẫn cài đặt

### Bước 1: Clone dự án

```bash
git clone https://github.com/lsdai1411/secure-cloud-video-storage.git

cd secure-cloud-video-storage
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 3: Tạo khóa RSA

```bash
python generate_keys.py
```

Nếu thành công sẽ xuất hiện:

```text
KEYS CREATED
```

Thư mục `keys/` sẽ được tạo tự động.

---

## ▶️ Hướng dẫn chạy chương trình

### Chạy Server

Mở Terminal:

```bash
python server/server_gui.py
```

Sau đó bấm:

```text
Start Server
```

Trạng thái:

```text
Server Running
```

### Chạy Client

Mở Terminal khác:

```bash
python client/client_gui.py
```

---

## 📤 Upload video

1. Bấm **Browse**
2. Chọn video
3. Bấm **Upload**

Nếu thành công:

```text
UPLOAD SUCCESS
SERVER: ACK
```

---

## 📥 Download video

Bấm:

```text
Download
```

Video tải về sẽ được lưu tại:

```text
downloads/video.mp4
```

Nếu thành công:

```text
DOWNLOAD SUCCESS
ACK
```

---

## 🌐 Chế độ mạng

### NORMAL

Hoạt động bình thường.

Server phản hồi:

```text
ACK
```

### PACKET LOSS

Mô phỏng mất gói tin.

Server phản hồi:

```text
NACK
```

Client sẽ tự động gửi lại tối đa 3 lần.

---

## 📝 Nhật ký bảo mật

Các sự kiện bảo mật sẽ được ghi lại trên Server.

Ví dụ:

```text
UPLOAD SUCCESS - video.mp4
ACK

DOWNLOAD SUCCESS - video.mp4
ACK

INTEGRITY ERROR
NACK
```

---

## 🧪 Chức năng đã kiểm thử

* ✅ Upload video
* ✅ Download video
* ✅ Mã hóa AES-GCM
* ✅ Trao đổi khóa RSA
* ✅ Kiểm tra SHA-256
* ✅ Xác thực chữ ký số
* ✅ Chống Replay Attack
* ✅ Retry Mechanism
* ✅ Packet Loss Simulation
* ✅ Clone mới và chạy thành công

---

## 📸 Hình ảnh minh họa

### Giao diện Server

*(Thêm ảnh tại đây)*

### Giao diện Client

*(Thêm ảnh tại đây)*

---

## 👨‍💻 Công nghệ sử dụng

* Python
* Socket Programming
* Tkinter
* AES-GCM
* RSA-2048
* SHA-256
* Cryptography

---

## 🎯 Mục tiêu dự án

Dự án được xây dựng nhằm nghiên cứu, mô phỏng và triển khai các cơ chế bảo mật thông tin trong quá trình truyền tải và lưu trữ dữ liệu trên môi trường đám mây.

Thông qua dự án, nhóm hướng đến việc:

* Tìm hiểu nguyên lý hoạt động của các thuật toán mật mã hiện đại.
* Áp dụng RSA trong trao đổi khóa an toàn.
* Áp dụng AES-GCM trong mã hóa dữ liệu video.
* Sử dụng chữ ký số để xác thực nguồn gốc dữ liệu.
* Kiểm tra tính toàn vẹn dữ liệu bằng SHA-256.
* Mô phỏng các tình huống mất gói tin và lỗi mạng trong thực tế.
* Xây dựng hệ thống Client – Server có khả năng upload và download dữ liệu an toàn.

Dự án đồng thời giúp sinh viên củng cố kiến thức về lập trình mạng, mật mã học ứng dụng và các nguyên tắc cơ bản trong lĩnh vực An toàn và Bảo mật Thông tin.

---

⭐ Dự án được thực hiện bởi **Nhóm 7 – Trường Đại học Đại Nam** dưới sự hướng dẫn của **TS. Trần Quý Nam**, phục vụ mục đích học tập, nghiên cứu và thực hành các kỹ thuật bảo mật thông tin trong môi trường lưu trữ đám mây.
