#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <stdint.h>
#include <unistd.h>

#define ADS1115_ADDR  ((int)0x48)

//Address pointer addresses
#define ADDR_PTR_CONV ((int)0x00)
#define ADDR_PTR_CFG  ((int)0x01)
#define ADDR_PTR_LOTH ((int)0x02)
#define ADDR_PTR_HITH ((int)0x03)

//Configuration Register
#define OS_BIT     	(1<<15)
#define MUX_2_BIT  	(1<<14)
#define MUX_1_BIT  	(1<<13)
#define MUX_0_BIT  	(1<<12)
#define PGA_2_BIT  	(1<<11)
#define PGA_1_BIT  	(1<<10)
#define PGA_0_BIT  	(1<<9)
#define MODE_BIT   	(1<<8)
#define DR_2_BIT   	(1<<7)
#define DR_1_BIT       	(1<<6)
#define DR_0_BIT       	(1<<5)
#define COMP_MODE_BIT	(1<<4)
#define COMP_POL_BIT	(1<<3)
#define COMP_LAT_BIT    (1<<2)
#define COMP_QUE_1_BIT  (1<<1)
#define COMP_QUE_0_BIT  (1)

//Important configurations
#define AIN0_SINGLE (MUX_2_BIT)
#define AIN1_SINGLE (MUX_2_BIT | MUX_0_BIT)
#define AIN2_SINGLE (MUX_2_BIT | MUX_1_BIT)
#define AIN3_SINGLE (MUX_2_BIT | MUX_1_BIT | MUX_0_BIT)

#define FSR_PM_6144 (0x0)
#define FSR_PM_4096 (PGA_0_BIT)
#define FSR_PM_2048 (PGA_1_BIT)
#define FSR_PM_1024 (PGA_1_BIT | PGA_0_BIT)

#define MODE_CONT   (0x0)
#define MODE_SINGLE (MODE_BIT)

#define DR_128_SPS  (DR_2_BIT)
#define DR_250_SPS  (DR_2_BIT | DR_0_BIT)
#define DR_475_SPS  (DR_2_BIT | DR_1_BIT)
#define DR_860_SPS  (DR_2_BIT | DR_1_BIT | DR_0_BIT)

#define COMP_DISABLE (COMP_QUE_1_BIT | COMP_QUE_0_BIT)

#define DELAY_128_SPS_US 7800
#define DELAY_250_SPS_US 4000
#define DELAY_475_SPS_US 2106
#define DELAY_860_SPS_US 1163

#define DELAY_OFFSET_US 20


//Utility function
#define SWAP16(_num) ((_num<<8 & 0xff00) | (_num>>8 &0xff))

static const uint32_t channel_lut[] = {AIN0_SINGLE, AIN1_SINGLE, AIN2_SINGLE, AIN3_SINGLE};

using namespace std;

static int fd;

static int setAdcChannel(uint8_t channel)
{
    if(channel > sizeof(channel_lut))
    {
        printf("Bad Channel number %u", channel);
        return -1;
    }
    uint16_t config = (OS_BIT | channel_lut[channel] | FSR_PM_6144 | MODE_SINGLE | DR_860_SPS | COMP_DISABLE);

    return wiringPiI2CWriteReg16(fd, ADDR_PTR_CFG, SWAP16(config));
}

static int startConversion()
{
   return wiringPiI2CWrite(fd, ADDR_PTR_CONV);
}

int main()
{
   int result;
   int joystickValues[4]={0};

   fd = wiringPiI2CSetup(ADS1115_ADDR);

   cout << "Init result: "<< fd << endl;

   while(1)
   {
      for(uint8_t channel=0; channel<4; channel++)
      {
          if(setAdcChannel(channel) < 0)
          {
               printf("failed channel %d \r\n", channel);
          }
          if(startConversion() < 0)
          {
               printf("failed to start conversion on channel %u\r\n", channel);
          }
	  usleep(DELAY_860_SPS_US + DELAY_OFFSET_US);
	  result = wiringPiI2CRead(fd);
	  joystickValues[channel] = SWAP16(result);
      }

      printf("left(%05u, %05u) | right(%05u, %05u) \r", joystickValues[0], joystickValues[1], joystickValues[2], joystickValues[3]);
      fflush(stdout);
   }
}

