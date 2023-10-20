int ledPin0 = 3; // change this to the pin the LED is wired to
int ledPin1 = 6;
int ledPin2 = 15;

void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin0, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  
  // turn on LED pins
  pinMode(LED_BUILTIN_TX,INPUT);
  pinMode(LED_BUILTIN_RX,INPUT);

  Serial.begin(9600);
  Serial.println("Initializing...");
  // digitalWrite(ledPin, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Enter data:");
  while (Serial.available() == 0) {}     //wait for data available
  String teststr = Serial.readString();  //read until timeout
  teststr.trim();                        // remove any \r \n whitespace at the end of the String
  
  // when it receives on, turn the pin on
  if (teststr == "on") {
    Serial.println("turning on");
    digitalWrite(ledPin0, HIGH);
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
  } 

  // when it receives off, turn the pin off
  if (teststr == "off") {
    Serial.println("Turning Off");
    digitalWrite(ledPin0, LOW);
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
  }

}
