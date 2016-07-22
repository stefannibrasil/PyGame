// run blink.py
// aqui ficará o código do PyGame recebendo dados do Arduino
// preciso pegar os dados do cartão e jogar no PyGame
const int ledPin = 13;
int red = 8;
int green = 7;

void setup()
{
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  Serial.println("Hello Stefanni");
  if (Serial.available())
  {
     flash(Serial.read() - '0');
  }
  delay(1000);
  changeLights(red, 3000);
  changeLights(green, 2001);
}

void changeLights(int color, int timer) {
    digitalWrite(color, HIGH);
    delay(timer);
    digitalWrite(color, LOW);
}

void flash(int n)
{
  for (int i = 0; i < n; i++)
  {
    digitalWrite(ledPin, HIGH);
    delay(100);
    digitalWrite(ledPin, LOW);
    delay(100);
  }
}
