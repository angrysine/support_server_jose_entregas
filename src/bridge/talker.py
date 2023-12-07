import time
import roslibpy
client = roslibpy.Ros(host='localhost', port=9090)
client.run()
talker = roslibpy.Topic(client, '/chatbot_topic', 'std_msgs/String')
while client.is_connected:
    talker.publish(roslibpy.Message({'data': '1,2'}))
    print('Sending message...')
    time.sleep(1)
talker.unadvertise()
client.terminate()
