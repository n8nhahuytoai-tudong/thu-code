# Hướng Dẫn Tải File Về VPS

## Thông tin kết nối SSH Proxy
```bash
ssh -p 30195 root@ssh6.vast.ai -L 8080:localhost:8080
```

## 1. Tải file TỪ máy local LÊN VPS

### Cách 1: Sử dụng SCP (Secure Copy)

#### Tải 1 file:
```bash
scp -P 30195 /path/to/local/file.txt root@ssh6.vast.ai:/path/to/remote/directory/
```

#### Tải cả thư mục:
```bash
scp -P 30195 -r /path/to/local/folder root@ssh6.vast.ai:/path/to/remote/directory/
```

### Cách 2: Sử dụng rsync (khuyến nghị cho file lớn)
```bash
rsync -avz -e "ssh -p 30195" /path/to/local/file root@ssh6.vast.ai:/path/to/remote/directory/
```

### Cách 3: Sử dụng SFTP
```bash
sftp -P 30195 root@ssh6.vast.ai
# Sau đó trong SFTP prompt:
put /path/to/local/file.txt /path/to/remote/directory/
# hoặc upload cả thư mục:
put -r /path/to/local/folder /path/to/remote/directory/
```

---

## 2. Tải file TỪ VPS VỀ máy local

### Cách 1: Sử dụng SCP

#### Tải 1 file:
```bash
scp -P 30195 root@ssh6.vast.ai:/path/to/remote/file.txt /path/to/local/directory/
```

#### Tải cả thư mục:
```bash
scp -P 30195 -r root@ssh6.vast.ai:/path/to/remote/folder /path/to/local/directory/
```

### Cách 2: Sử dụng rsync
```bash
rsync -avz -e "ssh -p 30195" root@ssh6.vast.ai:/path/to/remote/file /path/to/local/directory/
```

### Cách 3: Sử dụng SFTP
```bash
sftp -P 30195 root@ssh6.vast.ai
# Trong SFTP prompt:
get /path/to/remote/file.txt /path/to/local/directory/
# hoặc download cả thư mục:
get -r /path/to/remote/folder /path/to/local/directory/
```

---

## 3. Tải file qua HTTP (sử dụng port forwarding 8080)

Nếu bạn đã setup web server trên VPS (ví dụ: Python HTTP server):

### Trên VPS (sau khi SSH vào):
```bash
# Chuyển đến thư mục chứa file cần tải
cd /path/to/files

# Khởi động HTTP server đơn giản
python3 -m http.server 8080
```

### Trên máy local:
```bash
# Kết nối SSH với port forwarding
ssh -p 30195 root@ssh6.vast.ai -L 8080:localhost:8080

# Sau đó mở browser hoặc dùng wget/curl:
wget http://localhost:8080/filename.txt
# hoặc
curl -O http://localhost:8080/filename.txt
```

---

## 4. Ví dụ cụ thể

### Upload file model lên VPS:
```bash
scp -P 30195 ./model.pth root@ssh6.vast.ai:/workspace/models/
```

### Download kết quả từ VPS về:
```bash
scp -P 30195 root@ssh6.vast.ai:/workspace/output/result.mp4 ./downloads/
```

### Upload cả thư mục dataset:
```bash
rsync -avz --progress -e "ssh -p 30195" ./dataset/ root@ssh6.vast.ai:/workspace/data/
```

---

## Lưu ý quan trọng:

1. **Port SSH**: Luôn sử dụng `-P 30195` (chữ P hoa) cho SCP/SFTP, hoặc `-p 30195` (chữ p thường) cho SSH
2. **Progress bar**: Thêm `--progress` hoặc `-v` để xem tiến trình tải
3. **Resume download**: Sử dụng `rsync` với option `--partial` để tiếp tục tải file bị gián đoạn
4. **Nén file**: Với rsync, option `-z` sẽ nén file khi truyền để tăng tốc độ

## Script tự động

### Script upload file (upload.sh):
```bash
#!/bin/bash
SCP_PORT=30195
SCP_HOST="root@ssh6.vast.ai"
LOCAL_PATH="$1"
REMOTE_PATH="$2"

scp -P $SCP_PORT -r "$LOCAL_PATH" "$SCP_HOST:$REMOTE_PATH"
```

Sử dụng:
```bash
chmod +x upload.sh
./upload.sh /local/file.txt /remote/path/
```

### Script download file (download.sh):
```bash
#!/bin/bash
SCP_PORT=30195
SCP_HOST="root@ssh6.vast.ai"
REMOTE_PATH="$1"
LOCAL_PATH="$2"

scp -P $SCP_PORT -r "$SCP_HOST:$REMOTE_PATH" "$LOCAL_PATH"
```

Sử dụng:
```bash
chmod +x download.sh
./download.sh /remote/file.txt /local/path/
```
