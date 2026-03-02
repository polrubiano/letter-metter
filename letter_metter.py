import math
import os

# Coordinates Eye Sense
eye_sense_coords = {
    'k': (4.7, 5), 'f': (14.5, 5), 'm': (24.3, 5), 't': (34.1, 5), 'b': (43.9, 5), 'q': (53.7, 5),
    'z': (9.6, 13.5), 'i': (19.4, 13.5), 'd': (29.2, 13.5), 's': (39, 13.5), 'u': (48.8, 13.5), 'j': (58.7, 13.5),
    'ñ': (4.7, 22), 'l': (14.5, 22), 'a': (24.3, 22), 'e': (34.1, 22), 'o': (43.9, 22), 'g': (53.7, 22),
    'x': (63.6, 22),
    'h': (9.6, 30.5), 'c': (19.4, 30.5), 'r': (29.2, 30.5), 'n': (39, 30.5), 'p': (48.8, 30.5), 'w': (58.7, 30.5),
    'y': (24.3, 39), 'v': (43.9, 39)
}

# Coordinates QWERTY
qwerty_coords = {
    'q': (5, 5), 'w': (15, 5), 'e': (25, 5), 'r': (35, 5), 't': (45, 5), 'y': (55, 5), 'u': (65, 5), 'i': (75, 5),
    'o': (85, 5), 'p': (95, 5),
    'a': (8, 15), 's': (18, 15), 'd': (28, 15), 'f': (38, 15), 'g': (48, 15), 'h': (58, 15), 'j': (68, 15),
    'k': (78, 15), 'l': (88, 15), 'ñ': (98, 15),
    'z': (13, 25), 'x': (23, 25), 'c': (33, 25), 'v': (43, 25), 'b': (53, 25), 'n': (63, 25), 'm': (73, 25)
}


def clean_text(text):
    text = text.lower()
    changes = str.maketrans("áéíóúü", "aeiouu")
    cleaned_text = text.translate(changes)
    return cleaned_text


def calculate_distance(text, keyboard, scale=1.0):
    """
    Calculates the total distance across the keyboard.
    The 'scale' parameter allows resizing the physical layout (default is 1.0).
    """
    letters = [char for char in text if char in keyboard]
    if len(letters) < 2:
        return 0.0, len(letters)

    distance = 0.0
    for i in range(len(letters) - 1):
        # Apply the scaling factor directly to the coordinates
        x1, y1 = keyboard[letters[i]]
        x2, y2 = keyboard[letters[i + 1]]

        x1, y1 = x1 * scale, y1 * scale
        x2, y2 = x2 * scale, y2 * scale

        distance += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance, len(letters)


def format_distance(distance_mm):
    abs_dist = abs(distance_mm)
    if abs_dist >= 1_000_000:
        return f"{distance_mm / 1_000_000:.3f} km"
    elif abs_dist >= 1_000:
        return f"{distance_mm / 1_000:.2f} m"
    else:
        return f"{distance_mm:.2f} mm"


def format_time(seconds):
    abs_secs = abs(seconds)
    if abs_secs >= 3600:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours} h {minutes} min"
    elif abs_secs >= 60:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes} min {secs:.1f} s"
    else:
        return f"{seconds:.2f} s"


def process_file(path, current_kpm, scale_eye=1.0, scale_qwerty=1.0):
    if not os.path.exists(path):
        print(f"Error: File not found: '{path}'.")
        return

    with open(path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    processed_text = clean_text(original_text)

    # CORREGIDO: Hemos vuelto a añadir los parámetros 'scale' que faltaban
    dist_eye, valid_keystrokes = calculate_distance(processed_text, eye_sense_coords, scale=scale_eye)
    dist_qwerty, _ = calculate_distance(processed_text, qwerty_coords, scale=scale_qwerty)
    saved_dist = dist_qwerty - dist_eye

    if valid_keystrokes < 2:
        print("Not enough valid letters to analyze.")
        return

    # 1. Current time on QWERTY based on user's KPM (Keystrokes Per Minute)
    time_qwerty_s = (valid_keystrokes / current_kpm) * 60

    # 2. Deduce physical speed (mm per second)
    physical_speed_mm_s = dist_qwerty / time_qwerty_s

    # 3. Apply physical speed to Eye Sense distance
    time_eye_s = dist_eye / physical_speed_mm_s

    # 4. Extrapolate new KPM for Eye Sense
    kpm_eye = (valid_keystrokes / time_eye_s) * 60

    saved_time = time_qwerty_s - time_eye_s
    sec_per_keystroke_qwerty = time_qwerty_s / valid_keystrokes
    sec_per_keystroke_eye = time_eye_s / valid_keystrokes

    print(f"File processed: {path}")
    print(f"Valid keystrokes: {valid_keystrokes}")
    print(f"Scale applied -> Eye Sense: {scale_eye}x | QWERTY: {scale_qwerty}x\n")

    print("-" * 45)
    print(f"Distance QWERTY:      {format_distance(dist_qwerty)}")
    print(f"Distance Eye Sense:   {format_distance(dist_eye)}")
    print("-" * 45)

    if saved_dist > 0:
        percent_dist = (saved_dist / dist_qwerty) * 100
        print(f"Saved distance: {format_distance(saved_dist)} ({percent_dist:.1f}% less movement)\n")

        # AÑADIDO: Formato simétrico para la línea de QWERTY
        print(f"️Time on QWERTY:      {format_time(time_qwerty_s):<15} -> "
              f"Baseline of {current_kpm:.1f} KPM ({sec_per_keystroke_qwerty:.1f} sec/keystroke)")
        print(f"Time on Eye Sense:   {format_time(time_eye_s):<15} -> "
              f"Extrapolated to {kpm_eye:.1f} KPM ({sec_per_keystroke_eye:.1f} sec/keystroke)")
        print(f"Total time saved:    {format_time(saved_time)}")

    elif saved_dist < 0:
        print(f"Eye Sense requires {format_distance(abs(saved_dist))} more distance.")
    else:
        print("Both keyboards require exactly the same distance.")


# --- INSTRUCTIONS FOR USE ---
# Change "user_current_kpm" to the Keystrokes Per Minute (KPM)
# that the user currently achieves on a traditional keyboard.
# For example, if a patient takes 4 seconds per keystroke, their KPM is 15. (60 seconds / 4 = 15 KPM)

user_current_kpm = 15

# Modifiers for physical scale testing (1.0 is the baseline size from the coordinates)
# Example: Change to 1.5 if your physical prototype key is 50% larger than 10mm x 10mm
eye_sense_scale = 1
qwerty_scale = 1

process_file("El ingenioso hidalgo Don Quijot - Miguel Cervantes.txt", user_current_kpm, scale_eye=eye_sense_scale, scale_qwerty=qwerty_scale)
