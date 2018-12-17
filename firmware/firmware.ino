#include <Stepper.h>

enum state_t
{
  HEADER,
  TYPE,
  SIZE,
  DATA,
  CRC
};

state_t state=HEADER;
uint8_t packet_type=0;
uint8_t packet_size=0;
uint8_t packet_data[255];
uint8_t packet_ptr=0;
const uint8_t HEADER_SIG=0x33;
const uint8_t MOVE_SIG=0x01;

const int steps=500;
Stepper roll(steps,4,5,6,7);
Stepper yaw(steps,9,10,11,12);
int light_pin=2;

int calc_crc(uint8_t* data,uint8_t size)
{
  uint8_t crc=0;
  for(int ii=0;ii<size;++ii)
    crc^=data[ii];
  return crc;
}

void handle_packet()
{
  if(packet_type==MOVE_SIG&&packet_size==5)
  {
    int16_t roll_amount=*(int16_t*)(packet_data+0);
    int16_t yaw_amount=*(int16_t*)(packet_data+2);
    uint8_t light_val=*(uint8_t*)(packet_data+4);
    if(roll_amount!=0)
      roll.step(roll_amount);
    if(yaw_amount!=0)
      yaw.step(yaw_amount);
    digitalWrite(light_pin,light_val);
  }
}

void setup()
{
  roll.setSpeed(10);
  yaw.setSpeed(10);
  pinMode(light_pin,OUTPUT);
  digitalWrite(light_pin,HIGH);
  Serial.begin(115200);
}

void loop()
{
  uint8_t temp=0;
  while(Serial.available()>0&&Serial.readBytes((char*)&temp,1)==1)
  {
    if(state==HEADER&&temp==HEADER_SIG)
      state=TYPE;
    else if(state==TYPE)
    {
      packet_type=temp;
      state=SIZE;
    }
    else if(state==SIZE)
    {
      packet_size=temp;
      packet_ptr=0;
      state=DATA;
    }
    else if(state==DATA)
    {
      packet_data[packet_ptr++]=temp;
      if(packet_ptr>=packet_size)
        state=CRC;
    }
    else if(state==CRC)
    {
      if(calc_crc(packet_data,packet_size)==temp)
        handle_packet();
      state=HEADER;
    }
  }
}
