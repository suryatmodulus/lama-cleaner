from datetime import datetime
from json import JSONDecodeError

import gradio as gr
from loguru import logger

from iopaint.const import *


_config_file: Path = None


class WebConfig(ApiConfig):
    model_dir: str = DEFAULT_MODEL_DIR


def load_config(p: Path) -> WebConfig:
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            try:
                return WebConfig(**{**default_configs, **json.load(f)})
            except JSONDecodeError:
                print(f"Load config file failed, using default configs")
                return WebConfig(**default_configs)
    else:
        return WebConfig(**default_configs)


def save_config(
    host,
    port,
    model,
    model_dir,
    no_half,
    low_mem,
    cpu_offload,
    disable_nsfw_checker,
    local_files_only,
    cpu_textencoder,
    device,
    input,
    output_dir,
    quality,
    enable_interactive_seg,
    interactive_seg_model,
    interactive_seg_device,
    enable_remove_bg,
    enable_anime_seg,
    enable_realesrgan,
    realesrgan_device,
    realesrgan_model,
    enable_gfpgan,
    gfpgan_device,
    enable_restoreformer,
    restoreformer_device,
):
    config = WebConfig(**locals())
    if str(config.input) == ".":
        config.input = None
    if str(config.output_dir) == ".":
        config.output_dir = None

    print(config.model_dump_json(indent=4))
    if config.input and not os.path.exists(config.input):
        return "[Error] Input file or directory does not exist"

    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f"[{current_time}] Successful save config to: {str(_config_file.absolute())}"
    logger.info(msg)
    try:
        with open(_config_file, "w", encoding="utf-8") as f:
            f.write(config.model_dump_json(indent=4))
    except Exception as e:
        return f"Save configure file failed: {str(e)}"
    return msg


def main(config_file: Path):
    global _config_file
    _config_file = config_file

    init_config = load_config(config_file)

    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.Textbox(config_file, label="Config file", interactive=False)
            with gr.Column():
                save_btn = gr.Button(value="Save configurations")
                message = gr.HTML()

        with gr.Tabs():
            with gr.Tab("Common"):
                with gr.Row():
                    host = gr.Textbox(init_config.host, label="Host")
                    port = gr.Number(init_config.port, label="Port", precision=0)

                model = gr.Radio(
                    AVAILABLE_MODELS + DIFFUSION_MODELS,
                    label="Models (https://www.iopaint.com/models)",
                    value=init_config.model,
                )
                device = gr.Radio(
                    Device.values(), label="Device", value=init_config.device
                )
                quality = gr.Slider(
                    value=95,
                    label=f"Image Quality ({QUALITY_HELP})",
                    minimum=75,
                    maximum=100,
                    step=1,
                )

                no_half = gr.Checkbox(init_config.no_half, label=f"{NO_HALF_HELP}")
                cpu_offload = gr.Checkbox(
                    init_config.cpu_offload, label=f"{CPU_OFFLOAD_HELP}"
                )
                low_mem = gr.Checkbox(init_config.low_mem, label=f"{LOW_MEM_HELP}")
                cpu_textencoder = gr.Checkbox(
                    init_config.cpu_textencoder, label=f"{CPU_TEXTENCODER_HELP}"
                )
                disable_nsfw_checker = gr.Checkbox(
                    init_config.disable_nsfw_checker, label=f"{DISABLE_NSFW_HELP}"
                )
                local_files_only = gr.Checkbox(
                    init_config.local_files_only, label=f"{LOCAL_FILES_ONLY_HELP}"
                )

                with gr.Column():
                    model_dir = gr.Textbox(
                        init_config.model_dir, label=f"{MODEL_DIR_HELP}"
                    )
                    input = gr.Textbox(
                        init_config.input,
                        label=f"Input file or directory. {INPUT_HELP}",
                    )
                    output_dir = gr.Textbox(
                        init_config.output_dir,
                        label=f"Output directory. {OUTPUT_DIR_HELP}",
                    )

            with gr.Tab("Plugins"):
                with gr.Row():
                    enable_interactive_seg = gr.Checkbox(
                        init_config.enable_interactive_seg, label=INTERACTIVE_SEG_HELP
                    )
                    interactive_seg_model = gr.Radio(
                        InteractiveSegModel.values(),
                        label=f"Segment Anything models. {INTERACTIVE_SEG_MODEL_HELP}",
                        value=init_config.interactive_seg_model,
                    )
                    interactive_seg_device = gr.Radio(
                        Device.values(),
                        label="Segment Anything Device",
                        value=init_config.interactive_seg_device,
                    )
                with gr.Row():
                    enable_remove_bg = gr.Checkbox(
                        init_config.enable_remove_bg, label=REMOVE_BG_HELP
                    )
                with gr.Row():
                    enable_anime_seg = gr.Checkbox(
                        init_config.enable_anime_seg, label=ANIMESEG_HELP
                    )

                with gr.Row():
                    enable_realesrgan = gr.Checkbox(
                        init_config.enable_realesrgan, label=REALESRGAN_HELP
                    )
                    realesrgan_device = gr.Radio(
                        Device.values(),
                        label="RealESRGAN Device",
                        value=init_config.realesrgan_device,
                    )
                    realesrgan_model = gr.Radio(
                        RealESRGANModel.values(),
                        label="RealESRGAN model",
                        value=init_config.realesrgan_model,
                    )
                with gr.Row():
                    enable_gfpgan = gr.Checkbox(
                        init_config.enable_gfpgan, label=GFPGAN_HELP
                    )
                    gfpgan_device = gr.Radio(
                        Device.values(),
                        label="GFPGAN Device",
                        value=init_config.gfpgan_device,
                    )
                with gr.Row():
                    enable_restoreformer = gr.Checkbox(
                        init_config.enable_restoreformer, label=RESTOREFORMER_HELP
                    )
                    restoreformer_device = gr.Radio(
                        Device.values(),
                        label="RestoreFormer Device",
                        value=init_config.restoreformer_device,
                    )

        save_btn.click(
            save_config,
            [
                host,
                port,
                model,
                model_dir,
                no_half,
                low_mem,
                cpu_offload,
                disable_nsfw_checker,
                local_files_only,
                cpu_textencoder,
                device,
                input,
                output_dir,
                quality,
                enable_interactive_seg,
                interactive_seg_model,
                interactive_seg_device,
                enable_remove_bg,
                enable_anime_seg,
                enable_realesrgan,
                realesrgan_device,
                realesrgan_model,
                enable_gfpgan,
                gfpgan_device,
                enable_restoreformer,
                restoreformer_device,
            ],
            message,
        )
    demo.launch(inbrowser=True, show_api=False)
