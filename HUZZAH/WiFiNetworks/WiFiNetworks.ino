
/*
 This example  prints the Wifi shield's MAC address, and
 scans for available Wifi networks using the Wifi shield.
 Every ten seconds, it scans again. It doesn't actually
 connect to any network, so no encryption scheme is specified.

 Circuit:
 * WiFi shield attached

 created 13 July 2010
 by dlf (Metodo2 srl)
 modified 21 Junn 2012
 by Tom Igoe and Jaymes Dec
 */


#include <SPI.h>
#include <ESP8266WiFi.h>

String ssid;
uint8_t encryptionType;
int32_t RSSI;
uint8_t* bssid;
int32_t channel;
bool isHidden;

void setup() {

  //Setup Light for Troubleshooting Battery Life
  pinMode(0, OUTPUT);
  
  //Initialize serial and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }


  // Print WiFi MAC address:
  printMacAddress();
}

void loop() {
  // Blink light for troubleshooting
  digitalWrite(0, HIGH);
  delay(10000);
  digitalWrite(0, LOW);
  
  // scan for existing networks:
  Serial.println("Scanning available networks...");
  listNetworks();
  delay(10000);
}

void printMacAddress() {
  // the MAC address of your Wifi shield
  byte mac[6];

  // print your MAC address:
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5], HEX);
  Serial.print(":");
  Serial.print(mac[4], HEX);
  Serial.print(":");
  Serial.print(mac[3], HEX);
  Serial.print(":");
  Serial.print(mac[2], HEX);
  Serial.print(":");
  Serial.print(mac[1], HEX);
  Serial.print(":");
  Serial.println(mac[0], HEX);
}

void listNetworks() {
  // scan for nearby networks:
  Serial.println("** Scan Networks **");
  int numSsid = WiFi.scanNetworks();
  
  if (numSsid == -1) {
    Serial.println("Couldn't get a wifi connection");
    while (true);
  }
  
  int arrayRSSI[numSsid];
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    arrayRSSI[thisNet] = 0;
  }


  // print the list of networks seen:
  Serial.print("number of available networks:");
  Serial.println(numSsid);

  // print the network number and name for each network found:
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet);
    Serial.print(") ");
//    Serial.print(WiFi.SSID(thisNet));
//    Serial.print("\tSignal: ");
//    Serial.print(WiFi.RSSI(thisNet));
//    Serial.print(" dBm");
//    Serial.print("\tEncryption: ");
//    printEncryptionType(WiFi.encryptionType(thisNet));
    WiFi.getNetworkInfo(thisNet, ssid, encryptionType, RSSI, bssid, channel, isHidden);
    arrayRSSI[thisNet] = RSSI;
    Serial.println(String("RSSI in ARRAY: ") + arrayRSSI[thisNet]);
    Serial.println(String("SSID : ") + ssid);
    Serial.println(String("encryptionType : ") + encryptionType);
    Serial.print("BSSID: ");
    Serial.print(bssid[5],HEX);
    Serial.print(":");
    Serial.print(bssid[4],HEX);
    Serial.print(":");
    Serial.print(bssid[3],HEX);
    Serial.print(":");
    Serial.print(bssid[2],HEX);
    Serial.print(":");
    Serial.print(bssid[1],HEX);
    Serial.print(":");
    Serial.println(bssid[0],HEX);
    Serial.println(String("RSSI : ") + RSSI);
    Serial.println(String("Channel : ") + channel);
    Serial.println(String("Hidden : ") + isHidden); 
  }

  Serial.println("RSSI Array:");
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet + String("->"));
    Serial.println(arrayRSSI[thisNet]);
  }

}

void printEncryptionType(int thisType) {
  // read the encryption type and print out the name:
  switch (thisType) {
    case ENC_TYPE_WEP:
      Serial.println("WEP");
      break;
    case ENC_TYPE_TKIP:
      Serial.println("WPA");
      break;
    case ENC_TYPE_CCMP:
      Serial.println("WPA2");
      break;
    case ENC_TYPE_NONE:
      Serial.println("None");
      break;
    case ENC_TYPE_AUTO:
      Serial.println("Auto");
      break;
  }
}
