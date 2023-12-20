import roslibpy
import os
import threading

def run_command(command):
    os.system(command)
command_thread = threading.Thread(target=run_command, args=("ros2 launch rosbridge_server rosbridge_websocket_launch.xml",))
command_thread.start()

client = roslibpy.Ros(host='localhost', port=9090)

client.run()
class Talker:
    def __init__(self,topic,message_type='std_msgs/String'):
        self.talker = roslibpy.Topic(client, f'/{topic}', message_type)
    def send(self, message):
        self.talker.publish(roslibpy.Message({'data': message}))
    def close(self):
        self.talker.unadvertise()
        self.client.terminate()


