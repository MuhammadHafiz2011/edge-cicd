# Dokumentasi Arsitektur Sistem IoT Edge dengan CI/CD

## 1. Tujuan dan Ruang Lingkup Sistem

Sistem ini merupakan prototipe jaringan Internet of Things (IoT) berbasis edge computing yang dirancang untuk mengimplementasikan dan menguji mekanisme Continuous Integration dan Continuous Deployment (CI/CD) pada layanan IoT berbasis container.

Fokus utama sistem ini bukan pada pengembangan aplikasi IoT secara kompleks, melainkan pada:
- Otomatisasi proses build dan deployment container
- Pemisahan control plane dan data plane
- Pembaruan layanan edge tanpa intervensi manual ke edge device

---

## 2. Arsitektur Sistem Secara Umum

Alur data IoT pada sistem ini adalah sebagai berikut:

Sensor (Simulator)
   |
   | MQTT
   v
MQTT Broker (Mosquitto)
   |
   v
Receiver (MQTT Subscriber)
   |
   | HTTP
   v
Gateway (Edge Processing)
   |
   v
Web Server (Backend API)


Seluruh komponen dijalankan dalam bentuk container Docker dan dideploy pada sebuah edge device berupa AWS EC2.

---

## 3. Struktur Project dan Fungsi Setiap Komponen

Bagian ini menjelaskan direktori dan file utama yang dibuat pada project beserta fungsinya.

---

### 3.1 Sensor (Simulator)

Direktori: `sensor/`  
File utama: `sensor.py`

Fungsi:
- Mensimulasikan perangkat sensor IoT
- Menghasilkan data suhu secara periodik
- Mengirim data ke MQTT broker menggunakan topik `sensor/temperature`

Sensor digunakan sebagai pengganti sensor fisik agar proses pengujian dan demo dapat dilakukan dengan mudah. Komponen ini tidak dikelola oleh CI/CD dan dijalankan secara manual.

---

### 3.2 MQTT Broker

Direktori: `mqtt-broker/`  
Image: `eclipse-mosquitto:2`  
File konfigurasi: `mosquitto.conf`

Fungsi:
- Menjadi message broker pada sistem IoT
- Menjembatani komunikasi antara sensor dan receiver
- Menyediakan mekanisme publish–subscribe menggunakan protokol MQTT

MQTT broker dikategorikan sebagai service infrastruktur yang relatif stabil dan jarang berubah, sehingga tidak menjadi target CI/CD.

---

### 3.3 Receiver Service (Layanan Dinamis)

Direktori: `receiver/`  
File utama:
- `receiver.py`
- `Dockerfile`

Fungsi:
- Melakukan subscribe ke topik MQTT
- Menerima data dari sensor
- Meneruskan data ke gateway menggunakan HTTP

Receiver bersifat dinamis karena logika aplikasinya sering mengalami perubahan, seperti perubahan topik MQTT, format payload, atau mekanisme parsing data. Oleh karena itu, receiver menjadi salah satu target utama CI/CD.

---

### 3.4 Gateway Service (Layanan Dinamis)

Direktori: `gateway/`  
File utama:
- `gateway.py`
- `Dockerfile`

Fungsi:
- Menerima data dari receiver melalui endpoint `/ingest`
- Melakukan logging dan preprocessing data
- Meneruskan data ke web server

Gateway merupakan lapisan edge processing yang sering mengalami perubahan logika, misalnya penambahan filtering, validasi, atau agregasi data. Gateway menjadi target utama CI/CD.

---

### 3.5 Web Server (Control Plane Interface)

Direktori: `web/`  
File utama:
- `web_server.py`
- `Dockerfile`

Fungsi:
- Menyediakan backend API
- Menampilkan data hasil pemrosesan edge
- Digunakan sebagai endpoint observasi saat demo

Web server dikategorikan sebagai control plane interface dan tidak termasuk target CI/CD agar stabilitas layanan tetap terjaga.

---

## 4. Orkestrasi Container

### 4.1 Edge Data Plane

File: `docker-compose-edge.yml`

File ini mengatur container:
- mqtt-broker
- receiver
- gateway

File `docker-compose-edge.yml` menjadi target utama CI/CD karena berisi layanan edge yang bersifat dinamis dan sering diperbarui.

---

### 4.2 Control Plane

File: `docker-compose-control.yml`

File ini mengatur container:
- web-server

File ini digunakan saat setup awal sistem dan tidak disentuh oleh pipeline CI/CD untuk menjaga kestabilan control plane.

---

## 5. Arsitektur CI/CD

### 5.1 Alur CI/CD

Alur CI/CD pada sistem ini adalah sebagai berikut:

Developer melakukan push ke repository GitHub  
→ GitHub Actions menjalankan pipeline CI/CD  
→ Image Docker receiver dan gateway dibuild  
→ Image dipush ke Docker Hub  
→ Edge device melakukan pull image terbaru  
→ Container edge di-restart secara otomatis

---

### 5.2 Workflow CI/CD

File workflow: `.github/workflows/deploy.yml`

Tahapan yang diotomatisasi:
1. Checkout source code
2. Login ke Docker Hub
3. Build image Docker untuk receiver dan gateway
4. Push image ke Docker Hub
5. SSH ke edge device
6. Menjalankan `docker compose -f docker-compose-edge.yml pull`
7. Menjalankan `docker compose -f docker-compose-edge.yml up -d`

Pipeline ini hanya memengaruhi layanan edge dan tidak memengaruhi web server.

---

### 5.3 Container Registry

Registry yang digunakan pada project ini adalah Docker Hub.

Docker Hub berfungsi sebagai:
- Penyimpanan image hasil build CI/CD
- Penghubung antara pipeline CI/CD dan edge device

Penggunaan Docker Hub bersifat fleksibel dan dapat digantikan dengan private registry pada implementasi nyata tanpa perubahan arsitektur CI/CD.

---

## 6. Edge Device

Platform: AWS EC2

Peran edge device:
- Menjalankan seluruh container edge dan control plane
- Menjadi target deployment otomatis
- Mewakili edge device fisik seperti Raspberry Pi

---

## 7. Keamanan dan Konfigurasi

Keamanan sistem diterapkan melalui:
- Autentikasi SSH berbasis key
- Penggunaan GitHub Secrets untuk credential sensitif

Secret yang digunakan antara lain:
- EC2_HOST
- EC2_USER
- EC2_SSH_KEY
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN

Tidak terdapat credential yang di-hardcode di source code.

---

## 8. Pembagian Control Plane dan Data Plane

Data Plane:
- Sensor
- MQTT Broker
- Receiver
- Gateway

Control Plane:
- GitHub Repository
- GitHub Actions (CI/CD)
- Docker Hub (Registry)
- Web Server

CI/CD beroperasi pada control plane tanpa mengganggu alur data IoT pada data plane.

---

## 9. Manfaat Implementasi CI/CD

Dengan arsitektur ini, sistem memperoleh beberapa manfaat utama:
- Pembaruan layanan edge menjadi otomatis
- Downtime dapat diminimalkan
- Risiko kesalahan manual berkurang
- Sistem mudah direplikasi dan dikembangkan

---

## 10. Kesimpulan

Dokumentasi ini menjelaskan arsitektur sistem IoT berbasis edge yang dirancang khusus untuk mengimplementasikan mekanisme CI/CD berbasis container. Sistem dibangun secara modular dengan pemisahan yang jelas antara data plane dan control plane, serta siap diadaptasi ke jaringan IoT nyata.

Catatan: Fokus utama penelitian ini adalah mekanisme CI/CD, bukan pengembangan aplikasi IoT.
