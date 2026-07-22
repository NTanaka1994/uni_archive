#include <SPI.h>
#include <Ethernet.h>
#include <DHT.h>

// DHT11の設定
#define DHTPIN 2        // DHT11のDATAピンをデジタル2番ピンに接続
#define DHTTYPE DHT11   // センサーの種類をDHT11に指定
DHT dht(DHTPIN, DHTTYPE);

// MACアドレスの設定（環境に合わせて変更してください）
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// FlaskサーバーのIPアドレスとポートを設定
IPAddress server(192, 168, 10, 101); 
int port = 5000; 

EthernetClient client;
unsigned long lastConnectionTime = 0;           // 最後に通信した時間
const unsigned long postingInterval = 10000;    // 送信間隔（10秒）

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }

  // DHTセンサーの初期化
  dht.begin();

  // DHCPでIPアドレスを取得
  if (Ethernet.begin(mac) == 0) {
    Serial.println("DHCP configuration failed");
    while (true);
  }
  delay(1000);
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  // サーバーからのレスポンスをシリアルに出力（デバッグ用）
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  // 指定した間隔（10秒）ごとにデータを送信
  if (millis() - lastConnectionTime > postingInterval) {
    
    // DHT11から温度を読み込み（摂氏）
    float currentTemp = dht.readTemperature();

    // 読み込みに失敗していないか確認
    if (isnan(currentTemp)) {
      Serial.println("Failed to read from DHT sensor!");
    } else {
      Serial.print("Current Temp: ");
      Serial.print(currentTemp);
      Serial.println(" C");
      
      // サーバーに温度をPOST送信
      sendTemperature(currentTemp);
    }
  }
}

// 温度データをPOST送信する関数
void sendTemperature(float temp) {
  client.stop(); // 既存の接続を確実に閉じる
  
  if (client.connect(server, port)) {
    Serial.println("\n--- Sending Temperature (POST) ---");
    
    // Flaskの request.form["temp"] が受け取れる形式（temp=xx.x）にする
    String postData = "temp=" + String(temp, 1); 

    client.println("POST /sense HTTP/1.1");
    client.print("Host: "); client.println(server);
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: "); client.println(postData.length());
    client.println("Connection: close");
    client.println(); // ヘッダーの終わりの空行
    client.print(postData); // データ本体

    lastConnectionTime = millis();
  } else {
    Serial.println("POST connection failed");
  }
}
