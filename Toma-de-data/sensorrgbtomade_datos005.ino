#define PIN_OUT 3 // Número de pin al que se conecta la salida del pulso del TCS3200
#define PIN_OE  5 // Número de pin para activar el TCS3200 (se activa a nivel bajo) Para que siempre esté activo se puede conectar a GND
#define PIN_S0  2 // Número de pin de Arduino que conecta a S0 del TCS3200 (escala de frecuencia)
#define PIN_S1  4 // Número de pin de Arduino que conecta a S1 del TCS3200 (escala de frecuencia)
#define PIN_S2  7 // Número de pin de Arduino que conecta a S2 del TCS3200 (filtro de color)
#define PIN_S3  8 // Número de pin de Arduino que conecta a S3 del TCS3200 (filtro de color)
#define TOTAL_FILTROS 4
#define TIMEOUT_TCS3200 10000 // Máximo tiempo de espera de lectura (en microsegundos) 
#define TIEMPO_ENTRE_RESULTADOS 3000 // Esperar 3 segundos para mostrar el resultado
 
 
long cronometro_lecturas=0;
unsigned int contador_medidas=0;
unsigned char contador_filtro; // Contador global
unsigned char valor_intensidad_normalizado;
unsigned int pulso_medido;
float tiempo_pulso[TOTAL_FILTROS]={0,0,0,0}; // Valores medios
unsigned int minimo[TOTAL_FILTROS]={462,445,289,118};
unsigned int maximo[TOTAL_FILTROS]={7183,8558,6148,2446};
//unsigned int maximo[TOTAL_FILTROS]={7183,8558,6148,2446};
bool s2[TOTAL_FILTROS]={LOW,HIGH,LOW,HIGH}; // Valor del pin S2 para conseguir el rojo (0), verde (1) azul (2) y la luminosidad (3)
bool s3[TOTAL_FILTROS]={LOW,HIGH,HIGH,LOW}; // Valor del pin S3 para conseguir el rojo (0), verde (1) azul (2) y la luminosidad (3)
String nombre[TOTAL_FILTROS]={"Rojo","Verde","Azul","Blanco"};
 
void setup()
{
  pinMode(PIN_OUT,INPUT);
  pinMode(PIN_OE,OUTPUT);
  pinMode(PIN_S0,OUTPUT);
  pinMode(PIN_S1,OUTPUT);
  pinMode(PIN_S2,OUTPUT);
  pinMode(PIN_S3,OUTPUT);
  digitalWrite(PIN_S0,LOW);  // Modo de baja frecuencia (2%) 12 KHz máximo (con pulseIn la frecuencia máxima es de 50 KHz, tiempo mínimo 10 µs)
  digitalWrite(PIN_S1,HIGH); // Modo de baja frecuencia (2%) 12 KHz máximo (con pulseIn la frecuencia máxima es de 50 KHz, tiempo mínimo 10 µs)
  digitalWrite(PIN_OE,LOW);  // Activar el TCS3200 estableciendo un nivel bajo en OE
  Serial.begin(9600);
}
 
void loop()
{
  for(contador_filtro=0;contador_filtro<TOTAL_FILTROS;contador_filtro++)
  {
    digitalWrite(PIN_S2,s2[contador_filtro]);
    digitalWrite(PIN_S3,s3[contador_filtro]);
    contador_medidas++;
    pulseIn(PIN_OUT,LOW,TIMEOUT_TCS3200); // Esperar a que cambie el estado a bajo
    pulso_medido=pulseIn(PIN_OUT,HIGH,TIMEOUT_TCS3200); // Tiempo transcurrido hasta que cambia el estado (medio ciclo)
    pulso_medido+=pulseIn(PIN_OUT,LOW,TIMEOUT_TCS3200); // Volver a medir para completar y ciclo y disminuir un poco el error
    tiempo_pulso[contador_filtro]=tiempo_pulso[contador_filtro]*(contador_medidas-1)/contador_medidas+(float)pulso_medido/contador_medidas;
  }
  if((unsigned long)(millis()-cronometro_lecturas)>TIEMPO_ENTRE_RESULTADOS)
  {
    cronometro_lecturas=millis();
    //Serial.print(contador_medidas);
    //Serial.println(" medidas tomadas");
    contador_medidas=0;
    for(contador_filtro=0;contador_filtro<TOTAL_FILTROS;contador_filtro++)
    {
      valor_intensidad_normalizado=map(constrain(tiempo_pulso[contador_filtro],minimo[contador_filtro],maximo[contador_filtro]),minimo[contador_filtro],maximo[contador_filtro],255,0);
      Serial.print(tiempo_pulso[contador_filtro]);
      Serial.print("+");
      Serial.print(valor_intensidad_normalizado);
      Serial.print("  ");
      tiempo_pulso[contador_filtro]=0;
    }
    Serial.print("\n"); // Una línea en blanco como separador
  }
}
