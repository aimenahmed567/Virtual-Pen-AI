# VirtualPenAI ✋🖊️

VirtualPenAI is a real-time air drawing application built with **Python**, **OpenCV**, and **MediaPipe**.  
It turns your webcam into a touchless drawing board where you can draw in the air using your **right-hand index finger**.

The project features a translucent canvas, responsive on-screen buttons, color palette, and pen type selection — giving an AR-style interactive experience without any physical input device.

---

## 🚀 Features

- Real-time hand & finger tracking  
- Draw using the right-hand index finger  
- Gesture-based mode switching  
- On-screen UI with:
  - Color selection  
  - Pen type change (pen, brush, highlighter, eraser)  
  - Clear canvas option  
- Smooth, translucent drawing canvas  
- Modular and clean project structure  

---

## 🧠 Tech Stack

- Python 3.11  
- OpenCV  
- MediaPipe  
- NumPy  

---

## 📁 Project Structure

VirtualPenAI/
├── main.py
├── README.md
├── core/
│ ├── init.py
│ ├── hand_tracker.py
│ ├── gestures.py
│ └── drawing_engine.py
├── ui/
│ ├── palette.png
│ ├── toolbar.png
│ └── buttons/
│ ├── pen.png
│ ├── brush.png
│ ├── highlighter.png
│ ├── eraser.png
│ └── clear.png
├── assets/
│ └── sounds/
│ └── click.wav
└── output/
└── drawings/


---

## ⚙️ Installation

```bash
pip install opencv-python mediapipe numpy
Run the project:

python main.py
🎯 Use Cases
Touchless whiteboard

Online teaching & presentations

Interactive learning for kids

Smart classrooms

AR-style creative tools

💡 About
VirtualPenAI demonstrates the power of Computer Vision and Human–Computer Interaction by allowing users to draw without touching any device.
It is ideal for portfolios, internships, viva presentations, and academic showcases.

