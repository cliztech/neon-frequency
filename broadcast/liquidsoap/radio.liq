# /etc/liquidsoap/radio.liq
# The Unshakeable Audio Foundation

# 1. SETTINGS
set("server.telnet", true)
set("server.telnet.port", 1234)
set("server.telnet.bind_addr", "0.0.0.0")

# 2. SOURCES
# Safety: Randomly plays if the brain fails
safety = mksafe(playlist(mode="random", "/music"))

# Brain Queue: Python pushes songs here
request_queue = request.equeue(id="brain_queue")

# Voice Queue: Python pushes Speech here
voice_queue = request.equeue(id="voice_queue")

# 3. MIXING
# Fallback logic: Try brain queue, then safety
radio = fallback(track_sensitive = true, [request_queue, safety])

# Ducking Logic: Lower music volume when voice plays
def apply_ducking(voice, music)
  add([voice, amplify(0.2, music)])
end

# Master Stream
stream = fallback(track_sensitive=false, [
  apply_ducking(voice_queue, radio),
  radio
])

# 4. OUTPUT
output.icecast(%mp3(bitrate=192),
  host = "icecast",
  port = 8000,
  password = "hackme",
  mount = "/neon",
  name = "Neon Frequency",
  description = "Cybernetic Broadcast System",
  stream)
