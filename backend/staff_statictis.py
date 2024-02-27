import keyboard
import psutil
import threading
import time


class Keylogger(threading.Thread):
    def __init__(self):
        super(Keylogger, self).__init__()
        self.active_window = None
        self.keys_pressed = 0
        self.opened_programs = set()
        self.start_time = time.time()

    def run(self):
        while True:
            self.get_active_window()
            self.update_opened_programs()
            print(f"Открытые программы: {self.opened_programs}, Количество нажатых клавиш: {self.keys_pressed}")
            time.sleep(60)

    def get_active_window(self):
        try:
            active_window_id = None
            if hasattr(psutil, 'sensors_battery'):
                active_window_id = psutil.Process(psutil.sensors_battery()).parent().pid
            else:
                active_window_id = psutil.Process(psutil.Process().pid).parent().pid

            for process in psutil.process_iter():
                if process.pid == active_window_id:
                    self.active_window = process.name()
                    break
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    def update_opened_programs(self):
        current_time = time.time()
        current_programs = set()
        for process in psutil.process_iter():
            try:
                if process.create_time() >= self.start_time:
                    current_programs.add(process.name())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

        new_programs = current_programs - self.opened_programs
        self.opened_programs.update(new_programs)


def main():
    keylogger = Keylogger()
    keylogger.start()

    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                keylogger.keys_pressed += 1
    except KeyboardInterrupt:
        pass

    keylogger.join()


if __name__ == "__main__":
    main()
