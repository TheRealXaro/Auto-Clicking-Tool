import threading
import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode


class ClickingScript(threading.Thread):
    """
    Separated script from UI, works only in an IDE

    NO UI!
    """
    def __init__(self, delay: float):
        super(ClickingScript, self).__init__()

        # Options
        self.delay = float(delay)
        self.button = Button.left
        self.running = False
        self.script_running = True
        self.click_thread = self
        self.click_delay = 0.01
        self.start_pause_key = KeyCode(char='a')
        self.stop_key = KeyCode(char='d')

        self.mouse = Controller()
        self.click_thread.start()

        with Listener(on_press=self.on_press) as lis:
            lis.join()

    def start_clicking(self):
        self.running = True
        return True

    def stop_clicking(self):
        self.running = False
        return False

    def exit(self):
        self.stop_clicking()
        self.script_running = False

    def run(self):
        while self.script_running:
            while self.running:
                self.mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

    def on_press(self, key):
        if key == self.start_pause_key:
            if self.click_thread.running:
                if __name__ == '__main__':
                    print("\033[37m>>> script has paused.")
                self.click_thread.stop_clicking()
                exit()
            else:
                if __name__ == '__main__':
                    print("\033[36m>>> script is running...")
                self.click_thread.start_clicking()
        elif key == self.stop_key:
            if __name__ == '__main__':
                print("\033[31m>>> \n\n\nscript has stopped.")
            self.click_thread.exit()
            exit()


if __name__ == '__main__':
    ClickingScript(0.01)
