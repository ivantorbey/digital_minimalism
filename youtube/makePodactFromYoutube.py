import os
import datetime

# Set start date for downloads (YYYYMMDD format)
download_from = '20250219'

# Audio channels
audio_channels = ['https://www.youtube.com/@TechLead']

# Video channels
video_channels = ['https://www.youtube.com/@Fireship']

# Today's date for folder naming
today = datetime.date.today().strftime('%Y%m%d')

# Define output directory
output_dir = f"/Users/your_username/Desktop/a_faire/{today}"
os.makedirs(output_dir, exist_ok=True)

# Generate commands
commands = ''
for url in audio_channels:
    commands += f"yt-dlp --playlist-end 15 --dateafter {download_from} -x --audio-format mp3 '{url}' ;\n"

for url in video_channels:
    commands += f"yt-dlp --playlist-end 15 --dateafter {download_from} '{url}' ;\n"

# Write commands to shell script
script_path = os.path.join(output_dir, 'class.sh')
with open(script_path, 'w') as file:
    file.write(commands)

print(f"Commands script created at {script_path}")
