#include <SPI.h>
#include <Ethernet.h>

// 出力ピン
const int RED_LED   = 7;
const int MOTOR     = 6;
const int GREEN_LED = 5;

// Ethernet設定
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// Flaskサーバー
IPAddress server(192, 168, 10, 100);
const int port = 5000;

EthernetClient client;

unsigned long lastConnectionTime = 0;
const unsigned long postingInterval = 3000;

// 関数宣言
void checkControl();
void setMode(const String &mode);
String getControlValue(const String &response);

void setup() {
  Serial.begin(9600);

  pinMode(RED_LED, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  // 初期状態は停止
  setMode("none");

  Serial.println("Connecting to network...");

  if (Ethernet.begin(mac) == 0) {
    Serial.println("DHCP configuration failed");

    while (true) {
      // DHCP失敗時は停止
      setMode("none");
    }
  }

  delay(1000);

  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  // 3秒ごとにサーバーへ問い合わせる
  if (millis() - lastConnectionTime >= postingInterval) {
    checkControl();
    lastConnectionTime = millis();
  }
}

void checkControl() {
  client.stop();

  Serial.println();
  Serial.println(">>> Fetching control status... <<<");

  if (!client.connect(server, port)) {
    Serial.println("Connection failed");
    setMode("none");
    return;
  }

  // HTTPリクエスト送信
  client.println("GET /api-control HTTP/1.1");
  client.print("Host: ");
  client.println(server);
  client.println("Connection: close");
  client.println();

  String response = "";
  unsigned long startTime = millis();

  // サーバーからのレスポンスをすべて読み込む
  while (client.connected() || client.available()) {
    while (client.available()) {
      char c = client.read();
      response += c;
      startTime = millis();
    }

    // 5秒間データが来なければタイムアウト
    if (millis() - startTime > 5000) {
      Serial.println("Response timeout");
      client.stop();
      setMode("none");
      return;
    }
  }

  client.stop();

  Serial.println("Server response:");
  Serial.println(response);

  // JSONからcontの値を取得
  String mode = getControlValue(response);

  Serial.print("Received mode: ");
  Serial.println(mode);

  setMode(mode);
}

// JSON内の "cont" の値を取得する
String getControlValue(const String &response) {
  int keyPosition = response.indexOf("\"cont\"");

  if (keyPosition == -1) {
    Serial.println("cont field was not found");
    return "none";
  }

  // "cont"の後にあるコロンを探す
  int colonPosition = response.indexOf(':', keyPosition);

  if (colonPosition == -1) {
    Serial.println("Invalid JSON: colon was not found");
    return "none";
  }

  // 値の開始を示すダブルクォートを探す
  int valueStart = response.indexOf('"', colonPosition);

  if (valueStart == -1) {
    Serial.println("Invalid JSON: value start was not found");
    return "none";
  }

  // 値の終了を示すダブルクォートを探す
  int valueEnd = response.indexOf('"', valueStart + 1);

  if (valueEnd == -1) {
    Serial.println("Invalid JSON: value end was not found");
    return "none";
  }

  String value = response.substring(valueStart + 1, valueEnd);
  value.trim();

  return value;
}

// モードに応じてLEDとモーターを制御する
void setMode(const String &mode) {
  if (mode == "heat") {
    Serial.println("Mode: HEAT");

    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(MOTOR, HIGH);

  } else if (mode == "cool") {
    Serial.println("Mode: COOL");

    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(MOTOR, HIGH);

  } else {
    // none、不明な値、通信失敗時
    Serial.println("Mode: NONE");

    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(MOTOR, LOW);
  }
}