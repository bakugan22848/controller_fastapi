#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Update.h>

// --- ДИНАМІЧНЕ ПІДКЛЮЧЕННЯ БІБЛІОТЕК ДЛЯ ТРИГЕРІВ ---

  
#include "DHT.h"
  

  


// --- ІНІЦІАЛІЗАЦІЯ ТРИГЕРІВ ---

  
DHT dht_4(4, DHT11);
  

  


// --- КОНСТАНТИ ПРИСТРОЮ (Вшиваються сервером при збірці) ---
const char* device_id = "70f75a0b-c593-4b93-863b-2f6fe5ae6b7c";
const String current_version = "1780001472";

const char* ssid = "MikroTik-A478C0";
const char* password = "0506902609";
const String serverUrl = "http://192.168.88.241:8000/esp/";

void checkAndPerformOTA() {
  HTTPClient http;
  String checkVersionUrl = serverUrl + "firmware/" + String(device_id) + "/version";

  http.begin(checkVersionUrl.c_str());
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    String response = http.getString();
    StaticJsonDocument<256> doc;
    deserializeJson(doc, response);

    String server_version = doc["version"].as<String>();

    Serial.println("Поточна версія плати: " + current_version);
    Serial.println("Доступна версія на сервері: " + server_version);

    // Захист від нескінченної прошивки
    if (server_version == current_version || server_version == "v0" || server_version == "") {
      Serial.println("Оновлення не потрібне або прошивка актуальна.");
      http.end();
      return;
    }

    http.end();

    // Якщо версії не збігаються — качаємо новий бінарник
    String downloadUrl = serverUrl + "firmware/" + String(device_id);
    Serial.println("Завантажую нову конфігурацію з: " + downloadUrl);

    http.begin(downloadUrl.c_str());
    int downloadHttpCode = http.GET();

    if (downloadHttpCode == HTTP_CODE_OK) {
      int contentLength = http.getSize();
      if (Update.begin(contentLength)) {
        Serial.println("Знайдено нову конфігурацію! Оновлююсь... Не вимикайте живлення.");
        WiFiClient* client = http.getStreamPtr();
        if (Update.writeStream(*client) == contentLength && Update.end()) {
          if (Update.isFinished()) {
            Serial.println("Оновлено успішно! Рестарт системи...");
            delay(1000);
            ESP.restart();
          }
        }
      }
    }
  }
  http.end();
}

void sendPutRequest(const char* url, String jsonPayload) {
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.PUT(jsonPayload);
  http.end();
}

void checkControllerState(const char* controller_id, int pin) {
  HTTPClient http;
  String url = serverUrl + "controller/" + String(controller_id);
  http.begin(url.c_str());
  int httpResponseCode = http.GET();
  if (httpResponseCode == 200) {
    String response = http.getString();
    StaticJsonDocument<256> doc;
    if (!deserializeJson(doc, response) && doc.containsKey("last_state")) {
      bool last_state = doc["last_state"];
      digitalWrite(pin, last_state ? HIGH : LOW);
    }
  }
  http.end();
}

void setup(){
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n=========================================");
  Serial.println(" СИСТЕМА ЗАПУЩЕНА! Моя версія: " + current_version);
  Serial.println("=========================================");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWi-Fi Connected!");

  // Перевірка OTA при старті
  checkAndPerformOTA();

  // --- НАЛАШТУВАННЯ ТРИГЕРІВ ---
  
    
  dht_4.begin();
    
  
    
  

  // --- НАЛАШТУВАННЯ КОНТРОЛЕРІВ ---
  
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
  
}

void loop(){
  if (WiFi.status() == WL_CONNECTED) {

    // --- 1. ОПИТУВАННЯ ТРИГЕРІВ ---
    
      
    float hum_4 = dht_4.readHumidity();
    if (!isnan(hum_4)) {
        sendPutRequest((serverUrl + "trigger/" + "42a5d2e8-5fb4-46e3-be3f-aefbd6939391").c_str(), "{\"value\":" + String(hum_4) + "}");
    }
    delay(200);
      
    
      
    int raw_34 = analogRead(34);
    sendPutRequest((serverUrl + "trigger/" + "790efa4d-857a-4cf8-9289-e7836b59d693").c_str(), "{\"value\":" + String(raw_34) + "}");
    delay(200);
      
    

    // --- 2. ОПИТУВАННЯ КОНТРОЛЕРІВ ---
    
    checkControllerState("b4f2ca32-d430-42a7-bacc-35f633d85503", 2);
    delay(200);
    
  }
  delay(5000);
}