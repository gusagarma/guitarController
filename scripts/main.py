import mido
import json
from pynput.keyboard import Controller, Key
import time
import os
import threading

# Inicializa o teclado virtual
keyboard = Controller()

CONFIG_FILE = "midi_config.json"
HOLD_TIME = 1.0  # Tempo que a tecla de movimentação fica pressionada
LONG_HOLD_TIME = 3.0  # Tempo para ações que precisam ser seguradas (Zandatsu, Ninja Run)
PARRY_NOTE = 69  # Nota MIDI para executar o Parry

detecting_midi = True  # Controle para escutar MIDI durante a configuração

# Mapeia teclas especiais para evitar erros no pynput
SPECIAL_KEYS = {
    "ctrl": Key.ctrl,
    "shift": Key.shift,
    "tab": Key.tab,
    "space": Key.space,
}

# Exibir dispositivos MIDI disponíveis
print("\n=== Dispositivos MIDI Disponíveis ===")
available_ports = mido.get_input_names()
for i, port in enumerate(available_ports):
    print(f"{i}: {port}")

# Escolher o dispositivo MIDI correto
while True:
    try:
        device_index = int(input("\nDigite o número do dispositivo MIDI: "))
        if 0 <= device_index < len(available_ports):
            midi_input = mido.open_input(available_ports[device_index])
            break
        else:
            print("Número inválido. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Digite um número válido.")

# Função para escutar e exibir notas MIDI durante a configuração
def listen_midi():
    while detecting_midi:
        for msg in midi_input.iter_pending():
            if msg.type == "note_on" and msg.velocity > 0:
                print(f"🎵 Nota MIDI detectada: {msg.note}")

# Iniciar a thread de escuta MIDI para exibir os inputs ao vivo
midi_listener = threading.Thread(target=listen_midi, daemon=True)
midi_listener.start()

# Se existir um arquivo de configuração, carregar os valores salvos
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        MIDI_MAP = json.load(f)
    print("\n🎸 Configuração carregada do arquivo!")
else:
    # Permitir que o usuário defina os IDs das notas MIDI para cada tecla
    def choose_midi_note(action):
        while True:
            try:
                note_id = int(input(f"Digite o ID da nota MIDI para '{action}': "))
                return note_id
            except ValueError:
                print("Entrada inválida. Digite um número válido.")

    print("\nAgora, configure os IDs das notas para cada ação:")
    
    MIDI_MAP = {
        str(choose_midi_note("Frente (W)")): "w",
        str(choose_midi_note("Esquerda (A)")): "a",
        str(choose_midi_note("Trás (S)")): "s",
        str(choose_midi_note("Direita (D)")): "d",
        str(choose_midi_note("Ataque Fraco (J)")): "j",
        str(choose_midi_note("Ataque Forte (K)")): "k",
        str(choose_midi_note("Andar (Tab)")): "tab",
        str(choose_midi_note("Pular (Space)")): "space",
        str(choose_midi_note("Blade Mode (Shift)")): "shift",
        str(choose_midi_note("Ninja Run (Ctrl)")): "ctrl",
        str(choose_midi_note("Zandatsu/Ninja Kill (F)")): "f",
        str(choose_midi_note("Ripper Mode (R)")): "r",
        str(choose_midi_note("Lock-on (E)")): "e",
        str(choose_midi_note("Usar Sub-weapon (G)")): "g",
        str(choose_midi_note("Disparar Sub-weapon (Q)")): "q",
    }

    # Salvar configurações em um arquivo JSON
    with open(CONFIG_FILE, "w") as f:
        json.dump(MIDI_MAP, f, indent=4)

    print("\n🎸 Configuração salva! Agora ela será carregada automaticamente.")

# Parar a escuta MIDI depois da configuração
detecting_midi = False

# Diferenciar movimentação, ataque e botões de segurar
MOVEMENT_KEYS = ["w", "a", "s", "d"]
ATTACK_KEYS = ["j", "k"]
HOLD_KEYS = ["tab", "shift", "ctrl", "f", "r", "e", "g", "q"]  # Teclas que precisam ser seguradas por mais tempo

# Dicionário para armazenar o tempo de liberação das teclas de movimentação e ações
release_timers = {}

print("\n🎸 Configuração concluída! Aguardando input MIDI da guitarra...\n")

def execute_parry():
    """Executa a sequência de parry: W + J (com toques rápidos em J)"""
    keyboard.press("w")
    time.sleep(0.05)  # Pequeno delay para garantir que W seja registrado
    keyboard.press("j")
    keyboard.release("j")
    time.sleep(0.02)
    keyboard.press("j")
    keyboard.release("j")
    time.sleep(0.02)
    keyboard.press("j")
    keyboard.release("j")
    time.sleep(0.02)
    keyboard.press("j")
    keyboard.release("j")
    keyboard.release("w")
    print("🔥 PARRY EXECUTADO! (W + JJJJ) 🔥")

def process_midi():
    """Processa os inputs MIDI sem bloquear a execução"""
    global release_timers

    for msg in midi_input.iter_pending():
        if msg.type == "note_on" and msg.velocity > 0:
            if msg.note == PARRY_NOTE:
                # Criar uma thread para o parry, garantindo que a execução seja fluída
                threading.Thread(target=execute_parry, daemon=True).start()
                continue
            
            key = MIDI_MAP.get(str(msg.note))
            if key:
                key_to_press = SPECIAL_KEYS.get(key, key)

                if key in MOVEMENT_KEYS:
                    keyboard.press(key_to_press)
                    release_timers[key] = time.time() + HOLD_TIME
                    print(f"Nota MIDI {msg.note} -> Pressionando {key} por {HOLD_TIME}s")

                elif key in HOLD_KEYS:
                    keyboard.press(key_to_press)
                    release_timers[key] = time.time() + LONG_HOLD_TIME
                    print(f"Nota MIDI {msg.note} -> Segurando {key} por {LONG_HOLD_TIME}s")

                else:
                    keyboard.press(key_to_press)
                    keyboard.release(key_to_press)
                    print(f"Nota MIDI {msg.note} -> Pressionando {key}")

def release_keys():
    """Verifica se já passou o tempo de manter pressionado e solta as teclas"""
    global release_timers
    current_time = time.time()

    for key in list(release_timers.keys()):
        if current_time >= release_timers[key]:
            key_to_release = SPECIAL_KEYS.get(key, key)
            keyboard.release(key_to_release)
            print(f"Soltando {key} após tempo configurado")
            del release_timers[key]

try:
    while True:
        process_midi()
        release_keys()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nEncerrando...")
