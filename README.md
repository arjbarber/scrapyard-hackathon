# Bad Selfie Machine!
EPILEPSY WARNING: the hardware part of this project has strong, headache-inducing flashing lights! Please be cautious.

## Installation/use:
Supplies needed: computer, 64x32 LED Matrix & hackclub NEON microcontroller, USB C cable.

### Camera app:
1. Clone the repository to your computer
2. Run `pip install -r requirements.txt` to install required modules
3. Run the app using `python main.py`
4. The camera will take a screenshot when you blink

### LED Matrix:
1. Connect the microcontroller to your computer with the USBC cable
2. Flash the circuitpython firmware to the microcontroller
3. Replace all files on the microcontroller with the files in the LED Matrix folder
4. Go to `code.circuitpython.org`, connect your microcontroller and open `code.py`
5. Press save + run.