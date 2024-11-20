import cv2 
import datetime
import time
from pyzbar import pyzbar 

# Define a dictionary to store barcode-to-name mappings
barcode_to_name = {
    "A342198A": "Hayden Hetrick",
    "A342100A": "Alexander Lipp",
    "A342351A": "Chandler Culp",
    # Add more mappings as needed
}

# Initialize a timestamp and state for each barcode
barcode_state = {}

def read_barcodes(frame):
    global barcode_state

    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect

        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX

        # Get the associated student name from the dictionary
        student_name = barcode_to_name.get(barcode_info, "Unknown")

        # Get the current date and time
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Determine state based on barcode
        if barcode_info in barcode_state:
            state = "Time Back"
        else:
            state = "Time Left"
            barcode_state[barcode_info] = True

        cv2.putText(frame, f"{student_name}, {current_time}, {state}", (x, y - 10), font, 0.5, (255, 255, 255), 1)

        # Print to terminal and save to file only if enough time has passed since the last print
        if time.time() - barcode_state.get(barcode_info, 0) >= 5:  # Allow re-scanning after 5 seconds
            print(f"Recognized Barcode: {barcode_info}, Student Name: {student_name}, Time: {current_time}, State: {state}")
            save_to_file(barcode_info, student_name, current_time, state)  # Save the barcode, student name, and time to a file
            barcode_state[barcode_info] = time.time()

    return frame 

def save_to_file(barcode_info, student_name, current_time, state):
    with open("barcode_result.txt", mode='a') as file:  # 'a' for append mode
        file.write(f"Recognized Barcode: {barcode_info}, Student Name: {student_name}, Time: {current_time}, State: {state}\n")

def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break 

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()