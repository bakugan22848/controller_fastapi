#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Update.h>

// --- ДИНАМІЧНЕ ПІДКЛЮЧЕННЯ БІБЛІОТЕК ДЛЯ ТРИГЕРІВ ---
{% for t in triggers %}
  {% if t.type == 'DHT11' or t.type == 'DHT22' %}
#include "DHT.h"
  {% endif %}
{% endfor %}

// --- ІНІЦІАЛІЗАЦІЯ ТРИГЕРІВ ---
{% for t in triggers %}
  {% if t.type == 'DHT11' %}
DHT dht_{{ t.pin }}({{ t.pin }}, DHT11);
  {% elif t.type == 'DHT22' %}
DHT dht_{{ t.pin }}({{ t.pin }}, DHT22);
  {% endif %}
{% endfor %}

// --- КОНСТАНТИ ПРИСТРОЮ (Вшиваються сервером при збірці) ---
const char* device_id = "{{ device_id }}";
const String current_version = "{{ build_version }}";

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
  {% for t in triggers %}
    {% if t.type == 'DHT11' or t.type == 'DHT22' %}
  dht_{{ t.pin }}.begin();
    {% endif %}
  {% endfor %}

  // --- НАЛАШТУВАННЯ КОНТРОЛЕРІВ ---
  {% for c in controllers %}
  pinMode({{ c.pin }}, OUTPUT);
  digitalWrite({{ c.pin }}, LOW);
  {% endfor %}
}

void loop(){
  if (WiFi.status() == WL_CONNECTED) {

    // --- 1. ОПИТУВАННЯ ТРИГЕРІВ ---
    {% for t in triggers %}
      {% if t.type == 'Analog' %}
    int raw_{{ t.pin }} = analogRead({{ t.pin }});
    sendPutRequest((serverUrl + "trigger/" + "{{ t.id }}").c_str(), "{\"value\":" + String(raw_{{ t.pin }}) + "}");
    delay(200);
      {% elif t.type == 'DHT11' %}
    float hum_{{ t.pin }} = dht_{{ t.pin }}.readHumidity();
    if (!isnan(hum_{{ t.pin }})) {
        sendPutRequest((serverUrl + "trigger/" + "{{ t.id }}").c_str(), "{\"value\":" + String(hum_{{ t.pin }}) + "}");
    }
    delay(200);
      {% endif %}
    {% endfor %}

    // --- 2. ОПИТУВАННЯ КОНТРОЛЕРІВ ---
    {% for c in controllers %}
    checkControllerState("{{ c.id }}", {{ c.pin }});
    delay(200);
    {% endfor %}
  }
  delay(5000);
}