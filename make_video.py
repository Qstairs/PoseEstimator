import subprocess

def make_video(image_folder, output_path):

    command = f"ffmpeg -r 10 -i {image_folder}/%08d.jpg -vcodec libx264 -pix_fmt yuv420p -r 10 {output_path}"
    subprocess.run(command.split(" "))

if __name__ == "__main__":
    image_folder = "./outputs/walking_3"
    output_path = "./outputs/walking_3.mp4"
    make_video(image_folder, output_path)

