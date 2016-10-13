
/**
 * ----------------------------------------------------------------------------
 * This is a MFRC522 library example; see https://github.com/miguelbalboa/rfid
 */

#include <SPI.h>
#include <MFRC522.h>
#include <Button.h>

#define RST_PIN         9           // Configurable, see typical pin layout above
#define SS_PIN          10          // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

MFRC522::MIFARE_Key key;

Button sair = Button(2,PULLUP);
Button avancar = Button(4,PULLUP);
Button retornar = Button(7,PULLUP);


void setup() {
    Serial.begin(9600); // Initialize serial communications with the PC
    while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
    SPI.begin();        // Init SPI bus
    mfrc522.PCD_Init(); // Init MFRC522 card
}

void loop() {
     if (sair.isPressed())
        Serial.println("botao_sair");
  
     if (avancar.isPressed())
        Serial.println("botao_avancar");
  
     if (retornar.isPressed()) {
        Serial.println("botao_retornar");
     }
    // Look for new cards
    if ( ! mfrc522.PICC_IsNewCardPresent())
        return;

    // Select one of the cards
    if ( ! mfrc522.PICC_ReadCardSerial())
        return;

    Serial.print(F("Card UID:"));
    dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
    Serial.println();
    
    // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD
    mfrc522.PCD_StopCrypto1();
    
}

void dump_byte_array(byte *buffer, byte bufferSize) {
    for (byte i = 0; i < bufferSize; i++) {
        Serial.print(buffer[i] < 0x10 ? " 0" : " ");
        Serial.print(buffer[i], HEX);
    }
}
