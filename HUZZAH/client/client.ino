/*
Client Code for Huzzah Breakout Board.

The Huzzah scans and stores information about the networks around it. It'll then send 
a 34 byte array to the server. This array includes the IP address and the top 3 
routers' BSSIDs and their corresponding RSSIs. The array will be in the below form:

[  4 bytes  |  6 bytes  |  4 bytes  |  6 bytes  |  4 bytes  |  6 bytes  |  4 bytes  ]
[  IP addr  |  BSSID 0  |  RSSI 0   |  BSSID 1  |  RSSI 1   |  BSSID 2  |  RSSI 2   ]

Author: Christine Hwang
Project: On-Campus Lost & Found
Date: May 18, 2016
References: Tom Igoe and Jaymes Dec's ScanNetworks Example, Arduino Wi-Fi Library
 */

#include <SPI.h>
#include <ESP8266WiFi.h>

// Global Variables
String ssid;
uint8_t encryptionType;
int32_t RSSI;
uint8_t* bssid;
uint8_t topBSSID[3][6];
int32_t topRSSI[3];
byte clientArray[34];
int bssidFlag = 0;
int32_t channel;
bool isHidden;
IPAddress ip;

// Main Network Name and Password
const char* ssidMain = "RedRover";
const char* password = "";

// Server hostname and Port
const char* host = "google.com";//"10.148.1.96";
WiFiClient client;
const int httpPort = 80;//10002;

/*
 * Setup the LED, connect to Wi-Fi, and get the IP address
 */
void setup() {

  //Setup LED for troubleshooting battery life
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

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssidMain);

  // Change this line depending if there is a password or not
  WiFi.begin(ssidMain);//,password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");

  // Use WiFiClient class to create TCP connections
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  // Get the Address and store it in MS4B of clientArray
  Serial.println("IP address: ");
  ip = WiFi.localIP();
  Serial.println(ip);
  clientArray[0] = ip[0];
  clientArray[1] = ip[1];
  clientArray[2] = ip[2];
  clientArray[3] = ip[3];
  
  // Print WiFi MAC address:
  printMacAddress();
}

/*
 * Scan networks and send the clientArray every 30 seconds
 */
void loop() {
  // Blink LED for troubleshooting battery life
  digitalWrite(0, HIGH);
  delay(15000);
  digitalWrite(0, LOW);
  
  // scan for existing networks:
  Serial.println("Scanning available networks...");
  listNetworks();
  delay(15000);
}

/*
 * Prints MacAddress of Huzzah
 */
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

/*
 * Prints out a list of networks and their corresponding information
 */
void listNetworks() {  
  // scan for nearby networks:
  Serial.println("** Scan Networks **");
  int numSsid = WiFi.scanNetworks();
  
  if (numSsid == -1) {
    Serial.println("Couldn't get a wifi connection");
    while (true);
  }

  // Make temporary arrays and variables
  int32_t arrayRSSI[numSsid];
  uint8_t* arrayBSSID[numSsid];
  int i,j;                        // Used for sorting
  int32_t tmpRSSI;
  uint8_t* tmpBSSID;

  // print the list of networks seen:
  Serial.print("number of available networks:");
  Serial.println(numSsid);

  // print the network number and name for each network found:
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet);
    Serial.print(") ");
    WiFi.getNetworkInfo(thisNet, ssid, encryptionType, RSSI, bssid, channel, isHidden);
    arrayRSSI[thisNet] = RSSI;
    arrayBSSID[thisNet] = bssid;
    Serial.println(String("SSID : ") + ssid);
    printBSSID(99, bssid);
    Serial.println(String("RSSI : ") + RSSI);
  }

  // Sort the Array for the top 3 routers' BSSID using insertion sort
  // Do this one time only
  if (!bssidFlag){
    for (i = 1; i < numSsid; i++){
      j = i;
      while (j > 0 && arrayRSSI[j-1] < arrayRSSI[j]){
        tmpRSSI = arrayRSSI[j-1];
        tmpBSSID = arrayBSSID[j-1];
        arrayRSSI[j-1] = arrayRSSI[j];
        arrayBSSID[j-1] = arrayBSSID[j];
        arrayRSSI[j] = tmpRSSI;
        arrayBSSID[j] = tmpBSSID;
        j = j-1;       
      }
    }

    memcpy(topBSSID[0], arrayBSSID[0], 6);
    memcpy(topBSSID[1], arrayBSSID[1], 6);
    memcpy(topBSSID[2], arrayBSSID[2], 6);
    
    bssidFlag += 1;
  }

  // Find the top 3 BSSIDs' corresponding RSSI
  for (i = 0; i < numSsid; i++){
    if (memcmp(arrayBSSID[i], topBSSID[0], 6) == 0){
      topRSSI[0] = arrayRSSI[i];
    }
    else if (memcmp(arrayBSSID[i], topBSSID[1], 6) == 0){
      topRSSI[1] = arrayRSSI[i];      
    }
    else if (memcmp(arrayBSSID[i], topBSSID[2], 6) == 0) {
      topRSSI[2] = arrayRSSI[i];
    }
  }
  
//  Serial.println("RSSI Array:");
//  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
//    Serial.print(thisNet + String("->"));
//    Serial.println(arrayRSSI[thisNet]);
//  }


  // Make the client array
  updateClientArray();
  
  // Print for debugging purposes
  printClientArray();
  
  // Send the client array byte by byte
//  for(i = 0; i < 34; i++){
//    j = client.print(clientArray[i]);
//    Serial.println(String("Sending ") + j);
//  } 
}

/*
 * Prints the BSSID onto the Serial Monitor;
 * Used for debugging purposes
 */
void printBSSID(int i, uint8_t* bssid){
    Serial.print("BSSID");
    Serial.print(i,DEC);
    Serial.print(": ");
    Serial.print(bssid[0],HEX);
    Serial.print(":");
    Serial.print(bssid[1],HEX);
    Serial.print(":");
    Serial.print(bssid[2],HEX);
    Serial.print(":");
    Serial.print(bssid[3],HEX);
    Serial.print(":");
    Serial.print(bssid[4],HEX);
    Serial.print(":"); 
    Serial.print(bssid[5],HEX);
    Serial.println(" "); 
}

/*
 * Prints the Client Array;
 * Used for debugging purposes
 */
void printClientArray(){
  int32_t tmpRSSI;
  
  // Print IP First
  Serial.print("Stored IP: ");
  Serial.print(clientArray[0]);
  Serial.print(".");
  Serial.print(clientArray[1]);
  Serial.print(".");
  Serial.print(clientArray[2]);
  Serial.print(".");
  Serial.print(clientArray[3]);
  Serial.println(" ");

  // Print BSSID 0
  Serial.print("Stored ");
  printBSSID(0, clientArray+4);

  // Print BSSID 0 RSSI
  Serial.print("Stored RSSI0: ");
  tmpRSSI = (clientArray[10] << 24) | (clientArray[11] << 16) | (clientArray[12] << 8) | clientArray[13];
  Serial.print(tmpRSSI);
  Serial.println(" ");

  // Print BSSID 1
  Serial.print("Stored ");
  printBSSID(1, clientArray+14);

  // Print BSSID 1 RSSI
  Serial.print("Stored RSSI1: ");
  tmpRSSI = (clientArray[20] << 24) | (clientArray[21] << 16) | (clientArray[22] << 8) | clientArray[23];
  Serial.print(tmpRSSI);
  Serial.println(" ");

  // Print BSSID 2
  Serial.print("Stored ");
  printBSSID(2, clientArray+24);

  // Print BSSID 2 RSSI
  Serial.print("Stored RSSI2: ");
  tmpRSSI = (clientArray[30] << 24) | (clientArray[31] << 16) | (clientArray[32] << 8) | clientArray[33];
  Serial.print(tmpRSSI);
  Serial.println(" ");
}

/*
 * Updates the Client Array with the BSSIDs and their RSSIs
 */
void updateClientArray(){
  // Update BSSID 0
  memcpy(clientArray+4, topBSSID[0], 6);

  // Update BSSID 0's RSSI
  clientArray[10] = (topRSSI[0] >> 24) & 0xFF;
  clientArray[11] = (topRSSI[0] >> 16) & 0xFF;
  clientArray[12] = (topRSSI[0] >> 8) & 0xFF;
  clientArray[13] = topRSSI[0] & 0xFF;

  // Update BSSID 1
  memcpy(clientArray+14, topBSSID[1], 6);

  // Update BSSID 1's RSSI
  clientArray[20] = (topRSSI[1] >> 24) & 0xFF;
  clientArray[21] = (topRSSI[1] >> 16) & 0xFF;
  clientArray[22] = (topRSSI[1] >> 8) & 0xFF;
  clientArray[23] = topRSSI[1] & 0xFF;

  // Update BSSID 2
  memcpy(clientArray+24, topBSSID[2], 6);

  // Update BSSID 2's RSSI
  clientArray[30] = (topRSSI[2] >> 24) & 0xFF;
  clientArray[31] = (topRSSI[2] >> 16) & 0xFF;
  clientArray[32] = (topRSSI[2] >> 8) & 0xFF;
  clientArray[33] = topRSSI[2] & 0xFF; 
}

