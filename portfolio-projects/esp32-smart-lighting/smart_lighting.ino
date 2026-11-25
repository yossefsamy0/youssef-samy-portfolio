// ESP32 low-voltage smart lighting demo.
// Relay polarity varies by module: change RELAY_ACTIVE_LOW after checking its datasheet.
const int RELAY_PIN = 26;
const int BUTTON_PIN = 27;
const bool RELAY_ACTIVE_LOW = true;
const unsigned long DEBOUNCE_MS = 45;

bool lightOn = false;
bool lastReading = HIGH;
bool stableButtonState = HIGH;
unsigned long lastDebounceTime = 0;

void setLight(bool on) {
  lightOn = on;
  const int activeLevel = RELAY_ACTIVE_LOW ? LOW : HIGH;
  const int inactiveLevel = RELAY_ACTIVE_LOW ? HIGH : LOW;
  digitalWrite(RELAY_PIN, on ? activeLevel : inactiveLevel);
  Serial.println(on ? "Light: ON" : "Light: OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  setLight(false);
}

void loop() {
  const bool reading = digitalRead(BUTTON_PIN);

  if (reading != lastReading) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_MS) {
    if (reading != stableButtonState) {
      stableButtonState = reading;
      if (stableButtonState == LOW) {
        setLight(!lightOn);
      }
    }
  }

  lastReading = reading;
}
