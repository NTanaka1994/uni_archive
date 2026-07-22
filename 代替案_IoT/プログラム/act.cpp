#include <SPI.h>
#include <Ethernet.h>

// ピン配置の設定（ラズパイのBOARDピン番号から、Arduinoのデジタルピンに割り当て）
const int RED_LED = 7;    // 赤色LED
const int MOTOR   = 6;    // モーター（ラズパイの11番の代わり。Arduinoの6番などへ）
const int GREEN_LED = 5;  // 緑色LED

// イーサネットの設定
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// IoTサーバーのIPアドレスとポートを設定してください
IPAddress server(192, 168, 1, 50); 
int port = 5000; 

EthernetClient client;
unsigned long lastConnectionTime = 0;
const unsigned long postingInterval = 3000; // ラズパイと同じ3秒間隔

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }

  // ピンを出力モードに設定し、初期状態をLOW（消灯/停止）にする
  pinMode(RED_LED, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);
  digitalWrite(MOTOR, LOW);
  digitalWrite(GREEN_LED, LOW);

  // DHCPでネットワークに接続
  Serial.println("Connecting to network...");
  if (Ethernet.begin(mac) == 0) {
    Serial.println("DHCP configuration failed");
    while (true);
  }
  delay(1000);
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  // 3秒ごとにサーバーへ制御状態を問い合わせる
  if (millis() - lastConnectionTime > postingInterval) {
    checkControl();
  }
}

void checkControl() {
  client.stop(); // 前回の接続をクリア
  
  if (client.connect(server, port)) {
    Serial.println("\n>>> Fetching control status... <<<");
    
    // FlaskサーバーのJSON配布APIへGETリクエスト
    client.println("GET /api-control HTTP/1.1");
    client.print("Host: "); client.println(server);
    client.println("Connection: close");
    client.println(); // ヘッダーの終了

    // サーバーからのレスポンスを解析
    // JSON内の '"cont":"' という文字列まで読み飛ばす
    if (client.find("\"cont\":\"")) {
      
      // その直後の文字列を判定
      if (client.find("heat")) {
        Serial.println("Mode: HEAT");
        digitalWrite(RED_LED, HIGH);
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(MOTOR, HIGH);
      } 
      else if (client.find("cool")) {
        Serial.println("Mode: COOL");
        digitalWrite(RED_LED, LOW);
        digitalWrite(GREEN_LED, HIGH);
        digitalWrite(MOTOR, HIGH);
      } 
      else if (client.find("none")) {
        Serial.println("Mode: NONE");
        digitalWrite(RED_LED, LOW);
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(MOTOR, LOW);
      }
    }
    
    lastConnectionTime = millis();
  } else {
    Serial.println("Connection failed. Turning off outputs for safety.");
    // 通信エラー時は安全のためすべて停止
    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(MOTOR, LOW);
    lastConnectionTime = millis();
  }
}
