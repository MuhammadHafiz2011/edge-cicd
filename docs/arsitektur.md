# Dokumentasi Arsitektur Sistem IoT Edge dengan CI/CD

## 1. Gambaran Umum

Proyek ini mengimplementasikan sistem **IoT berbasis Edge Computing** yang terintegrasi dengan mekanisme **CI/CD otomatis** menggunakan GitHub Actions. Sistem dirancang untuk mensimulasikan alur data IoT dari sensor hingga aplikasi backend, serta mendukung pembaruan aplikasi edge secara otomatis tanpa intervensi manual ke server.

Tujuan utama dari sistem ini adalah:

* Mensimulasikan pengiriman data sensor IoT
* Memproses data sedekat mungkin dengan sumber (edge device)
* Menyediakan antarmuka backend melalui Web API
* Mengimplementasikan CI/CD untuk service edge tanpa mengganggu control plane

---

## 2. Arsitektur Tingkat Tinggi

Alur data pada sistem dapat digambarkan sebagai berikut:

```
Sensor (Simulator)
        |
        | MQTT (sensor/temperature)
        v
MQTT Broker (Mosquitto)
        |
        v
Receiver Service (MQTT Subscriber)
        |
        | HTTP POST
        v
Gateway Service (Edge Processing)
        |
        v
Web Server (API / Interface)
```

Seluruh komponen dijalankan dalam container Docker dan dideploy pada sebuah **edge device** berupa instance AWS EC2.

---

## 3. Komponen Sistem

### 3.1 Sensor (Simulator)

**Lokasi:** `sensor/sensor.py`

Sensor pada sistem ini merupakan simulasi menggunakan Python yang bertugas untuk:

* Menghasilkan data suhu secara periodik
* Mengirimkan data ke MQTT broker

**Topik MQTT:** `sensor/temperature`

**Contoh payload:**

```json
{
  "temperature": 27.5
}
```

---

### 3.2 MQTT Broker

**Image:** `eclipse-mosquitto:2`

MQTT broker berfungsi sebagai message broker yang menjembatani komunikasi antara sensor dan receiver. Broker menggunakan protokol MQTT yang umum digunakan pada sistem IoT karena ringan dan mendukung komunikasi real-time.

---

### 3.3 Receiver Service

**Lokasi:** `receiver/receiver.py`

Receiver bertugas sebagai penghubung antara dunia IoT dan backend application. Fungsi utama receiver meliputi:

* Melakukan subscribe ke topik MQTT
* Menerima data dari sensor
* Meneruskan data ke Gateway menggunakan HTTP

Receiver berperan sebagai **bridge** antara protokol MQTT dan HTTP.

---

### 3.4 Gateway Service

**Lokasi:** `gateway/gateway.py`

Gateway merupakan lapisan pemrosesan di sisi edge. Fungsinya antara lain:

* Menerima data dari receiver melalui endpoint `/ingest`
* Melakukan logging dan preprocessing data
* Meneruskan data ke Web Server

Gateway berfungsi sebagai **edge processing layer** yang dapat dikembangkan untuk filtering, agregasi, atau validasi data.

---

### 3.5 Web Server

**Lokasi:** `web/web_server.py`

Web server menyediakan antarmuka backend untuk pengguna atau sistem lain. Fungsinya meliputi:

* Menyediakan Web API
* Menampilkan atau menyajikan data hasil pemrosesan

Endpoint yang tersedia antara lain:

* `/`
* (opsional) `/data/latest`, `/data/history`

Web server berperan sebagai **control plane interface**.

---

## 4. Container Orchestration

Sistem menggunakan Docker Compose untuk orkestrasi container dengan pemisahan tanggung jawab sebagai berikut:

### 4.1 Edge Data Plane

**File:** `docker-compose-edge.yml`

Service yang dijalankan:

* `mqtt-broker`
* `receiver`
* `gateway`

Service edge berada dalam satu Docker network bernama `edge-network` dan menjadi target utama CI/CD.

### 4.2 Control Plane

**File:** `docker-compose-control.yml`

Service yang dijalankan:

* `web-server`

Control plane dipisahkan untuk menjaga stabilitas layanan antarmuka dan tidak ikut ter-redeploy saat update edge service.

---

## 5. Arsitektur CI/CD

### 5.1 Alur CI/CD

```
Developer
   |
   | git push
   v
GitHub Repository
   |
   | GitHub Actions
   v
Build & Push Docker Image
   |
   v
Docker Hub
   |
   | SSH Deployment
   v
Edge Device (EC2)
```

---

### 5.2 GitHub Actions Workflow

**File:** `.github/workflows/deploy.yml`

Tahapan pipeline:

1. Checkout source code
2. Login ke Docker Hub
3. Build image `receiver` dan `gateway`
4. Push image ke Docker Hub
5. SSH ke EC2
6. Menjalankan `docker compose -f docker-compose-edge.yml pull`
7. Menjalankan `docker compose -f docker-compose-edge.yml up -d`

Pipeline hanya melakukan deployment pada **edge services**, tanpa memengaruhi web server.

---

## 6. Edge Device

**Platform:** AWS EC2

**Peran:**

* Menjalankan seluruh container edge dan control plane
* Bertindak sebagai node edge
* Memproses data dekat dengan sumber sensor

---

## 7. Keamanan

Sistem menerapkan beberapa praktik keamanan dasar:

* Autentikasi SSH berbasis key
* Penggunaan GitHub Secrets untuk credential sensitif

Secret yang digunakan:

* `EC2_HOST`
* `EC2_USER`
* `EC2_SSH_KEY`
* `DOCKERHUB_USERNAME`
* `DOCKERHUB_TOKEN`

Tidak terdapat credential yang di-hardcode di source code.

---

## 8. Karakteristik Sistem

| Aspek                    | Status     |
| ------------------------ | ---------- |
| Edge Computing           | ✓          |
| Containerization         | ✓ (Docker) |
| CI/CD Otomatis           | ✓          |
| Real-time Data           | ✓ (MQTT)   |
| Scalable                 | ✓          |
| Production-ready Pattern | ✓          |

---

## 9. Contoh Update melalui CI/CD

Perubahan berikut dapat dilakukan tanpa login manual ke server:

* Perubahan logika gateway
* Penambahan logging
* Bug fix pada receiver
* Perubahan API backend

Cukup dengan menjalankan:

```bash
git push
```

---

## 10. Kesimpulan

Sistem ini merepresentasikan implementasi arsitektur **IoT Edge modern** yang menggabungkan:

* Pemrosesan data di edge device
* Orkestrasi container yang terpisah antara data plane dan control plane
* CI/CD otomatis berbasis GitHub Actions

Pendekatan ini mencerminkan praktik DevOps yang relevan untuk sistem IoT skala kecil hingga menengah.

