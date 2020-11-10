
bool start = false;

float Kp = 1462; // 600
float Ki = 0; // 0
float Kd = 23;   // 4.7

float Kp_cart = 0; // 10
float Kd_cart = 0; // 50
float Ki_cart = 0;  // 0

unsigned long prevTime = 0;
unsigned long prevDTime = 0;
unsigned long currTime = 0;


volatile long int cart_pos = 0;


volatile float err = 0;
volatile float prevErr = 0;
volatile float error[] = {0, 0, 0};
volatile float deriv_error[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
volatile float deriv_error_cart[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
volatile float prevDErr = 0;
volatile float prev_cart_error = 0;
volatile float cart_error = 0;

#define PI 3.1415926535897932384626433832795

void setup() {
  // put your setup code here, to run once:
  pinMode(A5, INPUT); // Angle sensor
  
  pinMode(2, INPUT);  // Encoder
  pinMode(3, INPUT);  // Encoder
  
  pinMode(4, OUTPUT); // Tells motor driver that it should rotate backwards
  pinMode(5, OUTPUT); // Tells motor driver that it should rotate forwards
  pinMode(9, OUTPUT); // PWM Signal that drives motor
  
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), encoder, RISING); // Encoder interrupt setup
  Serial.println("Setup complete!");
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available() && !start){
  }
  char in = Serial.read();
  if (in == 's'){
    start = true;
  }
  if (in == 'p'){
    start = false;
    analogWrite(9, 0);
  }
  float cErr = 0;
  float dErr = 0;
  while (start){
    unsigned long tempTime = millis();
    if(tempTime-currTime>=1){
          
      prevTime = currTime;
      currTime = tempTime;
      //Serial.println(currTime-prevTime);
      int sensorValue = analogRead(A5);
      prevErr = err;
    
      error[2] = error[1];
      error[1] = error[0];
      
      //err =  0 - ((sensorValue+(512-90))%1024-512)*PI/1024;
      error[0] = - ((sensorValue+(512-90))%1024-512)*PI/1024;

      float error_avg = (error[2]+error[1]+error[0])/3;
      /*
      if (currTime-prevDTime>50){
        dErr = 1000*(err - prevDErr)/(tempTime-prevDTime);
        //Serial.println(currTime-prevDTime);
        prevDErr = err;
        prevDTime = currTime;
      }*/

      deriv_error[9] = deriv_error[8];
      deriv_error[8] = deriv_error[7];
      deriv_error[7] = deriv_error[6];
      deriv_error[6] = deriv_error[5];
      deriv_error[5] = deriv_error[4];
      deriv_error[4] = deriv_error[3];
      deriv_error[3] = deriv_error[2];
      deriv_error[2] = deriv_error[1];
      deriv_error[1] = deriv_error[0];

      deriv_error_cart[9] = deriv_error_cart[8];
      deriv_error_cart[8] = deriv_error_cart[7];
      deriv_error_cart[7] = deriv_error_cart[6];
      deriv_error_cart[6] = deriv_error_cart[5];
      deriv_error_cart[5] = deriv_error_cart[4];
      deriv_error_cart[4] = deriv_error_cart[3];
      deriv_error_cart[3] = deriv_error_cart[2];
      deriv_error_cart[2] = deriv_error_cart[1];
      deriv_error_cart[1] = deriv_error_cart[0];

      deriv_error[0] = 1000*(error[0]-error[1])/(tempTime-prevDTime);
      cart_error  = 0 - (0.4/1065)*cart_pos;
      
      deriv_error_cart[0] = 1000*(cart_error-prev_cart_error)/(tempTime-prevDTime);
      
      float cart_deriv_avg = (deriv_error[9]+deriv_error[8])/10;
      cart_deriv_avg += (deriv_error_cart[7]+deriv_error_cart[6])/10;
      cart_deriv_avg += (deriv_error_cart[5]+deriv_error_cart[4])/10;
      cart_deriv_avg += (deriv_error_cart[3]+deriv_error_cart[2])/10;
      cart_deriv_avg += (deriv_error_cart[1]+deriv_error_cart[0])/10;

      
      float deriv_avg = (deriv_error[9]+deriv_error[8]+deriv_error[7]+deriv_error[6]+deriv_error[5]+deriv_error[4]+deriv_error[3]+deriv_error[2]+deriv_error[1]+deriv_error[0])/10;
      
      cErr += prevErr*(tempTime-prevTime)/1000;
      //Serial.println(cErr);
      float u = Kp*error[0]+Kd*dErr+Ki*cErr;
      u += Kp_cart*cart_error+Kd_cart*cart_deriv_avg;
    
      driveMotor(u);
      //Serial.println(u);
      //Serial.println(cart_pos);
    }
  }
}

void encoder(){
  
  if(digitalRead(3) == HIGH){
    cart_pos--;
  }
  else{
    cart_pos++;
  }
  
}

void driveMotor(float u){

  int input = (int)constrain(u*255/3.3, -255, 255);
  // Serial.println(input);
  if(input<0){

    // Motor going backward
    input = abs(input);
    
    digitalWrite(5, LOW);
    digitalWrite(4, HIGH);
    analogWrite(9, input);
    
  }
  else{

    // Motor going forward
    
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    analogWrite(9, input);
    
  }
  
}
