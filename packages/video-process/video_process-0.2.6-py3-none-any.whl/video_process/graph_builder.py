import math
import ffmpeg
from ffmpeg.nodes import Stream
from video_process.utils import get_video_duration


class GraphBuilder:
    def __init__(self, input_file):
        self.input_file = input_file
        self.stream = ffmpeg.input(input_file, vcodec="libvpx-vp9")
        self.audio = self.stream.audio
        self.video_info = ffmpeg.probe(input_file)["streams"][0]
        self.width = int(self.video_info["width"])
        self.height = int(self.video_info["height"])
        self.duration = get_video_duration(input_file)
        print("width: height", self.width, self.height)

    def add_bg(self, bg, x, y):
        if bg["bg_type"] == "video":
            self.add_bg_video(bg, x, y)
        elif bg["bg_type"] == "image":
            self.add_bg_image(bg, x, y)

    def add_bg_video(self, bg, x, y):
        bg_video = ffmpeg.input(bg["bg_video_path"])
        bg_audio = bg_video.audio
        bg_duration = float(ffmpeg.probe(bg["bg_video_path"])["streams"][0]["duration"])
        loop = bg["loop"]
        if loop and bg_duration < self.duration:
            repetitions = int(math.ceil(self.duration / bg_duration))
            repeated_bg_videos = [bg_video] * repetitions
            bg_video = ffmpeg.concat(*repeated_bg_videos, a=0, v=1)
            bg_audio = ffmpeg.concat(*repeated_bg_videos, a=1, v=0)

        bg_video = bg_video.filter(
            "crop",
            bg["crop"]["width"],
            bg["crop"]["height"],
            bg["crop"]["x"],
            bg["crop"]["y"],
        ).filter(
            "scale",
            width=self.width,
            height=self.height,
            force_original_aspect_ratio="none",
        )
        self.stream = ffmpeg.overlay(bg_video, self.stream, x=x, y=y, shortest=1)
        volume = bg["volume"]
        if volume and volume > 0:
            self.add_audio(bg_audio, bg)

    def add_bg_image(self, bg, x, y):
        bg_image = ffmpeg.input(bg["bg_image_path"])
        bg_image = bg_image.filter(
            "scale",
            width=self.width,
            height=self.height,
            force_original_aspect_ratio="none",
        )
        self.stream = ffmpeg.overlay(bg_image, self.stream, x=x, y=y)

    def add_overlay(self, layer):
        if layer["type"] == "image":
            overlay = ffmpeg.input(layer["layer_path"])
            self.stream = self.stream.overlay(overlay, x=layer["x"], y=layer["y"])
        elif layer["type"] == "sticker":
            overlay = ffmpeg.input(layer["layer_path"], **{"ignore_loop": "0"})
            self.stream = self.stream.overlay(
                overlay,
                x=layer["x"],
                y=layer["y"],
                shortest=1,
            )

    def add_bg_music(self, audio_filter: dict):
        audio = ffmpeg.input(audio_filter["path"]).audio
        bg_duration = float(
            ffmpeg.probe(audio_filter["path"])["streams"][0]["duration"]
        )
        if audio_filter["loop"] and bg_duration < self.duration:
            print("bg_duration", bg_duration)
            print("self.duration", self.duration)
            repetitions = int(math.ceil(self.duration / bg_duration))
            repeated_bg_audios = [audio] * repetitions
            audio = ffmpeg.concat(*repeated_bg_audios, a=1, v=0)
        self.add_audio(
            audio,
            audio_filter,
            fade_in=audio_filter["fade_in"],
            fade_out=audio_filter["fade_out"],
        )

    def add_audio(
        self, audio: Stream, audio_filter: dict, fade_in: int = 0, fade_out: int = 0
    ):
        print("audio_filter", audio_filter)
        audio = (
            audio.filter("volume", audio_filter["volume"])  # type: ignore
            .filter("afade", t="in", st=0, d=fade_in)
            .filter("afade", t="out", st=self.duration - fade_out, d=fade_out)
            .filter("atrim", duration=self.duration)
        )
        # audio.output("tmp.mp3").run()
        self.audio = ffmpeg.filter([self.audio, audio], "amix", inputs=2)

    def add_subtitle(self, subtitle_path):
        self.stream = self.stream.filter("ass", subtitle_path)

    def show_graph(self, graph_detail=False):
        ffmpeg.view(self.stream, detail=graph_detail, filename="graph")

    def scale_overlay(self, xpos=0.0, ypos=0.0, scale=1.0):
        w_overlay = int(self.width * xpos)
        h_overlay = int(-self.height * ypos)
        iw, ih = trunc_for_wh(self.width, self.height, scale)
        w_overlay += -int((iw - self.width) / 2)
        h_overlay += -int(ih - self.height)
        self.scale(iw, ih)
        return w_overlay, h_overlay

    def drop_first_frame(self):
        self.stream = self.stream.filter("select", "not(eq(n,0))")

    def scale(self, width, height):
        self.stream = self.stream.filter("scale", width=width, height=height)

    def overlay(self, x, y):
        self.stream = self.stream.filter("pad", width="iw", height="ih", x=x, y=y)

    def build(self, result_path="out.mp4", loglevel="info"):
        return ffmpeg.output(
            self.stream, self.audio, result_path, pix_fmt="yuv420p", loglevel=loglevel
        ).overwrite_output()

    def run(self, command):
        import shlex

        escaped_command = [shlex.quote(arg) for arg in command.compile()]
        print("command", " ".join(escaped_command))
        command.run()


def trunc_for_wh(w, h, scale=1.0):
    tw = int(w * scale)
    th = int(h * scale)
    if tw % 2 != 0:
        tw += 1
    if th % 2 != 0:
        th += 1
    return tw, th
