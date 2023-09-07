//https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=mathesis_time&logNo=221283782219
#include <Keypad.h>

const byte ROWS = 4; 
const byte COLS = 4;

// 필름 키패드
// char keys[ROWS][COLS] = {
//   {'1','2','3', 'A'},
//   {'4','5','6', 'B'},
//   {'7','8','9', 'C'},
//   {'*','0','#', 'D'}
// };

// PCB 키패드
char keys[ROWS][COLS] = {
  {'*', '7', '4', '1'},
  {'0', '8', '5', '2'},
  {'#', '9', '6', '3'},
  {'D', 'C', 'B', 'A'}
};

byte rowPins[ROWS] = { 12, 11, 10, 9 };
byte colPins[COLS] = { 8, 7, 6, 5 };
Keypad kpd = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

char cmd;
int buzzer = 3;
unsigned long timer = millis();

void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  Serial.println("Sound output control device connected");
}

void loop() {
  cmd = kpd.getKey();
  if(cmd && (millis() - timer > 100)){
    Serial.println(cmd);
    tone(buzzer,16, 50);
    timer = millis();
    }
}
