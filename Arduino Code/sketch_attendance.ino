#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 rfid(SS_PIN, RST_PIN); // Create instance of MFRC522

void setup() {
    Serial.begin(9600);   // Initialize serial communication
    SPI.begin();          // Init SPI bus
    rfid.PCD_Init();      // Init MFRC522
    Serial.println("Place your RFID card/tag near the reader...");
}

void loop() {
    // Look for new RFID cards
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
        String uid = "";
        for (byte i = 0; i < rfid.uid.size; i++) {
            uid += String(rfid.uid.uidByte[i], HEX);
        }
        uid.toUpperCase();
        Serial.println(uid); // Send the UID over serial to the PC

        delay(1000); // Avoid multiple readings
    }
}
