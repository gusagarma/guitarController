# 🎸 Guitar Controller para Metal Gear Rising: Revengeance 🎸

Este é um script que permite jogar **seu game favorito** usando **uma guitarra MIDI como controle**.  
Nada de teclado ou joystick—**somente riffs e golpes sincronizados!**  

[![Gameplay Preview](https://www.youtube.com/watch?v=fDZxpDFkkWU)

---

## 🔥 O que esse script faz?

-**Mapeia** as notas da guitarra MIDI para controles do jogo  
-**Personalizável** – Escolha as notas para cada ação  
-**Parry simplificado** – Uma única nota para executar defesas perfeitas  
-**Detecção MIDI em tempo real**  

---

## 🎛 Requisitos

### 🛠 **Softwares Necessários**
🔹 [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) – Cria um dispositivo MIDI virtual  
🔹 [MIDI Guitar 2](https://www.amplesound.net/en/index.asp) – Converte o áudio da guitarra em sinais MIDI  

### 🖥 **Dependências do Python**
Instale os pacotes necessários antes de rodar o script:  
```bash
pip install mido pynput
```
## 🎮 Como usar

1️⃣ **Conecte sua guitarra MIDI** ou use *MIDI Guitar 2* para capturar o som da guitarra e transformá-lo em notas MIDI.  

2️⃣ **Abra o loopMIDI** e crie um dispositivo virtual para rotear os sinais MIDI.  

3️⃣ **Execute o script:**  

   ```bash
   python main.py
```

4️⃣ Escolha o dispositivo MIDI correto ao iniciar o script.

5️⃣ Configure os controles: o script pedirá para mapear as notas da guitarra para cada ação do jogo.

6️⃣ Abra o seu jogo favorito e jogue com sua guita!



