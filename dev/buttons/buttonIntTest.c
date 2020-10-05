#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include "pigpio.h"

//D-pad
#define DPAD_UP		21
#define DPAD_DOWN	16
#define DPAD_LEFT	12
#define DPAD_RIGHT	20

//Analog stick Select buttons
#define SEL_LEFT	26
#define SEL_RIGHT	4

//Shoulders
#define SHOULDER_LEFT	19
#define SHOULDER_RIGHT	13

//Buttons
#define BUTTON_A 18
#define BUTTON_B 1
#define BUTTON_X 24
#define BUTTON_Y 23

#define GPIO_TIMEOUT (60*60*1000*24) // One day timeout. It's ignored anyway.

#define ARR_SIZE(_x) (sizeof(_x)/sizeof(_x[0]))

typedef struct btnLookup
{
    uint8_t buttonNum;
    const char *name;
    uint8_t pullDir;
} btnLookup_t;

btnLookup_t buttonLUT[] =
{
	{DPAD_UP, "UP", PI_PUD_UP},
 	{DPAD_DOWN, "DOWN", PI_PUD_UP},
	{DPAD_LEFT, "LEFT", PI_PUD_UP},
	{DPAD_RIGHT, "RIGHT", PI_PUD_UP},
	{SEL_LEFT, "SEL_LEFT", PI_PUD_UP},
	{SEL_RIGHT, "SEL_RIGHT", PI_PUD_UP},
	{SHOULDER_LEFT, "SHLDR_LEFT", PI_PUD_UP},
	{SHOULDER_RIGHT, "SHLDR_RIGHT", PI_PUD_UP},
	{BUTTON_A, "A", PI_PUD_UP},
	{BUTTON_B, "B", PI_PUD_UP},
	{BUTTON_X, "X", PI_PUD_UP},
	{BUTTON_Y, "Y", PI_PUD_UP}
};

void buttonHandler(int gpio, int level, uint32_t tick)
{
	if(level == PI_TIMEOUT)
	{
		return;
	}

	uint8_t i;
	for(i = 0; (i < ARR_SIZE(buttonLUT)) && (buttonLUT[i].buttonNum != gpio); i++){}

	if(i == ARR_SIZE(buttonLUT))
		return;

	printf("%s %s", buttonLUT[i].name, level==PI_LOW?"pressed":"released\r\n");
}


int main(void)
{
    // Mandatory gpio initialization function for the pigpio library
    if(gpioInitialise() < 0)
    {
        printf("Gpio Init failed...\r\n");
	return 0;
    }

    uint8_t i;
    bool firstPressed = false;

    // Set the Pull Up/Down Direction
    for(i = 0; i < ARR_SIZE(buttonLUT); i++)
    {
	gpioSetMode(buttonLUT[i].buttonNum, PI_INPUT);
	gpioSetPullUpDown(buttonLUT[i].buttonNum, buttonLUT[i].pullDir);
	gpioSetISRFunc(buttonLUT[i].buttonNum, EITHER_EDGE, GPIO_TIMEOUT, buttonHandler);
    }

    // Loop forever printing the gpios pressed on screen
    while(1)
    {}

    gpioTerminate();

    return 0;
}
