from audioplayer import AudioPlayer
import time

# Playback stops when the object is destroyed (GC'ed), so save a reference to the object for non-blocking playback.
player = AudioPlayer("test/test.mp3")
player.play()


current_volume = 100
while True:
    if player.volume <= 5:
        increase_volume = True
    elif player.volume >= 100:
        increase_volume = False
  
    
    if increase_volume:
        current_volume += 5
    else:
        current_volume -= 5
    print(current_volume)
    player.volume = current_volume
    time.sleep(0.1)
    pass

